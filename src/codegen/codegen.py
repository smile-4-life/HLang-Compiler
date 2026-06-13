"""
Code Generator for HLang programming language.
This module implements a code generator that traverses AST nodes and generates
Java bytecode using the Emitter and Frame classes.
"""

from typing import Any, List, Optional
from ..utils.visitor import ASTVisitor
from ..utils.nodes import *
from .emitter import Emitter
from .frame import Frame
from .error import IllegalOperandException, IllegalRuntimeException
from .io import IO_SYMBOL_LIST
from .utils import *
from functools import reduce
import copy


class CodeGenerator(ASTVisitor):
    def __init__(self):
        self.class_name = "HLang"
        self.emit = Emitter(self.class_name + ".j")

    def _emit_arraylength(self, frame) -> str:
        """Helper for array length since emitter.py might lack it."""
        return "\tarraylength\n"

    def visit_program(self, node: "Program", o: Any = None):
        self.emit.print_out(self.emit.emit_prolog(self.class_name, "java/lang/Object"))
        global_env = SubBody(None, IO_SYMBOL_LIST)

        global_env = reduce(
            lambda acc, cur: self.visit(cur, acc),
            node.const_decls,
            global_env,
        )

        global_env = reduce(
            lambda acc, cur: self.visit(cur, acc),
            node.func_decls,
            global_env,
        )

        self.generate_method(
            FuncDecl("<init>", [], VoidType(), []),
            SubBody(Frame("<init>", VoidType()), []),
        )

        self.emit.emit_epilog()

    def visit_const_decl(self, node: "ConstDecl", o=None):
        const_type = self.visit(node.type_annotation, o) if node.type_annotation else None

        if o is not None and o.frame is None:
            if const_type is None:
                _, const_type = self.visit(node.value, Access(Frame("<clinit>", VoidType()), o.sym))
            self.emit.print_out(
                self.emit.emit_attribute(node.name, const_type, True)
            )
            self.emit.print_out(self.emit.emit_method("<clinit>", FunctionType([], VoidType()), True))
            self.emit.print_out(self.emit.emit_limit_stack(5))
            self.emit.print_out(self.emit.emit_limit_local(1))
            code, _ = self.visit(node.value, Access(Frame("<clinit>", VoidType()), o.sym))
            self.emit.print_out(code)
            self.emit.print_out(self.emit.emit_put_static(f"{self.class_name}/{node.name}", const_type, None))
            self.emit.print_out(self.emit.emit_return(VoidType(), None))
            self.emit.print_out(self.emit.emit_end_method(None))
            symbol = Symbol(node.name, const_type, CName(self.class_name))
            return SubBody(o.frame, [symbol] + o.sym)

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



    def visit_var_decl(self, node: "VarDecl", o: Any = None):
        """Handle variable declarations (global and local) with optional type inference."""
        # Determine variable type, possibly via inference from the initializer.
        var_type = None
        if node.type_annotation:
            var_type = self.visit(node.type_annotation, o)
        # If no explicit type, infer from the value expression.
        if var_type is None:
            # Use a temporary frame for potential global initialization.
            _, var_type = self.visit(node.value, Access(Frame("<clinit>", VoidType()), o.sym if o else []))
        # Global variable handling: when o exists and has no frame (top-level)
        if o is not None and getattr(o, "frame", None) is None:
            # Emit static field declaration.
            self.emit.print_out(self.emit.emit_attribute(node.name, var_type, True))
            # Emit <clinit> method to initialize the static field.
            self.emit.print_out(self.emit.emit_method("<clinit>", FunctionType([], VoidType()), True))
            self.emit.print_out(self.emit.emit_limit_stack(5))
            self.emit.print_out(self.emit.emit_limit_local(1))
            init_code, _ = self.visit(node.value, Access(Frame("<clinit>", VoidType()), o.sym))
            self.emit.print_out(init_code)
            self.emit.print_out(self.emit.emit_put_static(f"{self.class_name}/{node.name}", var_type, None))
            self.emit.print_out(self.emit.emit_return(VoidType(), None))
            self.emit.print_out(self.emit.emit_end_method(None))
            symbol = Symbol(node.name, var_type, CName(self.class_name))
            return SubBody(o.frame, [symbol] + o.sym)
        else:
            idx = o.frame.get_new_index()
            self.emit.print_out(self.emit.emit_var(idx, node.name, var_type, o.frame.get_start_label(), o.frame.get_end_label()))
            init_code, _ = self.visit(node.value, Access(o.frame, o.sym))
            self.emit.print_out(init_code)
            self.emit.print_out(self.emit.emit_write_var(node.name, var_type, idx, o.frame))
            symbol = Symbol(node.name, var_type, Index(idx))
            return SubBody(o.frame, [symbol] + o.sym)

    def generate_method(self, node: "FuncDecl", o: SubBody = None):
        frame = o.frame
        is_init = node.name == "<init>"
        is_main = node.name == "main"

        param_types = list(map(lambda x: x.param_type, node.params))
        if is_main:
            param_types = [ArrayType(StringType(), 0)]
        return_type = node.return_type

        # 1. Phát dòng khai báo phương thức (.method ...)
        method_declaration = self.emit.emit_method(
            node.name, FunctionType(param_types, return_type), not is_init
        )
        self.emit.print_out(method_declaration)

        frame.enter_scope(True)
        from_label = frame.get_start_label()
        to_label = frame.get_end_label()

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

        if is_init:
            self.emit.print_out(
                self.emit.emit_read_var(
                    "this", ClassType(self.class_name), this_idx, frame
                )
            )
            self.emit.print_out(self.emit.emit_invoke_special(frame))

        # Duyệt qua các câu lệnh trong thân hàm
        o = reduce(lambda acc, cur: self.visit(cur, acc), node.body, o)

        if type(return_type) is VoidType:
            self.emit.print_out(self.emit.emit_return(VoidType(), frame))

        self.emit.print_out(self.emit.emit_label(to_label, frame))
        
        # Emit end method directly (includes .limit directives)
        self.emit.print_out(self.emit.emit_end_method(frame))
        
        frame.exit_scope()
        return o

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
    def visit_int_type(self, node: "IntType", o=None): return IntType()
    def visit_float_type(self, node: "FloatType", o=None): return FloatType()
    def visit_bool_type(self, node: "BoolType", o=None): return BoolType()
    def visit_string_type(self, node: "StringType", o=None): return StringType()
    def visit_void_type(self, node: "VoidType", o=None): return VoidType()
    def visit_array_type(self, node: "ArrayType", o=None): return ArrayType(node.element_type, node.size )

    # Statements
    

    def visit_assignment(self, node: "Assignment", o: SubBody = None):
        # Trường hợp 1: Gán phần tử mảng (Array element assignment)
        # Thứ tự bắt buộc trong JVM stack: arrayref -> index -> value -> [i/f/a]astore
        if hasattr(node.lvalue, "array"): 
            arr_code, arr_type = self.visit(node.lvalue.array, Access(o.frame, o.sym))
            idx_code, idx_type = self.visit(node.lvalue.index, Access(o.frame, o.sym))
            
            self.emit.print_out(arr_code) # Nạp địa chỉ mảng gốc (arrayref)
            self.emit.print_out(idx_code) # Nạp chỉ số mảng (index)
            
            rc, rt = self.visit(node.value, Access(o.frame, o.sym))
            elem_type = arr_type.element_type if hasattr(arr_type, 'element_type') else arr_type
            
            # Ép kiểu ngầm định int -> float cho phần tử mảng nếu cần
            if isinstance(elem_type, FloatType) and isinstance(rt, IntType):
                rc += self.emit.emit_i2f(o.frame)
                
            self.emit.print_out(rc) # Nạp giá trị cần gán (value)
            
            # Kiểm tra kiểu của phần tử để phát chỉ thị lưu trữ chính xác của JVM
            self.emit.print_out(self.emit.emit_astore(elem_type, o.frame))

                
        # Trường hợp 2: Gán biến thông thường/Biến tham chiếu mảng (Scalar/Variable assignment)
        # Thứ tự JVM Stack: value -> store
        else:
            rc, rt = self.visit(node.value, Access(o.frame, o.sym))
            
            # Tìm kiếm thông tin ký hiệu (symbol) của vế trái để lấy ô nhớ cục bộ (Index)
            sym = next((s for s in o.sym if s.name == node.lvalue.name), None)
            if sym is None:
                raise IllegalOperandException(f"Undeclared identifier: {node.lvalue.name}")
                
            # Ép kiểu ngầm định int -> float cho biến thường
            if isinstance(sym.type, FloatType) and isinstance(rt, IntType):
                rc += self.emit.emit_i2f(o.frame)
                
            self.emit.print_out(rc) # Nạp giá trị lên đỉnh stack trước
            
            # Sinh mã chỉ thị GHI (STORE) biến đích danh, loại bỏ hoàn toàn việc gọi visit_lvalue bừa bãi
            if isinstance(sym.value, Index):
                write_code = self.emit.emit_write_var(sym.name, sym.type, sym.value.value, o.frame)
                self.emit.print_out(write_code)
            elif isinstance(sym.value, CName):
                write_code = self.emit.emit_put_static(f"{sym.value.value}/{sym.name}", sym.type, o.frame)
                self.emit.print_out(write_code)
                
        return o

    def visit_if_stmt(self, node: "IfStmt", o: SubBody = None):
        frame = o.frame # Lấy frame gốc đang giữ loop labels
        end_label = frame.get_new_label()
        cond_code, cond_type = self.visit(node.condition, Access(frame, o.sym))
        self.emit.print_out(cond_code)
        
        false_label = frame.get_new_label()
        self.emit.print_out(self.emit.emit_if_false(false_label, frame))
        
        # --- SỬA NHÁNH THEN ---
        then_body = node.then_stmt.statements if isinstance(node.then_stmt, BlockStmt) else [node.then_stmt]
        # Chắc chắn rằng SubBody mới được tạo ra sử dụng chung 'frame' gốc của cấu trúc cha
        then_env = SubBody(frame, o.sym) 
        for stmt in then_body:
            res = self.visit(stmt, then_env)
            if isinstance(res, SubBody):
                then_env = res
                
        self.emit.print_out(self.emit.emit_goto(end_label, frame))
        
        if node.elif_branches:
            for cond, block in node.elif_branches:
                self.emit.print_out(self.emit.emit_label(false_label, frame))
                cond_code, cond_type = self.visit(cond, Access(frame, o.sym))
                self.emit.print_out(cond_code)
                false_label2 = frame.get_new_label()
                self.emit.print_out(self.emit.emit_if_false(false_label2, frame))
                
                # --- SỬA NHÁNH ELIF ---
                block_body = block.statements if isinstance(block, BlockStmt) else [block]
                elif_env = SubBody(frame, o.sym) # Sử dụng frame gốc
                for stmt in block_body:
                    res = self.visit(stmt, elif_env)
                    if isinstance(res, SubBody):
                        elif_env = res
                        
                self.emit.print_out(self.emit.emit_goto(end_label, frame))
                false_label = false_label2
                
        if node.else_stmt:
            self.emit.print_out(self.emit.emit_label(false_label, frame))
            
            # --- SỬA NHÁNH ELSE ---
            else_body = node.else_stmt.statements if isinstance(node.else_stmt, BlockStmt) else [node.else_stmt]
            else_env = SubBody(frame, o.sym) # Sử dụng frame gốc
            for stmt in else_body:
                res = self.visit(stmt, else_env)
                if isinstance(res, SubBody):
                    else_env = res
        else:
            self.emit.print_out(self.emit.emit_label(false_label, frame))
            
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        return o

    def visit_while_stmt(self, node: "WhileStmt", o: SubBody = None):
        frame = o.frame
        start_label = frame.get_new_label()
        end_label = frame.get_new_label()

        self.emit.print_out(self.emit.emit_label(start_label, frame))

        cond_code, cond_type = self.visit(node.condition, Access(frame, o.sym))
        self.emit.print_out(cond_code)
        self.emit.print_out(self.emit.emit_if_false(end_label, frame))

        body_env = o
        body_stmts = node.body.statements if isinstance(node.body, BlockStmt) else [node.body]
        for stmt in body_stmts:
            res = self.visit(stmt, body_env)
            if isinstance(res, SubBody):
                body_env = res

        self.emit.print_out(self.emit.emit_goto(start_label, frame))
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        return o

    def visit_for_stmt(self, node: "ForStmt", o: SubBody = None):
        frame = o.frame
        frame.enter_loop()
        start_label = frame.get_continue_label()
        end_label = frame.get_break_label()
        
        arr_code, arr_type = self.visit(node.iterable, Access(frame, o.sym))
        arr_idx = frame.get_new_index()
        idx_idx = frame.get_new_index()

        self.emit.print_out(arr_code)
        # Store array reference into local variable using appropriate store instruction
        self.emit.print_out(self.emit.emit_write_var("arr", arr_type, arr_idx, frame))  # arr local
        self.emit.print_out(self.emit.emit_push_iconst(0, frame))
        self.emit.print_out(self.emit.jvm.emitISTORE(idx_idx))  # i = 0

        elem_type = arr_type.element_type
        loop_var_sym = Symbol(node.variable, elem_type, Index(frame.get_new_index()))
        loop_var_idx = loop_var_sym.value.value

        new_o = SubBody(frame, [loop_var_sym] + o.sym)

        self.emit.print_out(self.emit.emit_label(start_label, frame))
        self.emit.print_out(self.emit.jvm.emitILOAD(idx_idx))
        self.emit.print_out(self.emit.jvm.emitALOAD(arr_idx))
        self.emit.print_out(self._emit_arraylength(frame))
        self.emit.print_out(self.emit.jvm.emitIFICMPGE(end_label))

        # read element from array
        self.emit.print_out(self.emit.emit_read_var("arr", arr_type, arr_idx, frame))
        self.emit.print_out(self.emit.jvm.emitILOAD(idx_idx))
        self.emit.print_out(self.emit.emit_aload(elem_type, frame))

        self.emit.print_out(self.emit.emit_write_var(node.variable, elem_type, loop_var_idx, frame))
        
        # --- ĐOẠN SỬA ĐỂ TÍCH LŨY MÔI TRƯỜNG BIẾN CỤC BỘ ---
        body_stmts = node.body.statements if isinstance(node.body, BlockStmt) else [node.body]
        loop_env = new_o  # Khởi tạo môi trường tích lũy chứa sẵn loop_var
        for stmt in body_stmts:
            res = self.visit(stmt, loop_env)
            if isinstance(res, SubBody):
                loop_env = res  # Lưu lại môi trường mới nếu stmt vừa rồi có khai báo thêm biến (như temp)
        # ----------------------------------------------------

        self.emit.print_out(self.emit.jvm.emitILOAD(idx_idx))
        self.emit.print_out(self.emit.emit_push_iconst(1, o.frame))
        self.emit.print_out(self.emit.jvm.emitIADD())
        self.emit.print_out(self.emit.jvm.emitISTORE(idx_idx))

        self.emit.print_out(self.emit.emit_goto(start_label, frame))
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_loop()
        
        return o

    def visit_return_stmt(self, node: "ReturnStmt", o: SubBody = None):
        frame = o.frame
        if node.value:
            code, typ = self.visit(node.value, Access(frame, o.sym))
            # Handle float promotion
            if isinstance(frame.return_type, FloatType) and isinstance(typ, IntType):
                code += self.emit.emit_i2f(frame)
                typ = FloatType()
            self.emit.print_out(code)
            self.emit.print_out(self.emit.emit_return(typ, frame))
        else:
            self.emit.print_out(self.emit.emit_return(VoidType(), frame))
        return o

    def visit_break_stmt(self, node: "BreakStmt", o: SubBody = None):
        label = getattr(o, "current_break_label", None)
        if label is None:
            label = o.frame.get_break_label()
        return self.emit.emit_goto(label, o.frame)

    def visit_continue_stmt(self, node: "ContinueStmt", o: SubBody = None):
        label = getattr(o, "current_continue_label", None)
        if label is None:
            label = o.frame.get_continue_label()
        return self.emit.emit_goto(label, o.frame)

    def visit_expr_stmt(self, node: "ExprStmt", o: SubBody = None):
        code, typ = self.visit(node.expr, Access(o.frame, o.sym))
        self.emit.print_out(code)
        return o

    def visit_block_stmt(self, node: "BlockStmt", o: SubBody = None):
        # Enter a new lexical block scope. Use the same frame for local variable indices,
        # but create a fresh symbol list so that variables declared inside the block do not
        # leak into the outer scope.
        o.frame.enter_scope(False)
        # Start with an empty symbol list for this block
        block_body = SubBody(o.frame, [])
        for stmt in node.statements:
            block_body = self.visit(stmt, block_body)
        # Exit the block scope; symbols in block_body are discarded
        o.frame.exit_scope()
        # Return the original context (outer SubBody) unchanged
        return o

    # Left-values
    def visit_id_lvalue(self, node: "IdLValue", o: Access = None):
        sym = next(filter(lambda x: x.name == node.name, o.sym), None)
        if sym is None:
            raise IllegalOperandException(f"Undeclared identifier: {node.name}")
        if type(sym.value) is Index:
            return self.emit.emit_write_var(sym.name, sym.type, sym.value.value, o.frame), sym.type
        else:
            raise IllegalOperandException(f"Unsupported identifier: {node.name}")

    def visit_array_access_lvalue(self, node: "ArrayAccessLValue", o: Access = None):
        # Read operations bypass store instructions (handled correctly by visit_assignment)
        arr_code, arr_type = self.visit(node.array, o)
        idx_code, idx_type = self.visit(node.index, o)
        elem_type = arr_type.element_type if isinstance(arr_type, ArrayType) else arr_type
        return arr_code + idx_code, elem_type

    # Expressions
    def visit_binary_op(self, node: "BinaryOp", o: Access = None):
        op = node.operator
        frame = o.frame

        # Pipeline operator
        if op == ">>":
            if not isinstance(node.right, FunctionCall):
                raise IllegalOperandException("Pipeline right must be a function call")
            right_clone = copy.copy(node.right)
            right_clone.args = [node.left] + node.right.args
            return self.visit_function_call(right_clone, o)

        # Short-circuit AND
        if op == "&&":
            left_code, _ = self.visit(node.left, o)
            false_label = frame.get_new_label()
            end_label = frame.get_new_label()
            
            code = left_code + self.emit.emit_if_false(false_label, frame)
            right_code, _ = self.visit(node.right, o)
            
            code += right_code + self.emit.emit_goto(end_label, frame)
            code += self.emit.emit_label(false_label, frame)
            code += self.emit.emit_push_iconst(0, frame)
            code += self.emit.emit_label(end_label, frame)
            return code, BoolType()

        # Short-circuit OR
        if op == "||":
            left_code, _ = self.visit(node.left, o)
            true_label = frame.get_new_label()
            end_label = frame.get_new_label()
            
            code = left_code + self.emit.emit_if_true(true_label, frame)
            right_code, _ = self.visit(node.right, o)
            
            code += right_code + self.emit.emit_goto(end_label, frame)
            code += self.emit.emit_label(true_label, frame)
            code += self.emit.emit_push_iconst(1, frame)
            code += self.emit.emit_label(end_label, frame)
            return code, BoolType()

        # Generate code for left and right operands
        left_code, left_type = self.visit(node.left, o)
        right_code, right_type = self.visit(node.right, o)

        # String operations
        is_left_str = isinstance(left_type, StringType)
        is_right_str = isinstance(right_type, StringType)

        if is_left_str or is_right_str:
            # String concatenation with auto-cast
            if op == "+":
                def to_str_code(t):
                    if isinstance(t, IntType): return self.emit.emit_invoke_static("io/int2str", FunctionType([IntType()], StringType()), frame)
                    if isinstance(t, FloatType): return self.emit.emit_invoke_static("io/float2str", FunctionType([FloatType()], StringType()), frame)
                    if isinstance(t, BoolType): return self.emit.emit_invoke_static("io/bool2str", FunctionType([BoolType()], StringType()), frame)
                    return ""

                left_code += to_str_code(left_type)
                right_code += to_str_code(right_type)
                
                code = left_code + right_code
                code += self.emit.emit_invoke_virtual("java/lang/String/concat", FunctionType([StringType()], StringType()), frame)
                return code, StringType()
            
            # String comparison
            if op in ["==", "!=", "<", "<=", ">", ">="] and is_left_str and is_right_str:
                if op in ["==", "!="]:
                    code = left_code + right_code
                    code += self.emit.emit_invoke_virtual("java/lang/String/equals", FunctionType([ClassType("java/lang/Object")], BoolType()), frame)
                    if op == "!=": 
                        code += self.emit.emit_not(BoolType(), frame)
                else:
                    code = left_code + right_code
                    code += self.emit.emit_invoke_virtual("java/lang/String/compareTo", FunctionType([StringType()], IntType()), frame)
                    code += self.emit.emit_push_iconst(0, frame)
                    code += self.emit.emit_re_op(op, IntType(), frame)
                return code, BoolType()

        # Boolean operations
        if isinstance(left_type, BoolType) and isinstance(right_type, BoolType):
            # Logical AND via '+'
            if op == "+":
                code = left_code + right_code
                code += self.emit.emit_and_op(frame)
                return code, BoolType()
            
            # Boolean comparison (treated as 0 and 1)
            if op in ["==", "!=", "<", "<=", ">", ">="]:
                code = left_code + right_code
                code += self.emit.emit_re_op(op, IntType(), frame)
                return code, BoolType()

        # Numeric operations (Int & Float)
        is_left_num = isinstance(left_type, (IntType, FloatType))
        is_right_num = isinstance(right_type, (IntType, FloatType))

        if is_left_num and is_right_num:
            # Type promotion to Float
            if isinstance(left_type, IntType) and isinstance(right_type, FloatType):
                left_code += self.emit.emit_i2f(frame)
                result_type = FloatType()
            elif isinstance(left_type, FloatType) and isinstance(right_type, IntType):
                right_code += self.emit.emit_i2f(frame)
                result_type = FloatType()
            else:
                result_type = left_type

            code = left_code + right_code

            # Arithmetic operators
            if op in ["+", "-", "*", "/"]:
                if op in ["+", "-"]:
                    code += self.emit.emit_add_op(op, result_type, frame)
                else:
                    code += self.emit.emit_mul_op(op, result_type, frame)
                return code, result_type

            # Relational operators
            if op in ["==", "!=", "<", "<=", ">", ">="]:
                code += self.emit.emit_re_op(op, result_type, frame)
                return code, BoolType()

            # Modulo operator
            if op == "%" and isinstance(result_type, IntType):
                code += self.emit.emit_mod(frame)
                return code, IntType()

        # Invalid operand or type combination
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
        
        if function_name in ["print", "input", "str", "int", "float", "len"]:
            return self.emit_builtin_call(node, o)
        
        function_symbol = next(filter(lambda x: x.name == function_name, o.sym), None)
        if function_symbol is None:
            raise IllegalOperandException(f"Undeclared function: {function_name}")
        
        class_name = function_symbol.value.value
        argument_codes = []
        for argument in node.args:
            ac, at = self.visit(argument, Access(o.frame, o.sym))
            
            # Param matching promotion (simplified logic handling Int -> Float)
            # A mature compiler matches against function_symbol.type.param_types
            argument_codes.append(ac)

        return (
            "".join(argument_codes)
            + self.emit.emit_invoke_static(
                class_name + "/" + function_name, function_symbol.type, o.frame
            ),
            function_symbol.type.return_type,
        )

    def emit_builtin_call(self, node: "FunctionCall", o: Access = None):
        func_name = node.function.name
        code = ""
        arg_types = []
        
        for arg in node.args:
            ac, at = self.visit(arg, Access(o.frame, o.sym))
            code += ac
            arg_types.append(at)
            
        frame = o.frame
        
        if func_name == "print":
            # Ensure argument is a String. Convert Bool, Int, Float to String if needed.
            if len(arg_types) == 1:
                arg_type = arg_types[0]
                if isinstance(arg_type, BoolType):
                    code += self.emit.emit_invoke_static("io/bool2str", FunctionType([BoolType()], StringType()), frame)
                    arg_types[0] = StringType()
                elif isinstance(arg_type, IntType):
                    code += self.emit.emit_invoke_static("io/int2str", FunctionType([IntType()], StringType()), frame)
                    arg_types[0] = StringType()
                elif isinstance(arg_type, FloatType):
                    code += self.emit.emit_invoke_static("io/float2str", FunctionType([FloatType()], StringType()), frame)
                    arg_types[0] = StringType()
            code += self.emit.emit_invoke_static("io/print", FunctionType([StringType()], VoidType()), frame)
            return code, VoidType()
        elif func_name == "input":
            code += self.emit.emit_invoke_static("io/input", FunctionType([], StringType()), frame)
            return code, StringType()
        elif func_name == "str":
            typ = arg_types[0]
            if isinstance(typ, IntType):
                code += self.emit.emit_invoke_static("io/int2str", FunctionType([IntType()], StringType()), frame)
            elif isinstance(typ, BoolType):
                code += self.emit.emit_invoke_static("io/bool2str", FunctionType([BoolType()], StringType()), frame)
            return code, StringType()
        elif func_name == "int":
            code += self.emit.emit_invoke_static("io/str2int", FunctionType([StringType()], IntType()), frame)
            return code, IntType()
        elif func_name == "float":
            code += self.emit.emit_invoke_static("io/str2float", FunctionType([StringType()], FloatType()), frame)
            return code, FloatType()
        elif func_name == "len":
            code += self._emit_arraylength(frame)
            return code, IntType()

    def visit_array_access(self, node: "ArrayAccess", o: Access = None):
        array_code, array_type = self.visit(node.array, o)
        index_code, index_type = self.visit(node.index, o)
        code = array_code + index_code
        element_type = array_type.element_type
        code += self.emit.emit_aload(element_type, o.frame)
        return code, element_type

    def visit_array_literal(self, node, o):
        if not node.elements:
            return "", ArrayType(IntType(), 0)  
        
        first_elem_code, first_elem_type = self.visit(node.elements[0], o)
        elem_typ = first_elem_type
        n = len(node.elements)

        code = []
        code.append(self.emit.emit_push_iconst(n, o.frame))
        
        if isinstance(elem_typ, (IntType, FloatType, BoolType)):
            jvm_type = "int" if isinstance(elem_typ, IntType) else ("float" if isinstance(elem_typ, FloatType) else "boolean")
            code.append(self.emit.emit_new_array(jvm_type))
        else:
            jvm_type = self.emit.get_jvm_type(elem_typ)
            if isinstance(elem_typ, StringType):
                code.append(self.emit.jvm.emitANEWARRAY("java/lang/String"))
            else:
                code.append(self.emit.jvm.emitANEWARRAY(jvm_type))

        for i, el in enumerate(node.elements):
            ec, et = self.visit(el, o)
            if type(et) != type(elem_typ):
                raise IllegalOperandException(f"Array literal elements must have consistent types")
            
            code.append(self.emit.emit_dup(o.frame))
            code.append(self.emit.emit_push_iconst(i, o.frame))
            code.append(ec)
            code.append(self.emit.emit_astore(elem_typ, o.frame))

        return "".join(code), ArrayType(elem_typ, n)

    def visit_identifier(self, node: "Identifier", o: Access = None):
        sym = next((s for s in o.sym if s.name == node.name), None)
        if sym is None:
            raise IllegalOperandException(f"Undeclared identifier: {node.name}")

        if isinstance(sym.value, Index):
            code = self.emit.emit_read_var(sym.name, sym.type, sym.value.value, o.frame)
            return code, sym.type
        elif isinstance(sym.value, CName):
            code = self.emit.emit_get_static(f"{sym.value.value}/{sym.name}", sym.type, o.frame)
            return code, sym.type
        else:
            raise IllegalOperandException(f"Unsupported identifier: {node.name}")

    # Literals
    def visit_integer_literal(self, node: "IntegerLiteral", o: Access = None):
        return self.emit.emit_push_iconst(node.value, o.frame), IntType()
    def visit_float_literal(self, node: "FloatLiteral", o: Access = None):
        return self.emit.emit_push_fconst(str(node.value), o.frame), FloatType()
    def visit_boolean_literal(self, node: "BooleanLiteral", o: Access = None):
        val_str = "true" if node.value else "false"
        return self.emit.emit_push_const(val_str, BoolType(), o.frame), BoolType()
    def visit_string_literal(self, node: "StringLiteral", o: Access = None):
        return self.emit.emit_push_const('"' + node.value + '"', StringType(), o.frame), StringType()