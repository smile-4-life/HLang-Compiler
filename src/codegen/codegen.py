"""
Code Generator for HLang programming language.
This module implements a code generator that traverses AST nodes and generates
Java bytecode using the Emitter and Frame classes.
"""

from ast import Sub
from typing import Any, List, Optional
from ..utils.visitor import ASTVisitor
from ..utils.nodes import *
from .emitter import Emitter
from .frame import Frame
from .error import IllegalOperandException, IllegalRuntimeException
from .io import IO_SYMBOL_LIST
from .utils import *
from functools import *


class CodeGenerator(ASTVisitor):
    def __init__(self):
        self.class_name = "HLang"
        self.emit = Emitter(self.class_name + ".j")

    def visit_program(self, node: "Program", o: Any = None):
        # Emit phần prolog cho class
        self.emit.print_out(self.emit.emit_prolog(self.class_name, "java/lang/Object"))

        # Tạo global environment (frame=None vì global scope không có stack frame)
        global_env = SubBody(None, IO_SYMBOL_LIST)

        # Duyệt qua global constants
        global_env = reduce(
            lambda acc, cur: self.visit(cur, acc),
            node.const_decls,
            global_env,
        )

        # Duyệt qua global functions
        global_env = reduce(
            lambda acc, cur: self.visit(cur, acc),
            node.func_decls,
            global_env,
        )

        # Generate default constructor <init>
        self.generate_method(
            FuncDecl("<init>", [], VoidType(), []),
            SubBody(Frame("<init>", VoidType()), []),
        )

        # Emit epilog
        self.emit.emit_epilog()


    def visit_const_decl(self, node: "ConstDecl", o=None):
        # Xác định kiểu const
        const_type = self.visit(node.type_annotation, o) if node.type_annotation else None

        # Nếu ở global scope (o.frame is None): tạo field static final và khởi tạo trong <clinit>
        if o is not None and o.frame is None:
            # Suy luận kiểu nếu chưa có
            if const_type is None:
                _, const_type = self.visit(node.value, Access(None, o.sym))
            # Tạo field static final
            self.emit.print_out(
                self.emit.emit_attribute(node.name, const_type, True)
            )
            # Sinh mã khởi tạo trong <clinit>
            self.emit.print_out(self.emit.emit_method("<clinit>", FunctionType([], VoidType()), True))
            self.emit.print_out(self.emit.emit_limit_stack(2))
            self.emit.print_out(self.emit.emit_limit_local(1))
            code, _ = self.visit(node.value, Access(None, o.sym))
            self.emit.print_out(code)
            self.emit.print_out(self.emit.emit_put_static(f"{self.class_name}/{node.name}", const_type, None))
            self.emit.print_out(self.emit.emit_return(VoidType(), None))
            self.emit.print_out(self.emit.emit_end_method(None))
            symbol = Symbol(node.name, const_type, CName(self.class_name))
            return SubBody(o.frame, [symbol] + o.sym)

        # Nếu là const cục bộ (trong hàm)
        else:
            idx = o.frame.get_new_index()
            if const_type is None:
                _, const_type = self.visit(node.value, Access(o.frame, o.sym))
            self.emit.print_out(
                self.emit.emit_var(
                    idx,
                    node.name,
                    const_type,
                    o.frame.get_start_label(),
                    o.frame.get_end_label(),
                )
            )
            code, _ = self.visit(node.value, Access(o.frame, o.sym))
            self.emit.print_out(code)
            self.emit.print_out(
                self.emit.emit_write_var(node.name, const_type, idx, o.frame)
            )
            symbol = Symbol(node.name, const_type, Index(idx))
            return SubBody(o.frame, [symbol] + o.sym)


    def generate_method(self, node: "FuncDecl", o: SubBody = None):
        frame = o.frame

        is_init = node.name == "<init>"
        is_main = node.name == "main"

        param_types = list(map(lambda x: x.param_type, node.params))
        if is_main:
            param_types = [ArrayType(StringType(), 0)]
        return_type = node.return_type

        self.emit.print_out(
            self.emit.emit_method(
                node.name, FunctionType(param_types, return_type), not is_init
            )
        )

        frame.enter_scope(True)

        from_label = frame.get_start_label()
        to_label = frame.get_end_label()

        # Generate code for parameters
        if is_init:
            this_idx = frame.get_new_index()

            self.emit.print_out(
                self.emit.emit_var(
                    this_idx, "this", ClassType(self.class_name), from_label, to_label
                )
            )
        elif is_main:
            args_idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(
                    args_idx, "args", ArrayType(StringType(), 0), from_label, to_label
                )
            )
        else:
            o = reduce(lambda acc, cur: self.visit(cur, acc), node.params, o)

        self.emit.print_out(self.emit.emit_label(from_label, frame))

        # Generate code for body

        if is_init:
            self.emit.print_out(
                self.emit.emit_read_var(
                    "this", ClassType(self.class_name), this_idx, frame
                )
            )
            self.emit.print_out(self.emit.emit_invoke_special(frame))

        o = reduce(lambda acc, cur: self.visit(cur, acc), node.body, o)

        if type(return_type) is VoidType:
            self.emit.print_out(self.emit.emit_return(VoidType(), frame))

        self.emit.print_out(self.emit.emit_label(to_label, frame))

        self.emit.print_out(self.emit.emit_end_method(frame))

        frame.exit_scope()

    def visit_func_decl(self, node: "FuncDecl", o: SubBody = None):
        frame = Frame(node.name, node.return_type)
        self.generate_method(node, SubBody(frame, o.sym))
        param_types = list(map(lambda x: x.param_type, node.params))
        return SubBody(
            None,
            [
                Symbol(
                    node.name,
                    FunctionType(param_types, node.return_type),
                    CName(self.class_name),
                )
            ]
            + o.sym,
        )

    def visit_param(self, node: "Param", o: Any = None):
        idx = o.frame.get_new_index()
        self.emit.print_out(
            self.emit.emit_var(
                idx,
                node.name,
                node.param_type,
                o.frame.get_start_label(),
                o.frame.get_end_label(),
            )
        )

        return SubBody(
            o.frame,
            [Symbol(node.name, node.param_type, Index(idx))] + o.sym,
        )

    # Type system

    def visit_int_type(self, node: "IntType", o=None):
        return IntType()

    def visit_float_type(self, node: "FloatType", o=None):
        return FloatType()

    def visit_bool_type(self, node: "BoolType", o=None):
        return BoolType()

    def visit_string_type(self, node: "StringType", o=None):
        return StringType()

    def visit_void_type(self, node: "VoidType", o=None):
        return VoidType()

    def visit_array_type(self, node: "ArrayType", o=None):
        return ArrayType(node.element_type)

    # Statements

    def visit_var_decl(self, node: "VarDecl", o: SubBody = None):
        idx = o.frame.get_new_index()
        self.emit.print_out(
            self.emit.emit_var(
                idx,
                node.name,
                node.type_annotation,
                o.frame.get_start_label(),
                o.frame.get_end_label(),
            )
        )
        # Thêm symbol vào context trước khi khởi tạo giá trị
        new_sym = Symbol(node.name, node.type_annotation, Index(idx))
        new_o = SubBody(o.frame, [new_sym] + o.sym)
        if node.value is not None:
            # Nếu là array literal thì xử lý đặc biệt
            if isinstance(node.value, ArrayLiteral):
                code, _ = self.visit(node.value, Access(o.frame, new_o.sym))
                self.emit.print_out(
                    code +
                    self.emit.emit_write_var(node.name, node.type_annotation, idx, o.frame)
                )
            else:
                # Các kiểu khác vẫn dùng assignment như cũ
                self.visit(
                    Assignment(IdLValue(node.name), node.value),
                    new_o,
                )
        return new_o

    def visit_assignment(self, node: "Assignment", o: SubBody = None):
        rc, rt = self.visit(node.value, Access(o.frame, o.sym))
        self.emit.print_out(rc)
        lc, lt = self.visit(node.lvalue, Access(o.frame, o.sym))
        self.emit.print_out(lc)
        return o

    def visit_if_stmt(self, node: "IfStmt", o: SubBody = None):
        frame = o.frame
        end_label = frame.get_new_label()
        cond_code, cond_type = self.visit(node.condition, Access(frame, o.sym))
        self.emit.print_out(cond_code)
        false_label = frame.get_new_label()
        self.emit.print_out(self.emit.emit_if_false(false_label, frame))
        # then block
        then_body = node.then_stmt.statements if isinstance(node.then_stmt, BlockStmt) else [node.then_stmt]
        for stmt in then_body:
            self.visit(stmt, o)
        self.emit.print_out(self.emit.emit_goto(end_label, frame))
        # elif branches
        if node.elif_branches:
            for cond, block in node.elif_branches:
                self.emit.print_out(self.emit.emit_label(false_label, frame))
                cond_code, cond_type = self.visit(cond, Access(frame, o.sym))
                self.emit.print_out(cond_code)
                false_label2 = frame.get_new_label()
                self.emit.print_out(self.emit.emit_if_false(false_label2, frame))
                block_body = block.statements if isinstance(block, BlockStmt) else [block]
                for stmt in block_body:
                    self.visit(stmt, o)
                self.emit.print_out(self.emit.emit_goto(end_label, frame))
                false_label = false_label2
        # else block
        if node.else_stmt:
            self.emit.print_out(self.emit.emit_label(false_label, frame))
            else_body = node.else_stmt.statements if isinstance(node.else_stmt, BlockStmt) else [node.else_stmt]
            for stmt in else_body:
                self.visit(stmt, o)
        else:
            self.emit.print_out(self.emit.emit_label(false_label, frame))
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        return o

    def visit_while_stmt(self, node: "WhileStmt", o: SubBody = None):
        frame = o.frame
        frame.enter_loop()
        start_label = frame.get_continue_label()
        end_label = frame.get_break_label()
        self.emit.print_out(self.emit.emit_label(start_label, frame))
        cond_code, cond_type = self.visit(node.condition, Access(frame, o.sym))
        self.emit.print_out(cond_code)
        self.emit.print_out(self.emit.emit_if_false(end_label, frame))
        for stmt in node.body.statements:
            self.visit(stmt, o)
        self.emit.print_out(self.emit.emit_goto(start_label, frame))
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_loop()
        return o

    def visit_for_stmt(self, node: "ForStmt", o: SubBody = None):
        frame = o.frame
        frame.enter_loop()
        start_label = frame.get_continue_label()
        end_label = frame.get_break_label()

        arr_code, arr_type = self.visit(node.iterable, Access(frame, o.sym))
        arr_idx = frame.get_new_index()
        idx_idx = frame.get_new_index()
        n = arr_type.size if hasattr(arr_type, "size") else 0

        self.emit.print_out(arr_code)
        self.emit.print_out(self.emit.emit_astore(arr_idx, frame))  # arr local
        self.emit.print_out(self.emit.emit_push_iconst(0, frame))
        self.emit.print_out(self.emit.emit_istore(idx_idx, frame))  # i = 0

        # Tạo symbol cho biến lặp
        elem_type = arr_type.element_type
        loop_var_sym = Symbol(node.var, elem_type, Index(frame.get_new_index()))
        loop_var_idx = loop_var_sym.value.value

        # Gán context mới
        new_o = SubBody(frame, [loop_var_sym] + o.sym)

        self.emit.print_out(self.emit.emit_label(start_label, frame))
        # while (i < arr.length)
        self.emit.print_out(self.emit.emit_iload(idx_idx, frame))
        self.emit.print_out(self.emit.emit_aload(arr_idx, frame))
        self.emit.print_out(self.emit.emit_arraylength(frame))
        self.emit.print_out(self.emit.emit_if_false(end_label, frame))  # if i >= arr.length goto end

        # Gán biến lặp: var = arr[i]
        self.emit.print_out(self.emit.emit_aload(arr_idx, frame))
        self.emit.print_out(self.emit.emit_iload(idx_idx, frame))
        self.emit.print_out(self.emit.emit_aload(elem_type, frame))
        self.emit.print_out(self.emit.emit_store(loop_var_idx, elem_type, frame))

        # Thân vòng lặp
        for stmt in node.body.statements:
            self.visit(stmt, new_o)

        # i = i + 1
        self.emit.print_out(self.emit.emit_iload(idx_idx, frame))
        self.emit.print_out(self.emit.emit_push_iconst(1, frame))
        self.emit.print_out(self.emit.emit_iadd(frame))
        self.emit.print_out(self.emit.emit_istore(idx_idx, frame))

        self.emit.print_out(self.emit.emit_goto(start_label, frame))
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_loop()
        return o

    def visit_return_stmt(self, node: "ReturnStmt", o: SubBody = None):
        frame = o.frame
        if node.value:
            code, typ = self.visit(node.value, Access(frame, o.sym))
            self.emit.print_out(code)
            self.emit.print_out(self.emit.emit_return(typ, frame))
        else:
            self.emit.print_out(self.emit.emit_return(VoidType(), frame))
        return o

    def visit_break_stmt(self, node: "BreakStmt", o: SubBody = None):
        frame = o.frame
        self.emit.print_out(self.emit.emit_goto(frame.get_break_label(), frame))
        return o

    def visit_continue_stmt(self, node: "ContinueStmt", o: SubBody = None):
        frame = o.frame
        self.emit.print_out(self.emit.emit_goto(frame.get_continue_label(), frame))
        return o

    def visit_expr_stmt(self, node: "ExprStmt", o: SubBody = None):
        code, typ = self.visit(node.expr, Access(o.frame, o.sym))
        self.emit.print_out(code)
        return o

    def visit_block_stmt(self, node: "BlockStmt", o: SubBody = None):
        frame = o.frame
        frame.enter_scope(False)
        
        current_context = o
        
        for stmt in node.statements:
            current_context = self.visit(stmt, current_context)
        
        frame.exit_scope()
        return current_context
    # Left-values

    def visit_id_lvalue(self, node: "IdLValue", o: Access = None):
        sym = next(
            filter(lambda x: x.name == node.name, o.sym),
            None,
        )
        if sym is None:
            raise IllegalOperandException(f"Undeclared identifier: {node.name}")
        if type(sym.value) is Index:
            code = self.emit.emit_write_var(
                sym.name, sym.type, sym.value.value, o.frame
            )
            return code, sym.type
        else:
            raise IllegalOperandException(f"Unsupported identifier: {node.name}")
    # Expressions

    def visit_array_access_lvalue(self, node: "ArrayAccessLValue", o: Access = None):
        arr_code, arr_type = self.visit(node.array, o)
        idx_code, idx_type = self.visit(node.index, o)
        elem_type = arr_type.element_type if isinstance(arr_type, ArrayType) else arr_type
        code = arr_code + idx_code
        store_code = self.emit.emit_astore(elem_type, o.frame)
        return code + store_code, elem_type


    def visit_binary_op(self, node: "BinaryOp", o: Access = None):
        left_code, left_type = self.visit(node.left, o)
        right_code, right_type = self.visit(node.right, o)
        op = node.operator
        
        # Type promotion: if one operand is float, promote both to float
        result_type = left_type
        if (isinstance(left_type, IntType) and isinstance(right_type, FloatType)):
            left_code += self.emit.emit_i2f(o.frame)
            result_type = FloatType()
        elif (isinstance(left_type, FloatType) and isinstance(right_type, IntType)):
            right_code += self.emit.emit_i2f(o.frame)
            result_type = FloatType()
        
        code = left_code + right_code
        frame = o.frame

        # String concatenation
        if op == "+" and type(left_type) is StringType and type(right_type) is StringType:
            code += self.emit.emit_invoke_virtual(
                "java/lang/String/concat",
                FunctionType([StringType()], StringType()),
                frame
            )
            return code, StringType()

        # String comparison (==, !=, <, <=, >, >=)
        if op in ["==", "!=", "<", "<=", ">", ">="] and isinstance(left_type, StringType) and isinstance(right_type, StringType):
            if op in ["<", "<=", ">", ">="]:
                # compareTo returns int: <0, ==0, >0
                code += self.emit.emit_invoke_virtual(
                    "java/lang/String/compareTo",
                    FunctionType([StringType()], IntType()),
                    frame
                )
                # So sánh với 0
                code += self.emit.emit_push_iconst(0, frame)
                code += self.emit.emit_re_op(op, IntType(), frame)
                return code, BoolType()
            else:
                # ==, !=: use equals
                code += self.emit.emit_invoke_virtual(
                    "java/lang/String/equals",
                    FunctionType([ClassType("java/lang/Object")], BoolType()),
                    frame
                )
                if op == "!=":
                    code += self.emit.emit_not(BoolType(), frame)
                return code, BoolType()

            
            
        if op in ["+", "-", "*", "/"]:
            if isinstance(result_type, IntType):
                if op == "+": code += self.emit.emit_add_op("+", IntType(), frame)
                elif op == "-": code += self.emit.emit_add_op("-", IntType(), frame)
                elif op == "*": code += self.emit.emit_mul_op("*", IntType(), frame)
                elif op == "/": code += self.emit.emit_mul_op("/", IntType(), frame)
            elif isinstance(result_type, FloatType):
                if op == "+": code += self.emit.emit_add_op("+", FloatType(), frame)
                elif op == "-": code += self.emit.emit_add_op("-", FloatType(), frame)
                elif op == "*": code += self.emit.emit_mul_op("*", FloatType(), frame)
                elif op == "/": code += self.emit.emit_mul_op("/", FloatType(), frame)
            return code, result_type
            # Float arithmetic (not fully implemented)
        # Logical
        elif op == "&&":
            code += self.emit.emit_and_op(frame)
            return code, BoolType()
        elif op == "||":
            code += self.emit.emit_or_op(frame)
            return code, BoolType()
        # Comparison
        elif op in ["==", "!=", "<", "<=", ">", ">="]:
            code += self.emit.emit_re_op(op, left_type, frame)
            return code, BoolType()
        # Modulo
        elif op == "%":
            code += self.emit.emit_mod(frame)
            return code, IntType()
        # Pipeline
        elif op == ">>":
            # For pipeline, treat as function call: left >> right
            # right must be a function call node
            if isinstance(node.right, FunctionCall):
                # Insert left as first argument
                node.right.args = [node.left] + node.right.args
                return self.visit_function_call(node.right, o)
            else:
                raise IllegalOperandException("Pipeline right must be function call")
        else:
            raise IllegalOperandException(op)

    def visit_unary_op(self, node: "UnaryOp", o: Access = None):
        operand_code, operand_type = self.visit(node.operand, o)
        op = node.operator
        frame = o.frame
        code = operand_code
        if op == "-":
            code += self.emit.emit_neg_op(operand_type, frame)
            return code, operand_type
        elif op == "!":
            code += self.emit.emit_not(BoolType(), frame)
            return code, BoolType()
        elif op == "+":
            return code, operand_type
        else:
            raise IllegalOperandException(op)

    def visit_function_call(self, node: "FunctionCall", o: Access = None):
        function_name = node.function.name
        
        # Handle built-in functions first
        if function_name in ["print", "input", "int2str", "str2int", "float2str", "str2float", "bool2str"]:
            return self.emit_builtin_call(node, o)
        
        # Handle user-defined functions
        function_symbol = next(filter(lambda x: x.name == function_name, o.sym), None)
        if function_symbol is None:
            raise IllegalOperandException(f"Undeclared function: {function_name}")
        
        class_name = function_symbol.value.value
        argument_codes = []
        for argument in node.args:
            ac, at = self.visit(argument, Access(o.frame, o.sym))
            argument_codes.append(ac)

        return (
            "".join(argument_codes)
            + self.emit.emit_invoke_static(
                class_name + "/" + function_name, function_symbol.type, o.frame
            ),
            function_symbol.type.return_type,  # Return actual return type
        )

    def emit_builtin_call(self, node: "FunctionCall", o: Access = None):
        func_name = node.function.name
        args_code = []
        arg_types = []
        
        for arg in node.args:
            code, typ = self.visit(arg, o)
            args_code.append(code)
            arg_types.append(typ)
        
        self.emit.print_out(''.join(args_code))
        
        if func_name == "print":
            # print(string): void
            return self.emit.emit_invoke_static(
                "io/print",
                FunctionType([StringType()], VoidType()),
                o.frame
            ), VoidType()

        elif func_name == "input":
            # input(): string
            return self.emit.emit_invoke_static(
                "io/input",
                FunctionType([], StringType()),
                o.frame
            ), StringType()

        elif func_name == "int2str":
            return self.emit.emit_invoke_static(
                "io/int2str",
                FunctionType([IntType()], StringType()),
                o.frame
            ), StringType()

        elif func_name == "str2int":
            return self.emit.emit_invoke_static(
                "io/str2int",
                FunctionType([StringType()], IntType()),
                o.frame
            ), IntType()

        elif func_name == "float2str":
            return self.emit.emit_invoke_static(
                "io/float2str",
                FunctionType([FloatType()], StringType()),
                o.frame
            ), StringType()

        elif func_name == "str2float":
            return self.emit.emit_invoke_static(
                "io/str2float",
                FunctionType([StringType()], FloatType()),
                o.frame
            ), FloatType()

        elif func_name == "bool2str":
            return self.emit.emit_invoke_static(
                "io/bool2str",
                FunctionType([BoolType()], StringType()),
                o.frame
            ), StringType()
        
    def visit_array_access(self, node: "ArrayAccess", o: Access = None):
        array_code, array_type = self.visit(node.array, o)
        index_code, index_type = self.visit(node.index, o)
        code = array_code + index_code
        element_type = array_type.element_type
        code += self.emit.emit_aload(element_type, o.frame)
        return code, element_type

    def visit_array_literal(self, node, o):
        if not node.elements:
            # Empty array - need context to determine type
            return "", ArrayType(IntType(), 0)  # Default to IntType for empty arrays
        
        # Determine element type from first element
        first_elem_code, first_elem_type = self.visit(node.elements[0], o)
        elem_typ = first_elem_type
        n = len(node.elements)

        code = []
        code.append(self.emit.emit_push_iconst(n, o.frame))
        code.append(self.emit.emit_new_array(self.emit.get_jvm_type(elem_typ)))

        for i, el in enumerate(node.elements):
            ec, et = self.visit(el, o)
            # Verify all elements have the same type
            if type(et) != type(elem_typ):
                raise IllegalOperandException(f"Array literal elements must have consistent types, found {type(elem_typ)} and {type(et)}")
            
            code.append(self.emit.emit_dup(o.frame))
            code.append(self.emit.emit_push_iconst(i, o.frame))
            code.append(ec)
            code.append(self.emit.emit_astore(elem_typ, o.frame))

        return "".join(code), ArrayType(elem_typ, n)



    def visit_identifier(self, node: "Identifier", o: Access = None):
        # Tìm symbol trong scope hiện tại
        sym = next((s for s in o.sym if s.name == node.name), None)
        if sym is None:
            raise IllegalOperandException(f"Undeclared identifier: {node.name}")

        # Local variable/const → Index
        if isinstance(sym.value, Index):
            code = self.emit.emit_read_var(sym.name, sym.type, sym.value.value, o.frame)
            return code, sym.type

        # Global const / function → CName
        elif isinstance(sym.value, CName):
            code = self.emit.emit_get_static(f"{sym.value.value}/{sym.name}", sym.type, o.frame)
            return code, sym.type

        else:
            raise IllegalOperandException(f"Unsupported identifier: {node.name}")


        
    # Literals

    def visit_integer_literal(self, node: "IntegerLiteral", o: Access = None):
        return self.emit.emit_push_iconst(node.value, o.frame), IntType()

    def visit_float_literal(self, node: "FloatLiteral", o: Access = None):
        code = self.emit.emit_push_fconst(node.value, o.frame)
        return code, FloatType()

    def visit_boolean_literal(self, node: "BooleanLiteral", o: Access = None):
        code = self.emit.emit_push_iconst(1 if node.value else 0, o.frame)
        return code, BoolType()
    
    def visit_string_literal(self, node: "StringLiteral", o: Any = None):
        return (
            self.emit.emit_push_const('"' + node.value + '"', StringType(), o.frame),
            StringType(),
        )
