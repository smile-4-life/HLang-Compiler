"""
Static Semantic Checker for HLang Programming Language
"""

from functools import reduce
from typing import Dict, List, Set, Optional, Any, Tuple, Union, NamedTuple
from ..utils.visitor import ASTVisitor
from ..utils.nodes import (
    ASTNode, Program, ConstDecl, FuncDecl, Param, VarDecl, Assignment, 
    IfStmt, WhileStmt, ForStmt, ReturnStmt, BreakStmt, ContinueStmt, 
    ExprStmt, BlockStmt, IntType, FloatType, BoolType, StringType, 
    VoidType, ArrayType, IdLValue, ArrayAccessLValue, BinaryOp, UnaryOp, 
    FunctionCall, ArrayAccess, Identifier, IntegerLiteral, FloatLiteral, 
    BooleanLiteral, StringLiteral, ArrayLiteral
)
from .static_error import (
    StaticError, Redeclared, Undeclared, TypeMismatchInExpression,
    TypeMismatchInStatement, TypeCannotBeInferred, NoEntryPoint,
    MustInLoop
)

# Import marker classes with different names to avoid conflict  
from .static_error import Identifier as IdentifierMarker, Function as FunctionMarker

class Symbol:
    def __init__(self, kind: str, type_: Any = None, mutable: bool = True):
        self.kind = kind                     # 'var' | 'const' | 'param' | 'func' | 'builtin'
        self.type = type_                     # Type node (IntType, ArrayType(...), ...)
        self.mutable = mutable               # False for const
        # For functions only:
        self.param_types: Optional[List[Any]] = None
        self.return_type: Optional[Any] = None
        self.size = None                     # For arrays, size is the length of the array

    def __repr__(self):
        if self.kind in ("func", "builtin"):
            return f"<{self.kind} ({self.param_types})->{self.return_type}>"
        return f"<{self.kind}:{self.type}{'' if self.mutable else ' (const)'}>"


class Scope:
    def __init__(self, parent: Optional['Scope']=None):
        self.parent = parent
        self.locals: Dict[str, Symbol] = {}

    def define(self, name: str, sym: Symbol):
        if name in self.locals:
            if sym.kind == "var":
                raise Redeclared("Variable", name)
            if sym.kind == "const":
                raise Redeclared("Constant", name)
            if sym.kind == "param":
                raise Redeclared("Parameter", name)
            if sym.kind == "func":
                raise Redeclared("Function", name)
        self.locals[name] = sym

    def lookup_local(self, name: str) -> Optional[Symbol]:
        return self.locals.get(name)

    def lookup(self, name: str) -> Optional[Symbol]:
        cur = self
        while cur:
            if name in cur.locals:
                return cur.locals[name]
            cur = cur.parent
        return None


# ----------------------------
# Static Checker
# ----------------------------

class StaticChecker(ASTVisitor):
    def __init__(self):
        super().__init__()
        self.current_scope: Scope = Scope(None)
        self.current_func: Optional[str] = None
        self.current_return_type: Optional[Any] = None
        self.loop_depth: int = 0
        self._install_builtins()

    # ---------- Built-ins ----------
    def _install_builtins(self):
        # Input/Output Functions
        # print(string) -> void
        print_sym = Symbol("builtin")
        print_sym.param_types = [StringType()]
        print_sym.return_type = VoidType()
        self.current_scope.define("print", print_sym)

        # input() -> string
        input_sym = Symbol("builtin")
        input_sym.param_types = []
        input_sym.return_type = StringType()
        self.current_scope.define("input", input_sym)

        # Type Conversion Functions
        # str(x: any) -> string (general version)
        str_sym = Symbol("builtin")
        str_sym.param_types = [None]  # Dynamic type checking
        str_sym.return_type = StringType()
        self.current_scope.define("str", str_sym)

        # int(x: string|int|float) -> int
        int_sym = Symbol("builtin")
        int_sym.param_types = [None]  # Dynamic checking for string/int/float
        int_sym.return_type = IntType()
        self.current_scope.define("int", int_sym)

        # float(x: string|int|float) -> float
        float_sym = Symbol("builtin")
        float_sym.param_types = [None]  # Dynamic checking for string/int/float
        float_sym.return_type = FloatType()
        self.current_scope.define("float", float_sym)

        # bool2str(bool) -> string
        bool2str_sym = Symbol("builtin")
        bool2str_sym.param_types = [BoolType()]
        bool2str_sym.return_type = StringType()
        self.current_scope.define("bool2str", bool2str_sym)

        # str2int(string) -> int
        str2int_sym = Symbol("builtin")
        str2int_sym.param_types = [StringType()]
        str2int_sym.return_type = IntType()
        self.current_scope.define("str2int", str2int_sym)

        # str2float(string) -> float
        str2float_sym = Symbol("builtin")
        str2float_sym.param_types = [StringType()]
        str2float_sym.return_type = FloatType()
        self.current_scope.define("str2float", str2float_sym)

        # Array Utility Functions
        # len([T;N]) -> int
        len_sym = Symbol("builtin")
        len_sym.param_types = [["array"]]  # Special marker for array type
        len_sym.return_type = IntType()
        self.current_scope.define("len", len_sym)


    # ---------- Entry ----------
    def check_program(self, program_node: Program):
        self.visit(program_node)

    # ---------- Utility: robust list handling ----------
    @staticmethod
    def _flatten_maybe_list(seq):
        """Return a flat list whether seq is a node, a list, or list-of-lists."""
        if seq is None:
            return []
        if isinstance(seq, list):
            flat = []
            for x in seq:
                if isinstance(x, list):
                    flat.extend(x)
                else:
                    flat.append(x)
            return flat
        # single node
        return [seq]

    @staticmethod
    def _stmts_from_body(body) -> List[ASTNode]:
        """Return list of statements from a body that may be BlockStmt or list."""
        if isinstance(body, BlockStmt):
            return list(getattr(body, "statements", []) or [])
        if isinstance(body, list):
            return body
        # fallback: unknown container -> wrap
        return [body] if body is not None else []

    # ---------- Program ----------
    def visit_program(self, node: Program, o: Any=None):
        # Load global consts & vars first
        for decl in getattr(node, "const_decls", []):
            self.visit(decl, o)
            
        # Predeclare function headers (for mutual recursion)
        for f in getattr(node, "func_decls", []):
            self._declare_function_header(f)

        # Visit function bodies
        for func in getattr(node, "func_decls", []):
            self.visit(func, o)

        # Check entry point
        main_sym = self.current_scope.lookup("main")
        if not main_sym or main_sym.kind != "func":
            raise NoEntryPoint()
        if (main_sym.param_types and len(main_sym.param_types) != 0) or not isinstance(main_sym.return_type, VoidType):
            raise NoEntryPoint()

    # ---------- Declarations ----------
    def visit_const_decl(self, node: ConstDecl, o: Any=None):
        if self.current_scope.lookup_local(node.name):
            raise Redeclared("Constant", node.name)

        ann = getattr(node, "type_annotation", None) 
        init = getattr(node, "value", None)

        if init is None:
            raise TypeCannotBeInferred(node)
        vtype = self.visit(init)
        if ann is not None:
            at = self.visit(ann)
            if isinstance(at,VoidType):
                raise TypeMismatchInExpression(init)
            if not self._is_same_type(at, vtype):
                raise TypeMismatchInStatement(node)
            dtype = at
        else:
            dtype = vtype

        self.current_scope.define(node.name, Symbol("const", dtype, mutable=False))

    def visit_var_decl(self, node: VarDecl, o: Any=None):
        if self.current_scope.lookup_local(node.name):
            raise Redeclared("Variable", node.name)
        ann = getattr(node, "type_annotation", None) 
        init = getattr(node, "value", None)
        if ann is None and init is None:
            raise TypeCannotBeInferred(node)

        if ann is not None:
            size = None;
            at = self.visit(ann)
            if init is not None:
                et = self.visit(init)
                if isinstance(et,VoidType):
                    raise TypeMismatchInExpression(init);
                if isinstance(et, ArrayType):
                    size = at.size
                if not self._is_same_type(at, et):
                    raise TypeMismatchInStatement(node)
            sym = Symbol("var", at, True)
            sym.size = size  
            self.current_scope.define(node.name, sym)
        else:
            et = self.visit(init)
            if et is None:
                raise TypeCannotBeInferred(node)
            if isinstance(et,VoidType):
                raise TypeMismatchInExpression(init);
            if isinstance(et, VoidType):
                raise TypeMismatchInStatement(node)
            self.current_scope.define(node.name, Symbol("var", et, mutable=True))

    def _declare_function_header(self, node: FuncDecl):
        if self.current_scope.lookup_local(node.name):
            raise Redeclared("Function", node.name)

        # Parameter types
        param_types: List[Any] = []
        for p in getattr(node, "params", []):
            # Param node must have .param_type
            ptype = self.visit(p)
            param_types.append(ptype)

        ret = self.visit(node.return_type) if getattr(node, "return_type", None) else VoidType()

        sym = Symbol("func")
        sym.param_types = param_types
        sym.return_type = ret
        self.current_scope.define(node.name, sym)

    def visit_func_decl(self, node: FuncDecl, o: Any=None):
        func_sym = self.current_scope.lookup(node.name)
        # Enter new function scope
        prev_scope = self.current_scope
        prev_func = self.current_func
        prev_ret = self.current_return_type
        self.current_scope = Scope(prev_scope)
        self.current_func = node.name
        self.current_return_type = func_sym.return_type

        # Parameters unique within function scope
        seen = set()
        params = getattr(node, "params", [])
        for i, p in enumerate(params):
            if p.name in seen:
                raise Redeclared("Parameter", p.name)
            seen.add(p.name)
            self.current_scope.define(p.name, Symbol("param", func_sym.param_types[i], mutable=True))

        # Visit body
        for stmt in self._stmts_from_body(node.body):
            self.visit(stmt, o)

        # After visiting, ensure non-void function returns on all paths
        if not isinstance(func_sym.return_type, VoidType):
            if not self._block_returns_always(self._stmts_from_body(node.body)):
                # Mismatch at function level
                raise TypeMismatchInStatement(node)

        # Exit
        self.current_scope = prev_scope
        self.current_func = prev_func
        self.current_return_type = prev_ret

    def visit_param(self, node: Param, o: Any=None):
        return self.visit(node.param_type)

    # ---------- Statements ----------
    def visit_block_stmt(self, node: BlockStmt, o: Any=None):
        prev = self.current_scope
        self.current_scope = Scope(prev)
        for st in self._stmts_from_body(node):
            self.visit(st)
        self.current_scope = prev

    def visit_assignment(self, node: Assignment, o: Any=None):
        ltype, lmutable = self._typeof_lvalue(node.lvalue)
        rnode = getattr(node, "value", None)
        rtype = self.visit(rnode)
        if isinstance(rtype, VoidType):
            raise TypeMismatchInStatement(node)
        if not self._is_same_type(ltype, rtype):
            raise TypeMismatchInStatement(node)  
        if not lmutable:
            raise TypeMismatchInStatement(node)
            
                     

    def visit_if_stmt(self, node: IfStmt, o: Any=None):
        ctype = self.visit(node.condition)
        if not isinstance(ctype, BoolType):
            raise TypeMismatchInStatement(node)

        self.visit(node.then_stmt)
        for pair in getattr(node, "elif_branches", []) or []:
            if isinstance(pair, tuple) or isinstance(pair, list):
                econd, ebody = pair
            else:
                # Pair-like object with .condition and .stmt?
                econd = getattr(pair, "condition", None)
                ebody = getattr(pair, "stmt", None)
            et = self.visit(econd)
            if not isinstance(et, BoolType):
                raise TypeMismatchInStatement(node)
            self.visit(ebody)

        if getattr(node, "else_stmt", None):
            self.visit(node.else_stmt)

    def visit_while_stmt(self, node: WhileStmt, o: Any=None):
        ctype = self.visit(node.condition)
        if not isinstance(ctype, BoolType):
            raise TypeMismatchInStatement(node)
        self.loop_depth += 1
        self.visit(node.body)
        self.loop_depth -= 1

    def visit_for_stmt(self, node: ForStmt, o: Any=None):
        it_type = self.visit(node.iterable)
        if not isinstance(it_type, ArrayType):
            raise TypeMismatchInStatement(node)

        prev = self.current_scope
        self.current_scope = Scope(prev)

        # loop variable may be Identifier or have .name
        if isinstance(node.variable, Identifier):
            vname = node.variable.name
        else:
            vname = getattr(node.variable, "name", str(node.variable))

        if self.current_scope.lookup_local(vname):
            raise Redeclared("Variable", vname)
        self.current_scope.define(vname, Symbol("var", it_type.element_type, mutable=True))

        self.loop_depth += 1
        self.visit(node.body)
        self.loop_depth -= 1

        self.current_scope = prev

    def visit_return_stmt(self, node: ReturnStmt, o: Any=None):
        if self.current_func is None:
            raise TypeMismatchInStatement(node)
        expected = self.current_return_type
        val = getattr(node, "value", None)
        if isinstance(expected, VoidType):
            if val is not None:
                raise TypeMismatchInStatement(node)
        else:
            if val is None:
                raise TypeMismatchInStatement(node)
            vtype = self.visit(val)
            if not self._is_same_type(expected, vtype):
                raise TypeMismatchInStatement(node)

    def visit_break_stmt(self, node: BreakStmt, o: Any=None):
        if self.loop_depth <= 0:
            raise MustInLoop(node)

    def visit_continue_stmt(self, node: ContinueStmt, o: Any=None):
        if self.loop_depth <= 0:
            raise MustInLoop(node)

    def visit_expr_stmt(self, node: ExprStmt, o: Any=None):
        self.visit(node.expr)

    # ---------- LValues ----------
    def _typeof_lvalue(self, lv: Any) -> Tuple[Any, bool]:
        if isinstance(lv, IdLValue):
            sym = self.current_scope.lookup(lv.name)
            if not sym:
                raise Undeclared(IdentifierMarker(), lv.name)
            return sym.type, sym.mutable
        if isinstance(lv, ArrayAccessLValue):
            at = self.visit(lv.array)
            if not isinstance(at, ArrayType):
                raise TypeMismatchInExpression(lv)
            idx_t = self.visit(lv.index)
            if not isinstance(idx_t, IntType):
                raise TypeMismatchInExpression(lv)
            # treat elements as mutable if array symbol is mutable (approx)
            return at.element_type, True
        raise TypeMismatchInStatement(lv)

    def visit_id_lvalue(self, node: IdLValue, o: Any=None):
        t, _ = self._typeof_lvalue(node)
        return t

    def visit_array_access_lvalue(self, node: ArrayAccessLValue, o: Any=None):
        t, _ = self._typeof_lvalue(node)
        return t

    # ---------- Expressions ----------
    def _resolve_func_name(self, node: FunctionCall) -> str:
        if hasattr(node, "function"):
            if isinstance(node.function, Identifier):
                return node.function.name
            return str(node.function)
        if hasattr(node, "name"):
            return node.name
        return ""

    def visit_identifier(self, node: Identifier, o: Any=None):
        sym = self.current_scope.lookup(node.name)
        if not sym:
            raise Undeclared(IdentifierMarker(), node.name)
        return sym.type

    def visit_function_call(self, node: FunctionCall, o: Any=None):
        fname = self._resolve_func_name(node)
        sym = self.current_scope.lookup(fname)
        if not sym or sym.kind not in ("func", "builtin"):
            raise Undeclared(FunctionMarker(), fname)

        # builtins
        if fname == "str":
            if len(node.args) != 1:
                raise TypeMismatchInExpression(node)
            t = self.visit(node.args[0])
            if not isinstance(t, (IntType, FloatType, BoolType, StringType)):
                raise TypeMismatchInExpression(node)
            return StringType()

        if fname == "int":
            if len(node.args) != 1:
                raise TypeMismatchInExpression(node)
            t = self.visit(node.args[0])
            if not isinstance(t, (StringType, IntType, FloatType)):
                raise TypeMismatchInExpression(node)
            return IntType()

        if fname == "float":
            if len(node.args) != 1:
                raise TypeMismatchInExpression(node)
            t = self.visit(node.args[0])
            if not isinstance(t, (StringType, IntType, FloatType)):
                raise TypeMismatchInExpression(node)
            return FloatType()

        if fname == "len":
            if len(node.args) != 1:
                raise TypeMismatchInExpression(node)
            at = self.visit(node.args[0])
            if not isinstance(at, ArrayType):
                raise TypeMismatchInExpression(node)
            return IntType()

        if fname == "print":
            if len(node.args) != 1:
                raise TypeMismatchInStatement(node)
            a = self.visit(node.args[0])
            if not isinstance(a, StringType):
                raise TypeMismatchInStatement(node)
            return VoidType()

        # user-defined function
        if len(node.args) != len(sym.param_types or []):
            raise TypeMismatchInExpression(node)

        # Check param types
        for i, arg in enumerate(node.args):
            at = self.visit(arg)
            pt = sym.param_types[i]
            if not self._is_same_type(pt, at):
                raise TypeMismatchInExpression(node)


        return sym.return_type

    def visit_array_access(self, node: ArrayAccess, o: Any=None):
        at = self.visit(node.array)
        if not isinstance(at, ArrayType):
            raise TypeMismatchInExpression(node)
        it = self.visit(node.index)
        if not isinstance(it, IntType):
            raise TypeMismatchInExpression(node)
        if node.index.value >= at.size:
            raise TypeMismatchInExpression(node)
        
        return at.element_type

    def visit_array_literal(self, node: ArrayLiteral, o: Any=None):
        if not node.elements:
            raise TypeCannotBeInferred(node)
        
        # Check all elements for consistent type
        first_type = self.visit(node.elements[0])
        for elem in node.elements[1:]:
            elem_type = self.visit(elem)
            if not self._is_same_type(first_type, elem_type):
                raise TypeMismatchInExpression(node)
        
        # Check size if required by context
        expected_size = None
        if o and 'expected_type' in o and isinstance(o['expected_type'], ArrayType):
            expected_size = o['expected_type'].size
        
        # If expected size exists, number of elements must match
        if expected_size is not None and len(node.elements) != expected_size:
            raise TypeMismatchInExpression(node)
        
        return ArrayType(first_type, len(node.elements))

    def visit_binary_op(self, node: BinaryOp, o: Any=None):
        op = node.operator
        lt = self.visit(node.left)
        rt = self.visit(node.right)

        # Arithmetic +, -, *, /
        if op in ["+", "-", "*", "/"]:
            if isinstance(lt, StringType) and isinstance(rt, StringType) and op == "+":
                return StringType()
            if isinstance(lt, (IntType, FloatType)) and isinstance(rt, (IntType, FloatType)):
                if isinstance(lt, FloatType) or isinstance(rt, FloatType):
                    return FloatType()
                return IntType()
            raise TypeMismatchInExpression(node)

        # Modulo
        if op == "%":
            if isinstance(lt, IntType) and isinstance(rt, IntType):
                return IntType()
            raise TypeMismatchInExpression(node)

        # Comparison <, <=, >, >=
        if op in ["<", "<=", ">", ">="]:
            if isinstance(lt, (IntType, FloatType)) and isinstance(rt, (IntType, FloatType)):
                return BoolType()
            raise TypeMismatchInExpression(node)

        # Equality ==, !=
        if op in ["==", "!="]:
            if self._is_same_type(lt, rt):
                return BoolType()
            raise TypeMismatchInExpression(node)

        # Logical &&, ||
        if op in ["&&", "||"]:
            if isinstance(lt, BoolType) and isinstance(rt, BoolType):
                return BoolType()
            raise TypeMismatchInExpression(node)

        raise TypeMismatchInExpression(node)

    def visit_unary_op(self, node: UnaryOp, o: Any=None):
        op = node.operator
        t = self.visit(node.operand)
        if op == "!":
            if isinstance(t, BoolType):
                return BoolType()
            raise TypeMismatchInExpression(node)
        if op in ["+", "-"]:
            if isinstance(t, (IntType, FloatType)):
                return t.__class__()
            raise TypeMismatchInExpression(node)
        raise TypeMismatchInExpression(node)

    # ---------- Literals ----------
    def visit_integer_literal(self, node: IntegerLiteral, o: Any=None):
        return IntType()

    def visit_float_literal(self, node: FloatLiteral, o: Any=None):
        return FloatType()

    def visit_boolean_literal(self, node: BooleanLiteral, o: Any=None):
        return BoolType()

    def visit_string_literal(self, node: StringLiteral, o: Any=None):
        return StringType()

    # ---------- Types ----------
    def visit_int_type(self, node: IntType, o: Any=None):
        return node

    def visit_float_type(self, node: FloatType, o: Any=None):
        return node

    def visit_bool_type(self, node: BoolType, o: Any=None):
        return node

    def visit_string_type(self, node: StringType, o: Any=None):
        return node

    def visit_void_type(self, node: VoidType, o: Any=None):
        return node

    def visit_array_type(self, node: ArrayType, o: Any=None):
        self.visit(node.element_type)
        return node

    # ---------- Helpers ----------
    def _is_same_type(self, a: Any, b: Any) -> bool:
        if isinstance(a, ArrayType) and isinstance(b, ArrayType):
            return a.size == b.size and self._is_same_type(a.element_type, b.element_type)
        return type(a) is type(b)

    def _block_returns_always(self, stmts: List[ASTNode]) -> bool:
        """Conservative analysis: returns True iff all control paths return.
        For a sequence, if any statement returns-always, subsequent are unreachable
        and we still consider it returning."""
        must_return = False
        for st in stmts:
            if self._stmt_returns_always(st):
                must_return = True
                break
        return must_return

    def _stmt_returns_always(self, st: ASTNode) -> bool:
        # Direct return
        if isinstance(st, ReturnStmt):
            return True

        # Block
        if isinstance(st, BlockStmt):
            return self._block_returns_always(self._stmts_from_body(st))

        # If ... (elif ...)* else ...
        if isinstance(st, IfStmt):
            branches = []

            # then
            branches.append(st.then_stmt)

            # elif branches
            for pair in getattr(st, "elif_branches", []) or []:
                if isinstance(pair, (list, tuple)):
                    branches.append(pair[1])
                else:
                    branches.append(getattr(pair, "stmt", None))

            # else
            if getattr(st, "else_stmt", None) is None:
                return False  # no else -> not guaranteed
            branches.append(st.else_stmt)

            # all branches must return
            for b in branches:
                if not self._stmt_returns_always(b if not isinstance(b, list) else BlockStmt(b)):
                    return False
            return True
        return False