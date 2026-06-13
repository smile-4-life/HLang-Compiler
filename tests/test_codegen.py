from src.utils.nodes import *
from utils import CodeGenerator
import sys, os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # Ensure src package is importable

"""
HLang Code Generation Test Suite (Freshly Designed)
Based on the detailed test plan in test_plan.md.
This suite verifies code generation for all language features.
"""
# Hello world
# Test case: hello world
def testcase_000():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Hello")]))
    ])])
    assert CodeGenerator().generate_and_run(ast) == "Hello"

# Test case: constdecl int
def testcase_001():
    ast = Program(
        [ConstDecl("a", IntType(), IntegerLiteral(1))], 
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("a")])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "1"
    
# Test case: consdecl float
def testcase_002():
    ast = Program(
        [ConstDecl("a", FloatType(), FloatLiteral(1.0))],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("float2str"), [Identifier("a")])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "1.0"
    
# Test case: constdecl string
def testcase_003():
    ast = Program(
        [ConstDecl("a", StringType(), StringLiteral("Hello"))],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [Identifier("a")]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "Hello"
    
    
# Test case: constdecl bool
def testcase_004():
    ast = Program(
        [ConstDecl("a", BoolType(), BooleanLiteral(True))],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"), [Identifier("a")])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "true"

# Test case: var decl int
def testcase_005():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", IntType(), IntegerLiteral(1)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("a")])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "1"

# Test case: var decl float
def testcase_006():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", FloatType(), FloatLiteral(1.0)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("float2str"), [Identifier("a")])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "1.0"
    
# Test case: var decl string
def testcase_007():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", StringType(), StringLiteral("Hello")),
                    ExprStmt(FunctionCall(Identifier("print"), [Identifier("a")]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "Hello"

# Test case: var decl bool
def testcase_008():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", BoolType(), BooleanLiteral(True)),
                    ExprStmt(FunctionCall(Identifier("print"), [Identifier("a")]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "true"

# Test case: var decl infer int
def testcase_009():
    ast = Program(
        [VarDecl("a", None, IntegerLiteral(1))],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("a")])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "1"

# Test case: var decl infer float
def testcase_010():
    ast = Program(
        [VarDecl("a", None, FloatLiteral(1.0))],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("float2str"), [Identifier("a")])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "1.0"

# Test case: var decl infer string
def testcase_011():
    ast = Program(
        [VarDecl("a", None, StringLiteral("Hello"))],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [Identifier("a")]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "Hello"

# Test case: var decl infer bool
def testcase_012():
    ast = Program(
        [VarDecl("a", None, BooleanLiteral(True))],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"), [Identifier("a")])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "true"

# Test case: add int
def testcase_013():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, IntegerLiteral(1)),
                    VarDecl("b", None, IntegerLiteral(2)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [BinaryOp("+", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "3"

# Test case: add float
def testcase_014():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, FloatLiteral(1.0)),
                    VarDecl("b", None, FloatLiteral(2.0)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("float2str"), [BinaryOp("+", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "3.0"

# Test case: add int float
def testcase_015():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, IntegerLiteral(1)),
                    VarDecl("b", None, FloatLiteral(2.0)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("float2str"), [BinaryOp("+", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "3.0"

# Test case: add string
def testcase_016():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, StringLiteral("Hello")),
                    VarDecl("b", None, StringLiteral(", World!")),
                    ExprStmt(FunctionCall(Identifier("print"), [BinaryOp("+", Identifier("a"), Identifier("b"))]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "Hello, World!"

# Test case: add string int
def testcase_017():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, StringLiteral("Hello")),
                    VarDecl("b", None, IntegerLiteral(1)),
                    ExprStmt(FunctionCall(Identifier("print"), [BinaryOp("+", Identifier("a"), Identifier("b"))]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "Hello1"

# Test case: add string float
def testcase_018():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, StringLiteral("Hello")),
                    VarDecl("b", None, FloatLiteral(1.0)),
                    ExprStmt(FunctionCall(Identifier("print"), [BinaryOp("+", Identifier("a"), Identifier("b"))]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "Hello1.0"

# Test case: add float string
def testcase_019():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, FloatLiteral(1.0)),
                    VarDecl("b", None, StringLiteral("Hello")),
                    ExprStmt(FunctionCall(Identifier("print"), [BinaryOp("+", Identifier("a"), Identifier("b"))]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "1.0Hello"

# Test case: add float string int
def testcase_020():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, FloatLiteral(1.0)),
                    VarDecl("b", None, StringLiteral("Hello")),
                    VarDecl("c", None, IntegerLiteral(1)),
                    ExprStmt(FunctionCall(Identifier("print"), [BinaryOp("+", BinaryOp("+", Identifier("a"), Identifier("b")), Identifier("c"))]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "1.0Hello1"

# Test case: add string float string
def testcase_021():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, StringLiteral("Hello")),
                    VarDecl("b", None, FloatLiteral(1.0)),
                    VarDecl("c", None, StringLiteral("World")),
                    ExprStmt(FunctionCall(Identifier("print"), [BinaryOp("+", BinaryOp("+", Identifier("a"), Identifier("b")), Identifier("c"))]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "Hello1.0World"

# Test case: add bool
def testcase_022():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, BooleanLiteral(True)),
                    VarDecl("b", None, BooleanLiteral(False)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"), [BinaryOp("+", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "false"
    
# Test case: sub int
def testcase_023():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, IntegerLiteral(1)),
                    VarDecl("b", None, IntegerLiteral(2)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [BinaryOp("-", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "-1"

# Test case: sub float
def testcase_024():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, FloatLiteral(1.0)),
                    VarDecl("b", None, FloatLiteral(2.0)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("float2str"), [BinaryOp("-", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "-1.0"

# Test case: sub int float
def testcase_025():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, IntegerLiteral(1)),
                    VarDecl("b", None, FloatLiteral(2.0)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("float2str"), [BinaryOp("-", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "-1.0"

# Test case: sub float int
def testcase_026():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, FloatLiteral(1.0)),
                    VarDecl("b", None, IntegerLiteral(2)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("float2str"), [BinaryOp("-", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "-1.0"

# Test case: mul int
def testcase_027():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, IntegerLiteral(2)),
                    VarDecl("b", None, IntegerLiteral(3)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [BinaryOp("*", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "6"

# Test case: mul float
def testcase_028():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, FloatLiteral(2.0)),
                    VarDecl("b", None, FloatLiteral(3.0)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("float2str"), [BinaryOp("*", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "6.0"

# Test case: mul int float
def testcase_029():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, IntegerLiteral(6)),
                    VarDecl("b", None, FloatLiteral(3.0)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("float2str"), [BinaryOp("*", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "18.0"

# Test case: div int
def testcase_030():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, IntegerLiteral(6)),
                    VarDecl("b", None, IntegerLiteral(3)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [BinaryOp("/", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "2"

# Test case: div float
def testcase_031():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, FloatLiteral(6.0)),
                    VarDecl("b", None, FloatLiteral(3.0)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("float2str"), [BinaryOp("/", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "2.0"

# Test case: div int float
def testcase_032():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, IntegerLiteral(6)),
                    VarDecl("b", None, FloatLiteral(3.0)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("float2str"), [BinaryOp("/", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "2.0"

# Test case: mod int
def testcase_033():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, IntegerLiteral(7)),
                    VarDecl("b", None, IntegerLiteral(3)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [BinaryOp("%", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "1"

# Test case: compare equal
def testcase_034():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, IntegerLiteral(1)),
                    VarDecl("b", None, IntegerLiteral(1)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"), [BinaryOp("==", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "true"

# Test case: compare not equal
def testcase_035():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, IntegerLiteral(1)),
                    VarDecl("b", None, IntegerLiteral(2)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"), [BinaryOp("!=", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "true"

# Test case: compare greater than
def testcase_036():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, IntegerLiteral(2)),
                    VarDecl("b", None, IntegerLiteral(1)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"), [BinaryOp(">", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "true"

# Test case: compare less than
def testcase_037():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, IntegerLiteral(1)),
                    VarDecl("b", None, IntegerLiteral(2)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"), [BinaryOp("<", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "true"

# Test case: compare greater than equal
def testcase_038():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, IntegerLiteral(2)),
                    VarDecl("b", None, IntegerLiteral(1)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"), [BinaryOp(">=", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "true"

# Test case: compare less than equal
def testcase_039():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, IntegerLiteral(1)),
                    VarDecl("b", None, IntegerLiteral(2)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"), [BinaryOp("<=", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "true"
        
# Test case: compare string
def testcase_040():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, StringLiteral("Hello")),
                    VarDecl("b", None, StringLiteral("World")),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"), [BinaryOp(">", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "false"

# Test case: compare bool
def testcase_041():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, BooleanLiteral(True)),
                    VarDecl("b", None, BooleanLiteral(False)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"), [BinaryOp(">", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "true"
    
# Test case: and bool
def testcase_042():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, BooleanLiteral(True)),
                    VarDecl("b", None, BooleanLiteral(False)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"), [BinaryOp("+", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "false"

# Test case: or bool
def testcase_043():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, BooleanLiteral(True)),
                    VarDecl("b", None, BooleanLiteral(False)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"), [BinaryOp("||", Identifier("a"), Identifier("b"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "true"

# Test case: deep expression bool
def testcase_044():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, BooleanLiteral(True)),
                    VarDecl("b", None, BooleanLiteral(False)),
                    VarDecl("c", None, BooleanLiteral(True)),
                    VarDecl("d", None, BooleanLiteral(False)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"), [BinaryOp(">", BinaryOp(">", BinaryOp(">", Identifier("a"), Identifier("b")), Identifier("c")), Identifier("d"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "false"
    
# Test case: deep expression int
def testcase_045():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, IntegerLiteral(1)),
                    VarDecl("b", None, IntegerLiteral(2)),
                    VarDecl("c", None, IntegerLiteral(3)),
                    VarDecl("d", None, IntegerLiteral(4)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"), [BinaryOp(">", BinaryOp("+", BinaryOp("+", Identifier("a"), Identifier("b")), Identifier("c")), Identifier("d"))])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "true"
    
# Test case: array decl int
def testcase_046():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", ArrayType(IntType(), 10), ArrayLiteral([IntegerLiteral(99), IntegerLiteral(55), IntegerLiteral(23), IntegerLiteral(77), IntegerLiteral(1)])),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [ArrayAccess(Identifier("a"), IntegerLiteral(0))])])),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [ArrayAccess(Identifier("a"), IntegerLiteral(1))])])),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [ArrayAccess(Identifier("a"), IntegerLiteral(2))])])),
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "99\n55\n23"

# Test case: array decl float
def testcase_047():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", ArrayType(FloatType(), 10), ArrayLiteral([FloatLiteral(99.9), FloatLiteral(55.5), FloatLiteral(23.3), FloatLiteral(77.7), FloatLiteral(1.1)])),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("float2str"), [ArrayAccess(Identifier("a"), IntegerLiteral(0))])])),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("float2str"), [ArrayAccess(Identifier("a"), IntegerLiteral(1))])])),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("float2str"), [ArrayAccess(Identifier("a"), IntegerLiteral(2))])])),
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "99.9\n55.5\n23.3"

# Test case: array decl string
def testcase_048():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", ArrayType(StringType(), 10), ArrayLiteral([StringLiteral("Hello"), StringLiteral("World"), StringLiteral("HLang")])),
                    ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("a"), IntegerLiteral(0))])),
                    ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("a"), IntegerLiteral(1))])),
                    ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("a"), IntegerLiteral(2))])),
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "Hello\nWorld\nHLang"

# Test case: array decl bool
def testcase_049():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", ArrayType(BoolType(), 10), ArrayLiteral([BooleanLiteral(True), BooleanLiteral(False), BooleanLiteral(True), BooleanLiteral(False), BooleanLiteral(True)])),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"), [ArrayAccess(Identifier("a"), IntegerLiteral(0))])])),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"), [ArrayAccess(Identifier("a"), IntegerLiteral(1))])])),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"), [ArrayAccess(Identifier("a"), IntegerLiteral(2))])])),
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "true\nfalse\ntrue"

# Test case: array decl infer int
def testcase_050():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, ArrayLiteral([IntegerLiteral(99), IntegerLiteral(55), IntegerLiteral(23), IntegerLiteral(77), IntegerLiteral(1)])),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [ArrayAccess(Identifier("a"), IntegerLiteral(0))])])),
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "99"

# Test case: array decl infer float
def testcase_051():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, ArrayLiteral([FloatLiteral(99.9), FloatLiteral(55.5), FloatLiteral(23.3), FloatLiteral(77.7), FloatLiteral(1.1)])),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("float2str"), [ArrayAccess(Identifier("a"), IntegerLiteral(0))])])),
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "99.9"

# Test case: array decl infer string
def testcase_052():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, ArrayLiteral([StringLiteral("Hello"), StringLiteral("World"), StringLiteral("HLang")])),
                    ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("a"), IntegerLiteral(0))])),
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "Hello"

# Test case: array decl infer bool
def testcase_053():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", None, ArrayLiteral([BooleanLiteral(True), BooleanLiteral(False), BooleanLiteral(True), BooleanLiteral(False), BooleanLiteral(True)])),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"), [ArrayAccess(Identifier("a"), IntegerLiteral(0))])])),
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "true"

# Test case: array multidimention decl explicit type
def testcase_054():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    # let matrix = [[1, 2], [3, 4]];
                    VarDecl(
                        "matrix", 
                        ArrayType(ArrayType(IntType(), 2), 2), 
                        ArrayLiteral([
                            ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]),
                            ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4)])
                        ])
                    ),
                    # print(str(matrix[0][1]));
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [
                                FunctionCall(
                                    Identifier("str"), 
                                    [
                                        # matrix[0][1]
                                        ArrayAccess(
                                            ArrayAccess(Identifier("matrix"), IntegerLiteral(0)), 
                                            IntegerLiteral(1)
                                        )
                                    ]
                                )
                            ]
                        )
                    ),
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "2"
    
# Test case: array multidimention decl infer type
def testcase_055():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    # let matrix = [[1, 2], [3, 4]];
                    VarDecl(
                        "matrix", 
                        None, 
                        ArrayLiteral([
                            ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]),
                            ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4)])
                        ])
                    ),
                    # print(str(matrix[0][1]));
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [
                                FunctionCall(
                                    Identifier("str"), 
                                    [
                                        # matrix[0][1]
                                        ArrayAccess(
                                            ArrayAccess(Identifier("matrix"), IntegerLiteral(0)), 
                                            IntegerLiteral(1)
                                        )
                                    ]
                                )
                            ]
                        )
                    ),
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "2"
    
# Test case: array elements calculation 1d
def testcase_056():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    # let arr = [10, 20, 30];
                    VarDecl(
                        "arr", None, 
                        ArrayLiteral([IntegerLiteral(10), IntegerLiteral(20), IntegerLiteral(30)])
                    ),
                    # let result = (arr[0] + arr[1]) * arr[2];
                    VarDecl(
                        "result", None,
                        BinaryOp(
                            "*",
                            BinaryOp(
                                "+",
                                ArrayAccess(Identifier("arr"), IntegerLiteral(0)),
                                ArrayAccess(Identifier("arr"), IntegerLiteral(1))
                            ),
                            ArrayAccess(Identifier("arr"), IntegerLiteral(2))
                        )
                    ),
                    # print(int2str(result));
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [Identifier("result")])]
                        )
                    ),
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "900"

# Test case: array elements calculation 2d
def testcase_057():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    # let matrix = [[1, 2], [3, 4]];
                    VarDecl(
                        "matrix", None, 
                        ArrayLiteral([
                            ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]),
                            ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4)])
                        ])
                    ),
                    # let sum = matrix[0][0] + matrix[0][1] + matrix[1][0] + matrix[1][1];
                    VarDecl(
                        "sum", None,
                        BinaryOp(
                            "+",
                            BinaryOp(
                                "+",
                                BinaryOp(
                                    "+",
                                    ArrayAccess(ArrayAccess(Identifier("matrix"), IntegerLiteral(0)), IntegerLiteral(0)),
                                    ArrayAccess(ArrayAccess(Identifier("matrix"), IntegerLiteral(0)), IntegerLiteral(1))
                                ),
                                ArrayAccess(ArrayAccess(Identifier("matrix"), IntegerLiteral(1)), IntegerLiteral(0))
                            ),
                            ArrayAccess(ArrayAccess(Identifier("matrix"), IntegerLiteral(1)), IntegerLiteral(1))
                        )
                    ),
                    # print(int2str(sum));
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("int2str"), [Identifier("sum")])]
                        )
                    ),
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "10"

# Test case: array element update int
def testcase_058():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    # let arr = [10, 20, 30];
                    VarDecl(
                        "arr", None, 
                        ArrayLiteral([IntegerLiteral(10), IntegerLiteral(20), IntegerLiteral(30)])
                    ),
                    # arr[1] = 99;
                    Assignment(
                        ArrayAccess(Identifier("arr"), IntegerLiteral(1)),
                        IntegerLiteral(99)
                    ),
                    # print(int2str(arr[1]));
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [
                                FunctionCall(
                                    Identifier("int2str"), 
                                    [ArrayAccess(Identifier("arr"), IntegerLiteral(1))]
                                )
                            ]
                        )
                    ),
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "99"

# Test case: array element update float
def testcase_059():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    # let arr = [10.5, 20.5, 30.5];
                    VarDecl(
                        "arr", None, 
                        ArrayLiteral([FloatLiteral(10.5), FloatLiteral(20.5), FloatLiteral(30.5)])
                    ),
                    # arr[1] = 99.5;
                    Assignment(
                        ArrayAccess(Identifier("arr"), IntegerLiteral(1)),
                        FloatLiteral(99.5)
                    ),
                    # print(str(arr[1]));
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [ArrayAccess(Identifier("arr"), IntegerLiteral(1))]
                        )
                    ),
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "99.5"
    
# Test case: array element update bool
def testcase_060():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    # let arr = [true, false, true];
                    VarDecl(
                        "arr", None, 
                        ArrayLiteral([BooleanLiteral(True), BooleanLiteral(False), BooleanLiteral(True)])
                    ),
                    # arr[1] = true;
                    Assignment(
                        ArrayAccess(Identifier("arr"), IntegerLiteral(1)),
                        BooleanLiteral(True)
                    ),
                    # print(bool2str(arr[1]));
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [FunctionCall(Identifier("bool2str"), [ArrayAccess(Identifier("arr"), IntegerLiteral(1))])]
                        )
                    ),
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "true"

# Test case: array element update string
def testcase_061():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    # let arr = ["hello", "world"];
                    VarDecl(
                        "arr", None, 
                        ArrayLiteral([StringLiteral("hello"), StringLiteral("world")])
                    ),
                    # arr[1] = "world!";
                    Assignment(
                        ArrayAccess(Identifier("arr"), IntegerLiteral(1)),
                        StringLiteral("world!")
                    ),
                    # print(arr[1]);
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), 
                            [ArrayAccess(Identifier("arr"), IntegerLiteral(1))]
                        )
                    ),
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "world!"

# Test case: pipeline operator chain
def testcase_062():
    ast = Program(
        [],
        [
            # square function: return n * n
            FuncDecl(
                "square",
                [Param("n", IntType())],
                IntType(),
                [ReturnStmt(BinaryOp("*", Identifier("n"), Identifier("n")))]
            ),
            # add function: return a + b
            FuncDecl(
                "add",
                [Param("a", IntType()), Param("b", IntType())],
                IntType(),
                [ReturnStmt(BinaryOp("+", Identifier("a"), Identifier("b")))]
            ),
            # main function
            FuncDecl(
                "main", [], VoidType(),
                [
                    # Evaluate pipeline chain: 5 >> square() >> add(10)
                    VarDecl(
                        "result", None,
                        BinaryOp(
                            ">>",
                            BinaryOp(
                                ">>",
                                IntegerLiteral(5),
                                FunctionCall(Identifier("square"), [])
                            ),
                            FunctionCall(Identifier("add"), [IntegerLiteral(10)])
                        )
                    ),
                    # Print pipeline result using built-in 'str' or direct variable
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"),
                            [FunctionCall(Identifier("int2str"), [Identifier("result")])] # Fixed: Use built-in 'str' instead of 'int2str'
                        )
                    ),
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "35"

# Test case: if simple
def testcase_063():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    # if (true) { print("Only If"); }
                    IfStmt(
                        condition=BooleanLiteral(True),
                        then_stmt=BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Only If")]))
                        ]),
                        elif_branches=None,
                        else_stmt=None
                    )
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "Only If"

# Test case: if else
def testcase_064():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    # if (false) { print("If"); } else { print("Else"); }
                    IfStmt(
                        condition=BooleanLiteral(False),
                        then_stmt=BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("If")]))
                        ]),
                        elif_branches=None,
                        else_stmt=BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Else")]))
                        ])
                    )
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "Else"

# Test case: if elif else
def testcase_065():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    # let x = 2;
                    VarDecl("x", IntType(), IntegerLiteral(2)),
                    
                    # if-elif-else structural check
                    IfStmt(
                        condition=BinaryOp("==", Identifier("x"), IntegerLiteral(1)),
                        then_stmt=BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("One")]))
                        ]),
                        elif_branches=[
                            # Cặp (Condition, Stmt) cho nhánh elif đầu tiên
                            (
                                BinaryOp("==", Identifier("x"), IntegerLiteral(2)),
                                BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Two")]))])
                            )
                        ],
                        else_stmt=BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Other")]))
                        ])
                    )
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "Two"

# Test case: nested if
def testcase_066():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    # Outer If
                    IfStmt(
                        condition=BooleanLiteral(True),
                        then_stmt=BlockStmt([
                            # Inner If-Else inside Outer Then block
                            IfStmt(
                                condition=BooleanLiteral(False),
                                then_stmt=BlockStmt([
                                    ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Inner If")]))
                                ]),
                                elif_branches=None,
                                else_stmt=BlockStmt([
                                    ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Inner Else")]))
                                ])
                            )
                        ]),
                        elif_branches=None,
                        else_stmt=None
                    )
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "Inner Else"

# Test case: if with let
def testcase_067():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    # let x = 10;
                    VarDecl("x", IntType(), IntegerLiteral(10)),
                    
                    # if (x > 5) { print("Greater"); }
                    IfStmt(
                        condition=BinaryOp(">", Identifier("x"), IntegerLiteral(5)),
                        then_stmt=BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Greater")]))
                        ]),
                        elif_branches=None,
                        else_stmt=None
                    )
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "Greater"

# Test case: if with assignment
def testcase_068():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    # let x = 10;
                    VarDecl("x", IntType(), IntegerLiteral(10)),
                    
                    # if (x > 5) { x = 20; print(x); }
                    IfStmt(
                        condition=BinaryOp(">", Identifier("x"), IntegerLiteral(5)),
                        then_stmt=BlockStmt([
                            # Assignment inside if
                            Assignment(
                                Identifier("x"),
                                IntegerLiteral(20)
                            ),
                            ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))
                        ]),
                        elif_branches=None,
                        else_stmt=None
                    )
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "20"

# Test case: if with function call
def testcase_069():
    ast = Program(
        [],
        [
            FuncDecl(
                "isEven",
                [Param("n", IntType())],
                BoolType(),
                [ReturnStmt(BinaryOp("==", BinaryOp("%", Identifier("n"), IntegerLiteral(2)), IntegerLiteral(0)))]
            ),
            FuncDecl(
                "main", [], VoidType(),
                [
                    # let x = 10;
                    VarDecl("x", IntType(), IntegerLiteral(10)),
                    
                    # if (isEven(x)) { print("Even"); } else { print("Odd"); }
                    IfStmt(
                        condition=FunctionCall(Identifier("isEven"), [Identifier("x")]),
                        then_stmt=BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Even")]))
                        ]),
                        elif_branches=None,
                        else_stmt=BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Odd")]))
                        ])
                    )
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "Even"

# Test case: if complex logic
def testcase_070():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    # let x = 10;
                    VarDecl("x", IntType(), IntegerLiteral(10)),
                    
                    # if (x > 5 && x < 15) { print("Between 5 and 15"); } 
                    # else { print("Outside range"); }
                    IfStmt(
                        condition=BinaryOp(
                            "&&",
                            BinaryOp(">", Identifier("x"), IntegerLiteral(5)),
                            BinaryOp("<", Identifier("x"), IntegerLiteral(15))
                        ),
                        then_stmt=BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Between 5 and 15")]))
                        ]),
                        elif_branches=None,
                        else_stmt=BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Outside range")]))
                        ])
                    )
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "Between 5 and 15"

# Test case: if with nested let
def testcase_071():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    # if (true) { let y = 5; let x = y + 10; print(x); }
                    IfStmt(
                        condition=BooleanLiteral(True),
                        then_stmt=BlockStmt([
                            # Nested let
                            VarDecl("y", IntType(), IntegerLiteral(5)),
                            VarDecl("x", IntType(), BinaryOp("+", Identifier("y"), IntegerLiteral(10))),
                            ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))
                        ]),
                        elif_branches=None,
                        else_stmt=None
                    )
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "15"

# Test case: while basic
def testcase_072():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    # Initialize loop variable and accumulator
                    VarDecl("i", IntType(), IntegerLiteral(1)),
                    VarDecl("sum", IntType(), IntegerLiteral(0)),
                    
                    # while (i <= 5)
                    WhileStmt(
                        condition=BinaryOp("<=", Identifier("i"), IntegerLiteral(5)),
                        body=BlockStmt([
                            # sum = sum + i
                            Assignment(
                                Identifier("sum"),
                                BinaryOp("+", Identifier("sum"), Identifier("i"))
                            ),
                            # i = i + 1
                            Assignment(
                                Identifier("i"),
                                BinaryOp("+", Identifier("i"), IntegerLiteral(1))
                            )
                        ])
                    ),
                    # Print result
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("str"), [Identifier("sum")])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "15"

# Test case: for in basic
def testcase_073():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    # Initialize accumulator and array literal
                    VarDecl("total", IntType(), IntegerLiteral(0)),
                    VarDecl("arr", None, ArrayLiteral([IntegerLiteral(10), IntegerLiteral(20), IntegerLiteral(30)])),
                    
                    # for x in arr
                    ForStmt(
                        variable="x",
                        iterable=Identifier("arr"),
                        body=BlockStmt([
                            # total = total + x
                            Assignment(
                                Identifier("total"),
                                BinaryOp("+", Identifier("total"), Identifier("x"))
                            )
                        ])
                    ),
                    # Print result
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("str"), [Identifier("total")])]))
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "60"

# Test case: for in nested let
def testcase_074():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    # Initialize array literal
                    VarDecl("arr", None, ArrayLiteral([IntegerLiteral(5)])),
                    
                    # for item in arr
                    ForStmt(
                        variable="item",
                        iterable=Identifier("arr"),
                        body=BlockStmt([
                            # Local variable declaration inside loop body
                            VarDecl("temp", IntType(), BinaryOp("+", Identifier("item"), IntegerLiteral(10))),
                            # Print temp (5 + 10 = 15)
                            ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("str"), [Identifier("temp")])]))
                        ])
                    )
                ]
            )
        ]
    )
    assert CodeGenerator().generate_and_run(ast) == "15"

    
