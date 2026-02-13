from src.utils.nodes import *
from utils import CodeGenerator

def test001():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("hello")]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "hello"

def test002():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("int2str"), [IntegerLiteral(42)])]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "42"

def test003():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", IntType(), IntegerLiteral(5)),
                    VarDecl("b", IntType(), IntegerLiteral(7)),
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("int2str"),
                            [BinaryOp(Identifier("a"), "+", Identifier("b"))]
                        )]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "12"

def test004():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(3)),
                    IfStmt(
                        BinaryOp(Identifier("x"), ">", IntegerLiteral(0)),
                        BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("pos")]))
                        ]),
                        [],
                        BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("neg")]))
                        ])
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "pos"

def test005():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("i", IntType(), IntegerLiteral(0)),
                    WhileStmt(
                        BinaryOp(Identifier("i"), "<", IntegerLiteral(3)),
                        BlockStmt([
                            ExprStmt(FunctionCall(
                                Identifier("print"),
                                [FunctionCall(Identifier("int2str"), [Identifier("i")])]
                            )),
                            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                        ])
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "0\n1\n2"

def test006():
    ast = Program(
        [],
        [
            FuncDecl(
                "sum2", [Param("a", IntType()), Param("b", IntType())], IntType(),
                [ReturnStmt(BinaryOp(Identifier("a"), "+", Identifier("b")))]
            ),
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("int2str"),
                            [FunctionCall(Identifier("sum2"), [IntegerLiteral(2), IntegerLiteral(3)])]
                        )]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "5"

def test007():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("bool2str"), [BooleanLiteral(True)])]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "true"

def test008():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("float2str"), [FloatLiteral(3.14)])]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "3.14"

def test009():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(0)),
                    IfStmt(
                        BinaryOp(Identifier("x"), ">", IntegerLiteral(0)),
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("pos")]))]),
                        [
                            (BinaryOp(Identifier("x"), "<", IntegerLiteral(0)),
                             BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("neg")]))]))
                        ],
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("zero")]))])
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "zero"

def test010():
    ast = Program(
        [],
        [
            FuncDecl(
                "add", [Param("a", IntType()), Param("b", IntType())], IntType(),
                [ReturnStmt(BinaryOp(Identifier("a"), "+", Identifier("b")))]
            ),
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("int2str"),
                            [FunctionCall(Identifier("add"), [
                                FunctionCall(Identifier("add"), [IntegerLiteral(1), IntegerLiteral(2)]),
                                IntegerLiteral(3)
                            ])]
                        )]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "6"

def test011():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [
                            BinaryOp(
                                IntegerLiteral(123),
                                ">>",
                                FunctionCall(Identifier("int2str"), [])
                            )
                        ]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "123"

def test012():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [
                            BinaryOp(
                                StringLiteral("Hello, "),
                                "+",
                                StringLiteral("world!")
                            )
                        ]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "Hello, world!"

def test013():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("i", IntType(), IntegerLiteral(0)),
                    WhileStmt(
                        BinaryOp(Identifier("i"), "<", IntegerLiteral(5)),
                        BlockStmt([
                            IfStmt(
                                BinaryOp(Identifier("i"), "==", IntegerLiteral(2)),
                                BlockStmt([Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1))), ContinueStmt()]),
                                [],
                                None
                            ),
                            IfStmt(
                                BinaryOp(Identifier("i"), "==", IntegerLiteral(4)),
                                BlockStmt([BreakStmt()]),
                                [],
                                None
                            ),
                            ExprStmt(FunctionCall(
                                Identifier("print"),
                                [FunctionCall(Identifier("int2str"), [Identifier("i")])]
                            )),
                            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                        ])
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "0\n1\n3"

def test014():
    ast = Program(
        [ConstDecl("PI", FloatType(), FloatLiteral(3.14))],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(10)),
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("int2str"), [Identifier("x")])]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "10"

def test015():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("bool2str"), [BooleanLiteral(False)])]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "false"

def test016():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("float2str"), [FloatLiteral(-2.5)])]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "-2.5"

def test017():
    ast = Program(
        [ConstDecl("X", IntType(), IntegerLiteral(100))],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ConstDecl("X", IntType(), IntegerLiteral(5)),
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("int2str"), [Identifier("X")])]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "5"

def test018():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("score", IntType(), IntegerLiteral(85)),
                    IfStmt(
                        BinaryOp(Identifier("score"), ">=", IntegerLiteral(90)),
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("A")]))]),
                        [
                            (BinaryOp(Identifier("score"), ">=", IntegerLiteral(80)),
                             BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("B")]))]))
                        ],
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("C")]))])
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "B"

def test019():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", BoolType(), BooleanLiteral(True)),
                    VarDecl("b", BoolType(), BooleanLiteral(False)),
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("bool2str"),
                            [BinaryOp(
                                BinaryOp(Identifier("a"), "&&", Identifier("b")),
                                "||",
                                UnaryOp("!", Identifier("b"))
                            )]
                        )]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "true"

def test020():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("bool2str"),
                            [BinaryOp(IntegerLiteral(5), "<", IntegerLiteral(10))]
                        )]
                    )),
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("bool2str"),
                            [BinaryOp(StringLiteral("abcd"), ">", StringLiteral("abc"))]
                        )]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "true\ntrue"

def test021():
    ast = Program(
        [],
        [
            FuncDecl(
                "get42", [], IntType(),
                [ReturnStmt(IntegerLiteral(42))]
            ),
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("int2str"),
                            [FunctionCall(Identifier("get42"), [])]
                        )]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "42"

def test022():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(5)),
                    IfStmt(
                        BinaryOp(Identifier("x"), ">", IntegerLiteral(0)),
                        BlockStmt([
                            IfStmt(
                                BinaryOp(Identifier("x"), ">", IntegerLiteral(10)),
                                BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("big")]))]),
                                [],
                                BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("small")]))])
                            )
                        ]),
                        [],
                        None
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "small"

def test023():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [
                            BinaryOp(
                                BinaryOp(
                                    IntegerLiteral(5),
                                    "+",
                                    IntegerLiteral(7)
                                ),
                                ">>",
                                FunctionCall(Identifier("int2str"), [])
                            )
                        ]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "12"

def test024():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("name", StringType(), StringLiteral("HLang")),
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [
                            BinaryOp(
                                BinaryOp(StringLiteral("Hello, "), "+", Identifier("name")),
                                "+",
                                StringLiteral("!")
                            )
                        ]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "Hello, HLang!"

def test025():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    IfStmt(
                        BooleanLiteral(True),
                        BlockStmt([ReturnStmt()]),
                        [],
                        None
                    ),
                    ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("should not print")]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == ""

def test026():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(10)),
                    ExprStmt(FunctionCall(Identifier("print"),
                                          [FunctionCall(Identifier("int2str"), [Identifier("x")])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "10"

def test027():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", IntType(), IntegerLiteral(5)),
                    Assignment(IdLValue("a"), BinaryOp(Identifier("a"), "*", IntegerLiteral(2))),
                    ExprStmt(FunctionCall(Identifier("print"),
                                          [FunctionCall(Identifier("int2str"), [Identifier("a")])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "10"

def test028():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("count", IntType(), IntegerLiteral(5)),
                    WhileStmt(
                        BinaryOp(Identifier("count"), ">", IntegerLiteral(0)),
                        BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("loop")])),
                            Assignment(IdLValue("count"), BinaryOp(Identifier("count"), "-", IntegerLiteral(1)))
                        ])
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "loop\nloop\nloop\nloop\nloop"

def test029():
    ast = Program(
        [],
        [
            FuncDecl(
                "is_even", [Param("n", IntType())], BoolType(),
                [
                    ReturnStmt(BinaryOp(BinaryOp(Identifier("n"), "%", IntegerLiteral(2)), "==", IntegerLiteral(0)))
                ]
            ),
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"),
                                                                            [FunctionCall(Identifier("is_even"), [IntegerLiteral(4)])])])),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"),
                                                                            [FunctionCall(Identifier("is_even"), [IntegerLiteral(5)])])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "true\nfalse"

def test030():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"),
                                          [BinaryOp(StringLiteral("A"), "+", StringLiteral("B"))]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "AB"

def test031():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(1)),
                    IfStmt(
                        BinaryOp(Identifier("x"), "==", IntegerLiteral(1)),
                        BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("one")]))
                        ]),
                        [],
                        None
                    ),
                    IfStmt(
                        BinaryOp(Identifier("x"), "==", IntegerLiteral(2)),
                        BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("two")]))
                        ]),
                        [],
                        None
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "one"

def test032():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("i", IntType(), IntegerLiteral(0)),
                    WhileStmt(
                        BinaryOp(Identifier("i"), "<", IntegerLiteral(5)),
                        BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"),
                                                  [FunctionCall(Identifier("int2str"), [Identifier("i")])])),
                            IfStmt(
                                BinaryOp(Identifier("i"), "==", IntegerLiteral(2)),
                                BlockStmt([BreakStmt()]),
                                [],
                                None
                            ),
                            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                        ])
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "0\n1\n2"

def test033():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("s1", StringType(), StringLiteral("test")),
                    VarDecl("s2", StringType(), StringLiteral("Test")),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"), [BinaryOp(Identifier("s1"), "==", Identifier("s2"))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "false"

def test034():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"),
                                                                            [BinaryOp(IntegerLiteral(5), "*", IntegerLiteral(5))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "25"

def test035():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(10)),
                    ExprStmt(FunctionCall(Identifier("print"),
                                          [FunctionCall(Identifier("int2str"), [BinaryOp(Identifier("x"), "/", IntegerLiteral(2))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "5"

def test036():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("y", IntType(), IntegerLiteral(10)),
                    WhileStmt(
                        BinaryOp(Identifier("y"), ">", IntegerLiteral(0)),
                        BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("y")])])),
                            Assignment(IdLValue("y"), BinaryOp(Identifier("y"), "-", IntegerLiteral(2)))
                        ])
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "10\n8\n6\n4\n2"

def test037():
    ast = Program(
        [],
        [
            FuncDecl(
                "get_string", [], StringType(),
                [
                    ReturnStmt(StringLiteral("from function"))
                ]
            ),
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("get_string"), [])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "from function"

def test038():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(10)),
                    IfStmt(
                        BinaryOp(Identifier("x"), "<=", IntegerLiteral(10)),
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("less or equal")]))]),
                        [],
                        None
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "less or equal"

def test039():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("s", StringType(), StringLiteral("test")),
                    ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(Identifier("s"), "+", StringLiteral("123"))]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "test123"

def test040():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"),
                                                                            [BinaryOp(UnaryOp("-", IntegerLiteral(10)), "+", IntegerLiteral(20))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "10"

def test041():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    IfStmt(
                        BinaryOp(BooleanLiteral(True), "&&", BooleanLiteral(True)),
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("both true")]))]),
                        [],
                        None
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "both true"

def test042():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"),
                                                                            [BinaryOp(IntegerLiteral(15), "%", IntegerLiteral(4))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "3"

def test043():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("s", StringType(), StringLiteral("test")),
                    IfStmt(
                        BinaryOp(Identifier("s"), "==", StringLiteral("test")),
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("equal")]))]),
                        [],
                        None
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "equal"

def test044():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [BinaryOp(IntegerLiteral(100), "-", IntegerLiteral(50))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "50"

def test045():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [BinaryOp(IntegerLiteral(2), "*", IntegerLiteral(20))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "40"

def test046():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [BinaryOp(IntegerLiteral(40), "/", IntegerLiteral(8))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "5"

def test047():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"), [BinaryOp(IntegerLiteral(10), "!=", IntegerLiteral(10))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "false"

def test048():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"),
                                                                            [BinaryOp(BooleanLiteral(True), "||", BooleanLiteral(False))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "true"

def test049():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("count", IntType(), IntegerLiteral(3)),
                    WhileStmt(
                        BinaryOp(Identifier("count"), ">", IntegerLiteral(0)),
                        BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("count")])])),
                            Assignment(IdLValue("count"), BinaryOp(Identifier("count"), "-", IntegerLiteral(1)))
                        ])
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "3\n2\n1"

def test050():
    ast = Program(
        [],
        [
            FuncDecl(
                "add_one", [Param("x", IntType())], IntType(),
                [ReturnStmt(BinaryOp(Identifier("x"), "+", IntegerLiteral(1)))]
            ),
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", IntType(), IntegerLiteral(10)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [FunctionCall(Identifier("add_one"), [Identifier("a")])])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "11"

def test051():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"),
                                          [FunctionCall(Identifier("int2str"), [BinaryOp(IntegerLiteral(1), "==", IntegerLiteral(1))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "1"

def test052():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"),
                                                                            [BinaryOp(IntegerLiteral(5), ">", IntegerLiteral(3))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "1"

def test053():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"),
                                                                            [BinaryOp(IntegerLiteral(5), "<", IntegerLiteral(3))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "0"

def test054():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", IntType(), IntegerLiteral(10)),
                    VarDecl("b", IntType(), IntegerLiteral(20)),
                    IfStmt(
                        BinaryOp(Identifier("a"), "==", Identifier("b")),
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("equal")]))]),
                        [
                            (BinaryOp(Identifier("a"), "!=", Identifier("b")),
                             BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("not equal")]))]))
                        ],
                        None
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "not equal"

def test055():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("i", IntType(), IntegerLiteral(0)),
                    WhileStmt(
                        BinaryOp(Identifier("i"), "<", IntegerLiteral(5)),
                        BlockStmt([
                            IfStmt(
                                BinaryOp(Identifier("i"), "==", IntegerLiteral(3)),
                                BlockStmt([BreakStmt()]),
                                [],
                                None
                            ),
                            ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("i")])])),
                            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                        ])
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "0\n1\n2"

def test056():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"),
                                          [BinaryOp(BinaryOp(StringLiteral("A"), "+", StringLiteral("B")), "+", StringLiteral("C"))]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "ABC"

def test057():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("x", FloatType(), FloatLiteral(10.5)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("float2str"), [BinaryOp(Identifier("x"), "*", FloatLiteral(2.0))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "21.0"

def test058():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("i", IntType(), IntegerLiteral(0)),
                    WhileStmt(
                        BinaryOp(Identifier("i"), "<", IntegerLiteral(3)),
                        BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Hello")])),
                            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                        ])
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "Hello\nHello\nHello"

def test059():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("x", BoolType(), BooleanLiteral(True)),
                    VarDecl("y", BoolType(), BooleanLiteral(False)),
                    IfStmt(
                        BinaryOp(Identifier("x"), "&&", Identifier("y")),
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("true")]))]),
                        [],
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("false")]))])
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "false"

def test060():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(10)),
                    VarDecl("y", IntType(), IntegerLiteral(20)),
                    ExprStmt(FunctionCall(Identifier("print"),
                                          [FunctionCall(Identifier("int2str"), [BinaryOp(Identifier("x"), "+", Identifier("y"))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "30"

def test060():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("hello")]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "hello"

def test061():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("int2str"), [IntegerLiteral(42)])]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "42"

def test062():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", IntType(), IntegerLiteral(5)),
                    VarDecl("b", IntType(), IntegerLiteral(7)),
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("int2str"),
                            [BinaryOp(Identifier("a"), "+", Identifier("b"))]
                        )]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "12"

def test063():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(3)),
                    IfStmt(
                        BinaryOp(Identifier("x"), ">", IntegerLiteral(0)),
                        BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("pos")]))
                        ]),
                        [],
                        BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("neg")]))
                        ])
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "pos"

def test064():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("i", IntType(), IntegerLiteral(0)),
                    WhileStmt(
                        BinaryOp(Identifier("i"), "<", IntegerLiteral(3)),
                        BlockStmt([
                            ExprStmt(FunctionCall(
                                Identifier("print"),
                                [FunctionCall(Identifier("int2str"), [Identifier("i")])]
                            )),
                            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                        ])
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "0\n1\n2"

def test065():
    ast = Program(
        [],
        [
            FuncDecl(
                "sum2", [Param("a", IntType()), Param("b", IntType())], IntType(),
                [ReturnStmt(BinaryOp(Identifier("a"), "+", Identifier("b")))]
            ),
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("int2str"),
                            [FunctionCall(Identifier("sum2"), [IntegerLiteral(2), IntegerLiteral(3)])]
                        )]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "5"


def test066():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("bool2str"), [BooleanLiteral(True)])]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "true"

def test067():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("float2str"), [FloatLiteral(3.14)])]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "3.14"


def test068():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(0)),
                    IfStmt(
                        BinaryOp(Identifier("x"), ">", IntegerLiteral(0)),
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("pos")]))]),
                        [
                            (BinaryOp(Identifier("x"), "<", IntegerLiteral(0)),
                             BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("neg")]))]))
                        ],
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("zero")]))])
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "zero"



def test069():
    ast = Program(
        [],
        [
            FuncDecl(
                "add", [Param("a", IntType()), Param("b", IntType())], IntType(),
                [ReturnStmt(BinaryOp(Identifier("a"), "+", Identifier("b")))]
            ),
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("int2str"),
                            [FunctionCall(Identifier("add"), [
                                FunctionCall(Identifier("add"), [IntegerLiteral(1), IntegerLiteral(2)]),
                                IntegerLiteral(3)
                            ])]
                        )]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "6"

def test070():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [
                            BinaryOp(
                                IntegerLiteral(123),
                                ">>",
                                FunctionCall(Identifier("int2str"), [])
                            )
                        ]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "123"

def test071():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [
                            BinaryOp(
                                StringLiteral("Hello, "),
                                "+",
                                StringLiteral("world!")
                            )
                        ]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "Hello, world!"

def test072():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("i", IntType(), IntegerLiteral(0)),
                    WhileStmt(
                        BinaryOp(Identifier("i"), "<", IntegerLiteral(5)),
                        BlockStmt([
                            IfStmt(
                                BinaryOp(Identifier("i"), "==", IntegerLiteral(2)),
                                BlockStmt([Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1))), ContinueStmt()]),
                                [],
                                None
                            ),
                            IfStmt(
                                BinaryOp(Identifier("i"), "==", IntegerLiteral(4)),
                                BlockStmt([BreakStmt()]),
                                [],
                                None
                            ),
                            ExprStmt(FunctionCall(
                                Identifier("print"),
                                [FunctionCall(Identifier("int2str"), [Identifier("i")])]
                            )),
                            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                        ])
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "0\n1\n3"


def test073():
    ast = Program(
        [ConstDecl("PI", FloatType(), FloatLiteral(3.14))],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(10)),
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("int2str"), [Identifier("x")])]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "10"

def test074():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("bool2str"), [BooleanLiteral(False)])]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "false"

def test075():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("float2str"), [FloatLiteral(-2.5)])]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "-2.5"

def test076():
    ast = Program(
        [ConstDecl("X", IntType(), IntegerLiteral(100))],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ConstDecl("X", IntType(), IntegerLiteral(5)),
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("int2str"), [Identifier("X")])]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "5"

def test077():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("score", IntType(), IntegerLiteral(85)),
                    IfStmt(
                        BinaryOp(Identifier("score"), ">=", IntegerLiteral(90)),
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("A")]))]),
                        [
                            (BinaryOp(Identifier("score"), ">=", IntegerLiteral(80)),
                             BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("B")]))]))
                        ],
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("C")]))])
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "B"

def test078():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", BoolType(), BooleanLiteral(True)),
                    VarDecl("b", BoolType(), BooleanLiteral(False)),
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("bool2str"),
                            [BinaryOp(
                                BinaryOp(Identifier("a"), "&&", Identifier("b")),
                                "||",
                                UnaryOp("!", Identifier("b"))
                            )]
                        )]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "true"

def test079():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("bool2str"),
                            [BinaryOp(IntegerLiteral(5), "<", IntegerLiteral(10))]
                        )]
                    )),
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("bool2str"),
                            [BinaryOp(StringLiteral("abcd"), ">", StringLiteral("abc"))]
                        )]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "true\ntrue"

def test080():
    ast = Program(
        [],
        [
            FuncDecl(
                "get42", [], IntType(),
                [ReturnStmt(IntegerLiteral(42))]
            ),
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [FunctionCall(Identifier("int2str"),
                            [FunctionCall(Identifier("get42"), [])]
                        )]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "42"

def test081():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(5)),
                    IfStmt(
                        BinaryOp(Identifier("x"), ">", IntegerLiteral(0)),
                        BlockStmt([
                            IfStmt(
                                BinaryOp(Identifier("x"), ">", IntegerLiteral(10)),
                                BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("big")]))]),
                                [],
                                BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("small")]))])
                            )
                        ]),
                        [],
                        None
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "small"

def test082():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [
                            BinaryOp(
                                BinaryOp(
                                    IntegerLiteral(5),
                                    "+",
                                    IntegerLiteral(7)
                                ),
                                ">>",
                                FunctionCall(Identifier("int2str"), [])
                            )
                        ]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "12"

def test083():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("name", StringType(), StringLiteral("HLang")),
                    ExprStmt(FunctionCall(
                        Identifier("print"),
                        [
                            BinaryOp(
                                BinaryOp(StringLiteral("Hello, "), "+", Identifier("name")),
                                "+",
                                StringLiteral("!")
                            )
                        ]
                    ))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "Hello, HLang!"

def test084():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    IfStmt(
                        BooleanLiteral(True),
                        BlockStmt([ReturnStmt()]),
                        [],
                        None
                    ),
                    ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("should not print")]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == ""

def test085():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(10)),
                    ExprStmt(FunctionCall(Identifier("print"),
                                          [FunctionCall(Identifier("int2str"), [Identifier("x")])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "10"

def test086():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", IntType(), IntegerLiteral(5)),
                    Assignment(IdLValue("a"), BinaryOp(Identifier("a"), "*", IntegerLiteral(2))),
                    ExprStmt(FunctionCall(Identifier("print"),
                                          [FunctionCall(Identifier("int2str"), [Identifier("a")])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "10"

def test087():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("count", IntType(), IntegerLiteral(5)),
                    WhileStmt(
                        BinaryOp(Identifier("count"), ">", IntegerLiteral(0)),
                        BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("loop")])),
                            Assignment(IdLValue("count"), BinaryOp(Identifier("count"), "-", IntegerLiteral(1)))
                        ])
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "loop\nloop\nloop\nloop\nloop"

def test088():
    ast = Program(
        [],
        [
            FuncDecl(
                "is_even", [Param("n", IntType())], BoolType(),
                [
                    ReturnStmt(BinaryOp(BinaryOp(Identifier("n"), "%", IntegerLiteral(2)), "==", IntegerLiteral(0)))
                ]
            ),
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"),
                                                                            [FunctionCall(Identifier("is_even"), [IntegerLiteral(4)])])])),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"),
                                                                            [FunctionCall(Identifier("is_even"), [IntegerLiteral(5)])])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "true\nfalse"

def test089():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"),
                                          [BinaryOp(StringLiteral("A"), "+", StringLiteral("B"))]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "AB"

def test090():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(1)),
                    IfStmt(
                        BinaryOp(Identifier("x"), "==", IntegerLiteral(1)),
                        BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("one")]))
                        ]),
                        [],
                        None
                    ),
                    IfStmt(
                        BinaryOp(Identifier("x"), "==", IntegerLiteral(2)),
                        BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("two")]))
                        ]),
                        [],
                        None
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "one"

def test091():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("i", IntType(), IntegerLiteral(0)),
                    WhileStmt(
                        BinaryOp(Identifier("i"), "<", IntegerLiteral(5)),
                        BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"),
                                                  [FunctionCall(Identifier("int2str"), [Identifier("i")])])),
                            IfStmt(
                                BinaryOp(Identifier("i"), "==", IntegerLiteral(2)),
                                BlockStmt([BreakStmt()]),
                                [],
                                None
                            ),
                            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                        ])
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "0\n1\n2"

def test092():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("s1", StringType(), StringLiteral("test")),
                    VarDecl("s2", StringType(), StringLiteral("Test")),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"), [BinaryOp(Identifier("s1"), "==", Identifier("s2"))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "false"


def test093():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"),
                                                                            [BinaryOp(IntegerLiteral(5), "*", IntegerLiteral(5))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "25"


def test094():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(10)),
                    ExprStmt(FunctionCall(Identifier("print"),
                                          [FunctionCall(Identifier("int2str"), [BinaryOp(Identifier("x"), "/", IntegerLiteral(2))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "5"

def test095():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("y", IntType(), IntegerLiteral(10)),
                    WhileStmt(
                        BinaryOp(Identifier("y"), ">", IntegerLiteral(0)),
                        BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("y")])])),
                            Assignment(IdLValue("y"), BinaryOp(Identifier("y"), "-", IntegerLiteral(2)))
                        ])
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "10\n8\n6\n4\n2"

def test096():
    ast = Program(
        [],
        [
            FuncDecl(
                "get_string", [], StringType(),
                [
                    ReturnStmt(StringLiteral("from function"))
                ]
            ),
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("get_string"), [])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "from function"

def test097():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(10)),
                    IfStmt(
                        BinaryOp(Identifier("x"), "<=", IntegerLiteral(10)),
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("less or equal")]))]),
                        [],
                        None
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "less or equal"


def test098():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("s", StringType(), StringLiteral("test")),
                    ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(Identifier("s"), "+", StringLiteral("123"))]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "test123"

def test099():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"),
                                                                            [BinaryOp(UnaryOp("-", IntegerLiteral(10)), "+", IntegerLiteral(20))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "10"

def test100():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    IfStmt(
                        BinaryOp(BooleanLiteral(True), "&&", BooleanLiteral(True)),
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("both true")]))]),
                        [],
                        None
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "both true"

def test101():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"),
                                                                            [BinaryOp(IntegerLiteral(15), "%", IntegerLiteral(4))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "3"


def test102():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("s", StringType(), StringLiteral("test")),
                    IfStmt(
                        BinaryOp(Identifier("s"), "==", StringLiteral("test")),
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("equal")]))]),
                        [],
                        None
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "equal"

def test103():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [BinaryOp(IntegerLiteral(100), "-", IntegerLiteral(50))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "50"

def test104():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [BinaryOp(IntegerLiteral(2), "*", IntegerLiteral(20))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "40"

def test105():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [BinaryOp(IntegerLiteral(40), "/", IntegerLiteral(8))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "5"

def test106():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"), [BinaryOp(IntegerLiteral(10), "!=", IntegerLiteral(10))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "false"

def test107():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("bool2str"),
                                                                            [BinaryOp(BooleanLiteral(True), "||", BooleanLiteral(False))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "true"

def test108():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("count", IntType(), IntegerLiteral(3)),
                    WhileStmt(
                        BinaryOp(Identifier("count"), ">", IntegerLiteral(0)),
                        BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("count")])])),
                            Assignment(IdLValue("count"), BinaryOp(Identifier("count"), "-", IntegerLiteral(1)))
                        ])
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "3\n2\n1"

def test109():
    ast = Program(
        [],
        [
            FuncDecl(
                "add_one", [Param("x", IntType())], IntType(),
                [ReturnStmt(BinaryOp(Identifier("x"), "+", IntegerLiteral(1)))]
            ),
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", IntType(), IntegerLiteral(10)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [FunctionCall(Identifier("add_one"), [Identifier("a")])])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "11"

def test110():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"),
                                          [FunctionCall(Identifier("int2str"), [BinaryOp(IntegerLiteral(1), "==", IntegerLiteral(1))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "1"

def test111():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"),
                                                                            [BinaryOp(IntegerLiteral(5), ">", IntegerLiteral(3))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "1"

def test112():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"),
                                                                            [BinaryOp(IntegerLiteral(5), "<", IntegerLiteral(3))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "0"

def test113():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("a", IntType(), IntegerLiteral(10)),
                    VarDecl("b", IntType(), IntegerLiteral(20)),
                    IfStmt(
                        BinaryOp(Identifier("a"), "==", Identifier("b")),
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("equal")]))]),
                        [
                            (BinaryOp(Identifier("a"), "!=", Identifier("b")),
                             BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("not equal")]))]))
                        ],
                        None
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "not equal"

def test114():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("i", IntType(), IntegerLiteral(0)),
                    WhileStmt(
                        BinaryOp(Identifier("i"), "<", IntegerLiteral(5)),
                        BlockStmt([
                            IfStmt(
                                BinaryOp(Identifier("i"), "==", IntegerLiteral(3)),
                                BlockStmt([BreakStmt()]),
                                [],
                                None
                            ),
                            ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("int2str"), [Identifier("i")])])),
                            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                        ])
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "0\n1\n2"


def test115():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    ExprStmt(FunctionCall(Identifier("print"),
                                          [BinaryOp(BinaryOp(StringLiteral("A"), "+", StringLiteral("B")), "+", StringLiteral("C"))]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "ABC"

def test116():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("x", FloatType(), FloatLiteral(10.5)),
                    ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("float2str"), [BinaryOp(Identifier("x"), "*", FloatLiteral(2.0))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "21.0"

def test117():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("i", IntType(), IntegerLiteral(0)),
                    WhileStmt(
                        BinaryOp(Identifier("i"), "<", IntegerLiteral(3)),
                        BlockStmt([
                            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Hello")])),
                            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                        ])
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "Hello\nHello\nHello"

def test118():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("x", BoolType(), BooleanLiteral(True)),
                    VarDecl("y", BoolType(), BooleanLiteral(False)),
                    IfStmt(
                        BinaryOp(Identifier("x"), "&&", Identifier("y")),
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("true")]))]),
                        [],
                        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("false")]))])
                    )
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "false"

def test119():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(10)),
                    VarDecl("y", IntType(), IntegerLiteral(20)),
                    ExprStmt(FunctionCall(Identifier("print"),
                                          [FunctionCall(Identifier("int2str"), [BinaryOp(Identifier("x"), "+", Identifier("y"))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "30"

def test120():
    ast = Program(
        [],
        [
            FuncDecl(
                "main", [], VoidType(),
                [
                    VarDecl("x", IntType(), IntegerLiteral(10)),
                    VarDecl("y", IntType(), IntegerLiteral(20)),
                    ExprStmt(FunctionCall(Identifier("print"),
                                          [FunctionCall(Identifier("int2str"), [BinaryOp(Identifier("x"), "+", Identifier("y"))])]))
                ]
            )
        ]
    )
    result = CodeGenerator().generate_and_run(ast)
    assert result == "30"