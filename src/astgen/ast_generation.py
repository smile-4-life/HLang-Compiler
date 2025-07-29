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
    def visitProgram(self,ctx): 
        const_decls = list(map(lambda x: self.visit(x), ctx.constdecl())) if ctx.constdecl() else []
        funcdecls = list(map(lambda x: self.visit(x), ctx.funcdecl())) if ctx.funcdecl() else []
        return Program(const_decls,funcdecls)

    def visitConstdecl(self,ctx):
        name = ctx.ID().getText()
        type_annotation = self.visit(ctx.type1()) if ctx.type1() else None
        value = self.visit(ctx.expr())
        return ConstDecl(name,type_annotation,value)
    
    def visitFuncdecl(self,ctx):
        name = ctx.ID().getText()
        params = self.visit(ctx.parameterList()) if ctx.parameterList() else []
        return_type = self.visit(ctx.type1())
        body = self.visit(ctx.body())
        return FuncDecl(name,params,return_type,body)

    def visitParameterList(self, ctx):
        return list(map(lambda x: self.visit(x), ctx.parameter()))
    
    def visitParameter(self, ctx):
        name = ctx.ID().getText()
        param_type = self.visit(ctx.type1())
        return Param(name,param_type)

    def visitType1(self,ctx):   
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
        
    def visitArrayType(self, ctx):
        if ctx.arrayType(): 
            element_type = self.visit(ctx.arrayType())
        else:  
            element_type = self.visit(ctx.type1())
        
        size = int(ctx.INT_LIT().getText())
        return ArrayType(element_type, size)
    
    def visitUserDefinedType(self, ctx):
        return Identifier(ctx.ID().getText())
    
    def visitBody(self, ctx):
        return list(map(lambda x: self.visit(x), ctx.statement()))
    
    def visitStatement(self, ctx):
        return self.visit(ctx.getChild(0))
    
    def visitExpression_stmt(self, ctx):
        expr = self.visit(ctx.expr())
        return ExprStmt(expr)
    
    def visitVardecl_stmt(self, ctx):
        name = ctx.ID().getText()
        type_annotation = self.visit(ctx.type1()) if ctx.type1() else None
        value = self.visit(ctx.expr())
        return VarDecl(name,type_annotation,value)
        
    def visitAssignment_stmt(self, ctx):
        lvalue = None
        if not ctx.expr8().expr():
            lvalue = IdLValue(ctx.expr8().primary_expression().identifier().ID().getText())
        else:
            lst = ctx.expr8().expr()
            base = self.visit(ctx.expr8().primary_expression())
            for expr in lst[:-1]:
                base = ArrayAccess(base, self.visit(expr))
            lvalue = ArrayAccessLValue(base, self.visit(lst[-1]))
        
        value = self.visit(ctx.expr())
        return Assignment(lvalue, value)
    
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
        return self.visit(ctx.getChild(0))

    def visitWhileLoop(self, ctx):
        condition = self.visit(ctx.expr())
        body = self.visit(ctx.statement_block())
        return WhileStmt(condition,body)
    
    def visitForLoop(self, ctx):
        variable = ctx.ID().getText()
        condition = self.visit(ctx.expr())
        body = self.visit(ctx.statement_block())
        return ForStmt(variable,condition,body)
    
    def visitStatement_block(self, ctx):
        statements = list(map(lambda x: self.visit(x), ctx.statement())) if ctx.statement() else []
        return BlockStmt(statements)
    
    def visitControlflow_stmt(self, ctx):
        return self.visit(ctx.getChild(0))
    
    def visitBreak_stmt(self, ctx):
        return BreakStmt()
    
    def visitContinue_stmt(self, ctx):
        return ContinueStmt()
    
    def visitReturn_stmt(self, ctx):
        value = self.visit(ctx.expr()) if ctx.expr() else None
        return ReturnStmt(value)
    
    def visitBlock_stmt(self, ctx):
        statements = list(map(lambda x: self.visit(x), ctx.statement())) if ctx.statement() else []
        return BlockStmt(statements)
        
    def visitExpr(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr1(0))
        else:
            exprs = [self.visit(expr) for expr in ctx.expr1()]
            operators = [op.getText() for op in ctx.PIPE_LINE()]
            return reduce(
                lambda left, pair: BinaryOp(left, pair[0], pair[1]),
                zip(operators, exprs[1:]),
                exprs[0]
            )

    def visitExpr1(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr2(0))
        else:
            exprs = [self.visit(expr) for expr in ctx.expr2()]
            operators = [op.getText() for op in ctx.OR()]
            return reduce(
                lambda left, pair: BinaryOp(left, pair[0], pair[1]),
                zip(operators, exprs[1:]),
                exprs[0]
            )

    def visitExpr2(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr3(0))
        else:
            exprs = [self.visit(expr) for expr in ctx.expr3()]
            operators = [op.getText() for op in ctx.AND()]
            return reduce(
                lambda left, pair: BinaryOp(left, pair[0], pair[1]),
                zip(operators, exprs[1:]),
                exprs[0]
            )

    def visitExpr3(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr4(0))
        else:
            exprs = [self.visit(expr) for expr in ctx.expr4()]
            operators = [ctx.getChild(i*2+1).getText() for i in range(len(ctx.expr4())-1)]
            return reduce(
                lambda left, pair: BinaryOp(left, pair[0], pair[1]),
                zip(operators, exprs[1:]),
                exprs[0]
            )

    def visitExpr4(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr5(0))
        else:
            exprs = [self.visit(expr) for expr in ctx.expr5()]
            operators = [ctx.getChild(i*2+1).getText() for i in range(len(ctx.expr5())-1)]
            return reduce(
                lambda left, pair: BinaryOp(left, pair[0], pair[1]),
                zip(operators, exprs[1:]),
                exprs[0]
            )

    def visitExpr5(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr6(0))
        else:
            exprs = [self.visit(expr) for expr in ctx.expr6()]
            operators = [ctx.getChild(i*2+1).getText() for i in range(len(ctx.expr6())-1)]
            return reduce(
                lambda left, pair: BinaryOp(left, pair[0], pair[1]),
                zip(operators, exprs[1:]),
                exprs[0]
            )

    def visitExpr6(self, ctx):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr7(0))
        else:
            exprs = [self.visit(expr) for expr in ctx.expr7()]
            operators = [ctx.getChild(i*2+1).getText() for i in range(len(ctx.expr7())-1)]
            return reduce(
                lambda left, pair: BinaryOp(left, pair[0], pair[1]),
                zip(operators, exprs[1:]),
                exprs[0]
            )
            
    def visitExpr7(self, ctx):
        # Lấy tất cả children
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr8())
        elif ctx.NOT() or ctx.MINUS() or ctx.PLUS():
            children = list(ctx.getChildren())
            operand = self.visit(ctx.expr8())
            
            operators = [child.getText() for child in children[:-1]]
            
            for op in reversed(operators):
                operand = UnaryOp(op, operand)
            return operand
        
    def visitExpr8(self, ctx):
        base = self.visit(ctx.primary_expression())
        if not ctx.expr():
            return base
        else:
            return reduce(
                lambda acc, expr: ArrayAccess(acc, self.visit(expr)),
                ctx.expr(),
                base
            )                                                 
        
    def visitPrimary_expression(self, ctx):    
        if ctx.getChildCount() == 3:
            return self.visit(ctx.expr())
        else:
            return self.visit(ctx.getChild(0))
        
    def visitIdentifier(self,ctx):
        name = ctx.ID().getText()
        return Identifier(name)
        
    def visitLiterals(self, ctx):
        if ctx.INT_LIT():
            return IntegerLiteral(int(ctx.INT_LIT().getText()))
        elif ctx.FLOAT_LIT():
            return FloatLiteral(float(ctx.FLOAT_LIT().getText()))
        elif ctx.STRING_LIT():
            return StringLiteral(ctx.STRING_LIT().getText())
        elif ctx.BOOL_LIT():
            return BooleanLiteral(True if ctx.BOOL_LIT().getText() == "true" else False)
        elif ctx.array_lit():
            return self.visit(ctx.array_lit())
    
    def visitArray_lit(self, ctx):
        elements = list(map(lambda x: self.visit(x),ctx.expr()))
        return ArrayLiteral(elements)

    def visitFunc_call(self, ctx):
        function = self.visit(ctx.identifier())
        args = list(map(lambda x: self.visit(x), ctx.argument_list().expr())) if ctx.argument_list() else []
        return FunctionCall(function, args)
    