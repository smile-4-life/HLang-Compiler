"""
AST Generation module for HLang programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.HLangVisitor import HLangVisitor
from build.HLangParser import HLangParser
from src.utils.nodes import *


class ASTGeneration(HLangVisitor):
    def visitProgram(self, ctx):
        const_decls = list(map(lambda x: self.visit(x), ctx.constdecl())) if ctx.constdecl() else []
        funcdecls = list(map(lambda x: self.visit(x), ctx.funcdecl())) if ctx.funcdecl() else []
        program = Program(const_decls, funcdecls)

        # Preserve original source-order interleaving of consts and funcs
        ordered = []
        ci, fi = 0, 0
        for child in ctx.getChildren():
            if isinstance(child, HLangParser.ConstdeclContext) and ci < len(const_decls):
                ordered.append(const_decls[ci])
                ci += 1
            elif isinstance(child, HLangParser.FuncdeclContext) and fi < len(funcdecls):
                ordered.append(funcdecls[fi])
                fi += 1
        program.ordered_decls = ordered
        return program

    def visitConstdecl(self, ctx):
        name = ctx.ID().getText()
        type_annotation = self.visit(ctx.type1()) if ctx.type1() else None
        value = self.visit(ctx.expr())
        return ConstDecl(name, type_annotation, value)

    def visitFuncdecl(self, ctx):
        name = ctx.ID().getText()
        params = self.visit(ctx.parameterList()) if ctx.parameterList() else []
        return_type = self.visit(ctx.type1())
        body = self.visit(ctx.body())
        return FuncDecl(name, params, return_type, body)

    def visitParameterList(self, ctx):
        return [self.visit(x) for x in ctx.parameter()]

    def visitParameter(self, ctx):
        name = ctx.ID().getText()
        param_type = self.visit(ctx.type1())
        return Param(name, param_type)

    def visitType1(self, ctx):
        return self.visit(ctx.getChild(0))

    def visitPrimitiveType(self, ctx):
        if ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.BOOL():
            return BoolType()
        elif ctx.STRING():
            return StringType()
        elif ctx.VOID():
            return VoidType()
        else:
            raise ValueError(f"Unknown primitive type: {ctx.getText()}")

    def visitArrayType(self, ctx):
        element_type = self.visit(ctx.type1())
        size = int(ctx.INT_LIT().getText())
        return ArrayType(element_type, size)

    def visitBody(self, ctx):
        return list(map(lambda x: self.visit(x), ctx.statement()))

    def visitStatement(self, ctx):
        return self.visit(ctx.getChild(0))

    def visitExpression_stmt(self, ctx):
        return ExprStmt(self.visit(ctx.expr()))

    def visitVardecl_stmt(self, ctx):
        name = ctx.ID().getText()
        type_annotation = self.visit(ctx.type1()) if ctx.type1() else None
        value = self.visit(ctx.expr())
        return VarDecl(name, type_annotation, value)

    def visitAssignment_stmt(self, ctx):
        if not ctx.expr8().expr():
            prim = ctx.expr8().primary_expression()
            lvalue = IdLValue(prim.ID().getText() if prim.ID() else prim.getText())
        else:
            lst = ctx.expr8().expr()
            base = self.visit(ctx.expr8().primary_expression())
            for expr in lst[:-1]:
                base = ArrayAccess(base, self.visit(expr))
            lvalue = ArrayAccessLValue(base, self.visit(lst[-1]))
        return Assignment(lvalue, self.visit(ctx.expr()))

    def visitConditional_stmt(self, ctx):
        conditions = [self.visit(expr) for expr in ctx.expr()]
        blocks = [self.visit(block) for block in ctx.statement_block()]

        elif_branches = []
        if len(conditions) > 1:
            elif_conditions = conditions[1:]
            elif_blocks = blocks[1:-1] if len(ctx.IF()) == len(ctx.ELSE()) else blocks[1:]
            elif_branches = list(zip(elif_conditions, elif_blocks))
        else_block = blocks[-1] if len(ctx.IF()) == len(ctx.ELSE()) else None

        return IfStmt(
            condition=conditions[0],
            then_stmt=blocks[0],
            elif_branches=elif_branches,
            else_stmt=else_block
        )

    def visitLoop_stmt(self, ctx):
        if ctx.WHILE():
            condition = self.visit(ctx.expr())
            body = self.visit(ctx.statement_block())
            return WhileStmt(condition, body)
        else:  # FOR
            variable = ctx.ID().getText()
            condition = self.visit(ctx.expr())
            body = self.visit(ctx.statement_block())
            return ForStmt(variable, condition, body)

    def visitStatement_block(self, ctx):
        statements = list(map(lambda x: self.visit(x), ctx.statement())) if ctx.statement() else []
        return BlockStmt(statements)

    def visitControlflow_stmt(self, ctx):
        if ctx.BREAK():
            return BreakStmt()
        elif ctx.CONTINUE():
            return ContinueStmt()
        else:  # RETURN
            value = self.visit(ctx.expr()) if ctx.expr() else None
            return ReturnStmt(value)

    def visitBlock_stmt(self, ctx):
        statements = list(map(lambda x: self.visit(x), ctx.statement())) if ctx.statement() else []
        return BlockStmt(statements)

    def visitExpr(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr1(0))
        exprs = [self.visit(e) for e in ctx.expr1()]
        operators = [op.getText() for op in ctx.PIPE_LINE()]
        return reduce(
            lambda left, pair: BinaryOp(left, pair[0], pair[1]),
            zip(operators, exprs[1:]),
            exprs[0]
        )

    def visitExpr1(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr2(0))
        exprs = [self.visit(e) for e in ctx.expr2()]
        operators = [op.getText() for op in ctx.OR()]
        return reduce(
            lambda left, pair: BinaryOp(left, pair[0], pair[1]),
            zip(operators, exprs[1:]),
            exprs[0]
        )

    def visitExpr2(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr3(0))
        exprs = [self.visit(e) for e in ctx.expr3()]
        operators = [op.getText() for op in ctx.AND()]
        return reduce(
            lambda left, pair: BinaryOp(left, pair[0], pair[1]),
            zip(operators, exprs[1:]),
            exprs[0]
        )

    def visitExpr3(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr4(0))
        exprs = [self.visit(e) for e in ctx.expr4()]
        operators = [ctx.getChild(i * 2 + 1).getText() for i in range(len(exprs) - 1)]
        return reduce(
            lambda left, pair: BinaryOp(left, pair[0], pair[1]),
            zip(operators, exprs[1:]),
            exprs[0]
        )

    def visitExpr4(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr5(0))
        exprs = [self.visit(e) for e in ctx.expr5()]
        operators = [ctx.getChild(i * 2 + 1).getText() for i in range(len(exprs) - 1)]
        return reduce(
            lambda left, pair: BinaryOp(left, pair[0], pair[1]),
            zip(operators, exprs[1:]),
            exprs[0]
        )

    def visitExpr5(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr6(0))
        exprs = [self.visit(e) for e in ctx.expr6()]
        operators = [ctx.getChild(i * 2 + 1).getText() for i in range(len(exprs) - 1)]
        return reduce(
            lambda left, pair: BinaryOp(left, pair[0], pair[1]),
            zip(operators, exprs[1:]),
            exprs[0]
        )

    def visitExpr6(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr7(0))
        exprs = [self.visit(e) for e in ctx.expr7()]
        operators = [ctx.getChild(i * 2 + 1).getText() for i in range(len(exprs) - 1)]
        return reduce(
            lambda left, pair: BinaryOp(left, pair[0], pair[1]),
            zip(operators, exprs[1:]),
            exprs[0]
        )

    def visitExpr7(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr8())
        operand = self.visit(ctx.expr8())
        operators = [child.getText() for child in list(ctx.getChildren())[:-1]]
        for op in reversed(operators):
            operand = UnaryOp(op, operand)
        return operand

    def visitExpr8(self, ctx):
        base = self.visit(ctx.primary_expression())
        if not ctx.expr():
            return base
        return reduce(
            lambda acc, expr: ArrayAccess(acc, self.visit(expr)),
            ctx.expr(),
            base
        )

    def visitPrimary_expression(self, ctx):
        if ctx.getChildCount() == 3:          # LPAREN expr RPAREN
            return self.visit(ctx.expr())
        elif ctx.ID():                         # bare identifier
            return Identifier(ctx.ID().getText())
        else:                                  # literal or func_call
            return self.visit(ctx.getChild(0))

    def visitLiteral(self, ctx):
        if ctx.INT_LIT():
            return IntegerLiteral(int(ctx.INT_LIT().getText()))
        elif ctx.FLOAT_LIT():
            return FloatLiteral(float(ctx.FLOAT_LIT().getText()))
        elif ctx.STRING_LIT():
            return StringLiteral(ctx.STRING_LIT().getText())
        elif ctx.bool_lit():
            return self.visit(ctx.bool_lit())
        elif ctx.array_lit():
            return self.visit(ctx.array_lit())

    def visitBool_lit(self, ctx):
        return BooleanLiteral(ctx.TRUE() is not None)

    def visitArray_lit(self, ctx):
        elements = list(map(lambda x: self.visit(x), ctx.expr()))
        return ArrayLiteral(elements)

    def visitFunc_call(self, ctx):
        function = Identifier(ctx.ID().getText())
        args = list(map(lambda x: self.visit(x), ctx.argument_list().expr())) if ctx.argument_list() else []
        return FunctionCall(function, args)