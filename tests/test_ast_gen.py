from utils import ASTGenerator

def test_100():
    """Test integer literal"""
    source = "func main() -> void { let x = 1; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, IntegerLiteral(1))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_101():
    """Test float literal"""
    source = "func main() -> void { let x = 1.696969; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, FloatLiteral(1.696969))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_102():
    """Test boolean literal"""
    source = "func main() -> void { let x = true; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, BooleanLiteral(True))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_103():
    """Test string literal"""
    source = "func main() -> void { let x = \"abc\"; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, StringLiteral('abc'))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_104():
    """Test identifier expression"""
    source = "func main() -> void { let x = y; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, Identifier(y))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_105():
    """Test unary minus expression"""
    source = "func main() -> void { let x = -1; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, UnaryOp(-, IntegerLiteral(1)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_106():
    """Test binary addition expression"""
    source = "func main() -> void { let x = 1 + 2; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, BinaryOp(IntegerLiteral(1), +, IntegerLiteral(2)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_107():
    """Test nested binary expression with precedence"""
    source = "func main() -> void { let x = 1 + 2 * 3; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, BinaryOp(IntegerLiteral(1), +, BinaryOp(IntegerLiteral(2), *, IntegerLiteral(3))))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_108():
    """Test parenthesized binary expression"""
    source = "func main() -> void { let x = (1 + 2) * 3; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, BinaryOp(BinaryOp(IntegerLiteral(1), +, IntegerLiteral(2)), *, IntegerLiteral(3)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_109():
    """Test simple array literal"""
    source = "func main() -> void { let x = [1, 2]; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_110():
    """Test array access"""
    source = "func main() -> void { let x = arr[0]; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, ArrayAccess(Identifier(arr), IntegerLiteral(0)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_111():
    """Test const decl with type"""
    source = "const PI: float = 3.14;"
    expected = "Program(consts=[ConstDecl(PI, float, FloatLiteral(3.14))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_112():
    """Test const decl without type"""
    source = "const MAX = 100;"
    expected = "Program(consts=[ConstDecl(MAX, IntegerLiteral(100))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_113():
    """Test assignment to identifier"""
    source = "func main() -> void { x = 5; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [Assignment(IdLValue(x), IntegerLiteral(5))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_114():
    """Test assignment to array access"""
    source = "func main() -> void { x[1] = 10; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [Assignment(ArrayAccessLValue(Identifier(x), IntegerLiteral(1)), IntegerLiteral(10))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_115():
    """Test subtraction operator"""
    source = "func main() -> void { let x = 5 - 3; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, BinaryOp(IntegerLiteral(5), -, IntegerLiteral(3)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_116():
    """Test division operator"""
    source = "func main() -> void { let x = 6 / 2; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, BinaryOp(IntegerLiteral(6), /, IntegerLiteral(2)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_117():
    """Test modulo operator"""
    source = "func main() -> void { let x = 7 % 4; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, BinaryOp(IntegerLiteral(7), %, IntegerLiteral(4)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_118():
    """Test equality operator"""
    source = "func main() -> void { let x = a == b; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, BinaryOp(Identifier(a), ==, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_119():
    """Test inequality operator"""
    source = "func main() -> void { let x = a != b; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, BinaryOp(Identifier(a), !=, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_120():
    """Test greater than operator"""
    source = "func main() -> void { let x = a > b; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, BinaryOp(Identifier(a), >, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_121():
    """Test greater than or equal operator"""
    source = "func main() -> void { let x = a >= b; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, BinaryOp(Identifier(a), >=, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_122():
    """Test less than operator"""
    source = "func main() -> void { let x = a < b; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, BinaryOp(Identifier(a), <, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_123():
    """Test less than or equal operator"""
    source = "func main() -> void { let x = a <= b; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, BinaryOp(Identifier(a), <=, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_124():
    """Test logical AND operator"""
    source = "func main() -> void { let x = a && b; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, BinaryOp(Identifier(a), &&, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_125():
    """Test logical OR operator"""
    source = "func main() -> void { let x = a || b; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, BinaryOp(Identifier(a), ||, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_126():
    """Test logical NOT operator"""
    source = "func main() -> void { let x = !a; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, UnaryOp(!, Identifier(a)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_127():
    """Test pipeline operator (>>)"""
    source = "func main() -> void { let x = a >> b; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, BinaryOp(Identifier(a), >>, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_128():
    """Test nested unary and binary operators"""
    source = "func main() -> void { let x = !a && b; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, BinaryOp(UnaryOp(!, Identifier(a)), &&, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_129():
    """Test multiple arithmetic operations"""
    source = "func main() -> void { let x = a + b - c; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, BinaryOp(BinaryOp(Identifier(a), +, Identifier(b)), -, Identifier(c)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_130():
    """Test expression statement"""
    source = "func main() -> void { foo(); }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [ExprStmt(FunctionCall(Identifier(foo), []))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_131():
    """Test return with value"""
    source = "func main() -> int { return 1; }"
    expected = "Program(funcs=[FuncDecl(main, [], int, [ReturnStmt(IntegerLiteral(1))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_132():
    """Test return without value"""
    source = "func main() -> void { return; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [ReturnStmt()])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_133():
    """Test break statement"""
    source = "func main() -> void { break; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [BreakStmt()])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_134():
    """Test continue statement"""
    source = "func main() -> void { continue; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [ContinueStmt()])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_135():
    """Test simple if statement"""
    source = "func main() -> void { if (a) { return; } }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[IfStmt(condition=Identifier(a), then_stmt=BlockStmt([ReturnStmt()]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_136():
    """Test if-else statement"""
    source = "func main() -> void { if (a) { return; } else { break; } }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, [IfStmt(condition=Identifier(a), "
                "then_stmt=BlockStmt([ReturnStmt()]), else_stmt=BlockStmt([BreakStmt()]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_137():
    """Test if-elif-else statement"""
    source = """
    func main() -> void {
        if (a) { return; }
        else if (b) { continue; }
        else { break; }
    }
    """
    expected = ("Program(funcs=[FuncDecl(main, [], void, [IfStmt(condition=Identifier(a), "
                "then_stmt=BlockStmt([ReturnStmt()]), "
                "elif_branches=[(Identifier(b), BlockStmt([ContinueStmt()]))], "
                "else_stmt=BlockStmt([BreakStmt()]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_138():
    """Test while loop"""
    source = "func main() -> void { while (x < 10) { x = x + 1; } }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[WhileStmt(BinaryOp(Identifier(x), <, IntegerLiteral(10)), "
                "BlockStmt([Assignment(IdLValue(x), BinaryOp(Identifier(x), +, IntegerLiteral(1)))]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_139():
    """Test for loop"""
    source = "func main() -> void { for (i in arr) { return; } }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[ForStmt(i, Identifier(arr), BlockStmt([ReturnStmt()]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_140():
    """Test empty block statement"""
    source = "func main() -> void { {} }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [BlockStmt([])])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_141():
    """Test block statement with multiple statements"""
    source = "func main() -> void { { let x = 1; let y = 2; } }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[BlockStmt([VarDecl(x, IntegerLiteral(1)), VarDecl(y, IntegerLiteral(2))])])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_142():
    """Test array literal"""
    source = "func main() -> void { let a = [1, 2]; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[VarDecl(a, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_143():
    """Test nested array literal"""
    source = "func main() -> void { let a = [[1, 2], [3, 4]]; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[VarDecl(a, ArrayLiteral([ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), "
                "ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4)])]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_144():
    """Test FuncDecl with parameters"""
    source = "func add(a: int, b: float) -> int { return 0; }"
    expected = ("Program(funcs=[FuncDecl(add, [Param(a, int), Param(b, float)], int, "
                "[ReturnStmt(IntegerLiteral(0))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_145():
    """Test FuncDecl returning void with empty body"""
    source = "func empty() -> void {}"
    expected = "Program(funcs=[FuncDecl(empty, [], void, [])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_146():
    """Test FuncDecl without parameters"""
    source = "func hello() -> string { return \"hi\"; }"
    expected = ("Program(funcs=[FuncDecl(hello, [], string, "
                "[ReturnStmt(StringLiteral('hi'))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_147():
    """Test array access LValue with two indices"""
    source = "func main() -> void { x[0][1] = 10; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[Assignment(ArrayAccessLValue(ArrayAccess(Identifier(x), IntegerLiteral(0)), "
                "IntegerLiteral(1)), IntegerLiteral(10))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_148():
    """Test string + int (string concat)"""
    source = "func main() -> void { let x = \"count: \" + 1; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[VarDecl(x, BinaryOp(StringLiteral('count: '), +, IntegerLiteral(1)))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_149():
    """Test function call with arguments"""
    source = "func main() -> void { foo(1, 2); }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[ExprStmt(FunctionCall(Identifier(foo), [IntegerLiteral(1), IntegerLiteral(2)]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_150():
    """Test nested function calls"""
    source = "func main() -> void { print(str(123)); }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[ExprStmt(FunctionCall(Identifier(print), "
                "[FunctionCall(Identifier(str), [IntegerLiteral(123)])]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_151():
    """Test function call with pipeline operator"""
    source = "func main() -> void { let x = data >> clean >> normalize; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[VarDecl(x, BinaryOp(BinaryOp(Identifier(data), >>, Identifier(clean)), >>, Identifier(normalize)))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_152():
    """Test deeply nested function call"""
    source = "func main() -> void { let x = a(b(c(1))); }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[VarDecl(x, FunctionCall(Identifier(a), [FunctionCall(Identifier(b), [FunctionCall(Identifier(c), [IntegerLiteral(1)])])]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_153():
    """Test type cast with str()"""
    source = "func main() -> void { let s = str(123); }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[VarDecl(s, FunctionCall(Identifier(str), [IntegerLiteral(123)]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_154():
    """Test array literal empty"""
    source = "func main() -> void { let x = []; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[VarDecl(x, ArrayLiteral([]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_155():
    """Test array access multiple layers"""
    source = "func main() -> void { let x = m[0][1][2]; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[VarDecl(x, ArrayAccess(ArrayAccess(ArrayAccess(Identifier(m), IntegerLiteral(0)), IntegerLiteral(1)), IntegerLiteral(2)))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_156():
    """Test if with no else or elif"""
    source = "func main() -> void { if (true) { let x = 1; } }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[IfStmt(condition=BooleanLiteral(True), "
                "then_stmt=BlockStmt([VarDecl(x, IntegerLiteral(1))]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_157():
    """Test if with elif but no else"""
    source = """
    func main() -> void {
        if (a) { return; }
        else if (b) { break; }
    }
    """
    expected = ("Program(funcs=[FuncDecl(main, [], void, [IfStmt(condition=Identifier(a), "
                "then_stmt=BlockStmt([ReturnStmt()]), "
                "elif_branches=[(Identifier(b), BlockStmt([BreakStmt()]))])])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_158():
    """Test if with empty else block"""
    source = """
    func main() -> void {
        if (a) { return; }
        else {}
    }
    """
    expected = ("Program(funcs=[FuncDecl(main, [], void, [IfStmt(condition=Identifier(a), "
                "then_stmt=BlockStmt([ReturnStmt()]), else_stmt=BlockStmt([]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_159():
    """Test nested if-else inside block"""
    source = """
    func main() -> void {
        if (a) {
            if (b) { return; }
        }
    }
    """
    expected = ("Program(funcs=[FuncDecl(main, [], void, [IfStmt(condition=Identifier(a), "
                "then_stmt=BlockStmt([IfStmt(condition=Identifier(b), "
                "then_stmt=BlockStmt([ReturnStmt()]))]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_160():
    """Test nested return inside if-else block"""
    source = """
    func main() -> void {
        if (x > 0) {
            return;
        } else {
            return;
        }
    }
    """
    expected = ("Program(funcs=[FuncDecl(main, [], void, [IfStmt(condition=BinaryOp(Identifier(x), >, IntegerLiteral(0)), "
                "then_stmt=BlockStmt([ReturnStmt()]), else_stmt=BlockStmt([ReturnStmt()]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_161():
    """Test str concat with nested function call"""
    source = "func main() -> void { let x = \"Result: \" + str(42); }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[VarDecl(x, BinaryOp(StringLiteral('Result: '), +, FunctionCall(Identifier(str), [IntegerLiteral(42)])))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_162():
    """Test multi-block inside for-loop"""
    source = "func main() -> void { for (x in arr) { { return; } } }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[ForStmt(x, Identifier(arr), BlockStmt([BlockStmt([ReturnStmt()])]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_163():
    """Test nested function call with array access"""
    source = "func main() -> void { let x = print(data[0]); }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[VarDecl(x, FunctionCall(Identifier(print), [ArrayAccess(Identifier(data), IntegerLiteral(0))]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_164():
    """Test type cast nested (str(int(x)))"""
    source = "func main() -> void { let x = foo(foo(y)); }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[VarDecl(x, FunctionCall(Identifier(foo), "
                "[FunctionCall(Identifier(foo), [Identifier(y)])]))])])")
    assert str(ASTGenerator(source).generate()) == expected


    assert str(ASTGenerator(source).generate()) == expected

def test_166():
    """Test empty function with only break"""
    source = "func main() -> void { break; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [BreakStmt()])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_167():
    """Test continue in nested if"""
    source = "func main() -> void { if (true) { continue; } }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, [IfStmt(condition=BooleanLiteral(True), "
                "then_stmt=BlockStmt([ContinueStmt()]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_168():
    """Test binary string concat multiple"""
    source = "func main() -> void { let x = \"a\" + \"b\" + \"c\"; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, "
                "BinaryOp(BinaryOp(StringLiteral('a'), +, StringLiteral('b')), +, StringLiteral('c')))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_169():
    """Test identifier as function argument"""
    source = "func main() -> void { f(x); }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, [ExprStmt("
                "FunctionCall(Identifier(f), [Identifier(x)]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_170():
    """Test bool literal false"""
    source = "func main() -> void { let x = false; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[VarDecl(x, BooleanLiteral(False))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_171():
    """Test chained assignment with array"""
    source = "func main() -> void { a[1] = b[2] + 5; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, [Assignment("
                "ArrayAccessLValue(Identifier(a), IntegerLiteral(1)), "
                "BinaryOp(ArrayAccess(Identifier(b), IntegerLiteral(2)), +, IntegerLiteral(5)))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_1000():
    """Test complex expression with all operators"""
    source = """
    func complexExpr(a: int, b: int, c: int) -> bool {
        return a + b * c > 0 && (a < b || c != 0);
    }
    """
    expected = "Program(funcs=[FuncDecl(complexExpr, [Param(a, int), Param(b, int), Param(c, int)], bool, [ReturnStmt(BinaryOp(BinaryOp(BinaryOp(Identifier(a), +, BinaryOp(Identifier(b), *, Identifier(c))), >, IntegerLiteral(0)), &&, BinaryOp(BinaryOp(Identifier(a), <, Identifier(b)), ||, BinaryOp(Identifier(c), !=, IntegerLiteral(0)))))])])";
    assert str(ASTGenerator(source).generate()) == expected

def test_172():
    """Test array type declaration"""
    source = "func main() -> void { let x: [int; 3] = [1, 2, 3]; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, [int; 3], "
                "ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]))])])")
    assert str(ASTGenerator(source).generate()) == expected
  
def test_173():
    """Test multidimensional array literal"""
    source = "func main() -> void { let x = [[1, 2], [3, 4]]; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, "
                "ArrayLiteral([ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), "
                "ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4)])]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_174():
    """Test nested array access and assignment"""
    source = "func main() -> void { matrix[1][2] = 99; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[Assignment(ArrayAccessLValue(ArrayAccess(Identifier(matrix), IntegerLiteral(1)), IntegerLiteral(2)), IntegerLiteral(99))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_175():
    """Test array passed as function argument"""
    source = "func main() -> void { print(arr[0]); }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[ExprStmt(FunctionCall(Identifier(print), [ArrayAccess(Identifier(arr), IntegerLiteral(0))]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_176():
    """Test const declaration with array"""
    source = "const A: [int; 2] = [10, 20];"
    expected = ("Program(consts=[ConstDecl(A, [int; 2], "
                "ArrayLiteral([IntegerLiteral(10), IntegerLiteral(20)]))])")
    assert str(ASTGenerator(source).generate()) == expected

def test_177():
    """Test function returning array"""
    source = "func getNums() -> [int; 3] { return [1, 2, 3]; }"
    expected = ("Program(funcs=[FuncDecl(getNums, [], [int; 3], "
                "[ReturnStmt(ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_178():
    """Test assignment with function returning array"""
    source = "func main() -> void { let x = getNums()[1]; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[VarDecl(x, ArrayAccess(FunctionCall(Identifier(getNums), []), IntegerLiteral(1)))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_179():
    """Test nested function + array access"""
    source = "func main() -> void { let x = f()[0][1]; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[VarDecl(x, ArrayAccess(ArrayAccess(FunctionCall(Identifier(f), []), IntegerLiteral(0)), IntegerLiteral(1)))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_180():
    """Test array pipeline chain"""
    source = "func main() -> void { let x = arr >> map >> flatten >> print; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[VarDecl(x, BinaryOp(BinaryOp(BinaryOp(Identifier(arr), >>, Identifier(map)), >>, Identifier(flatten)), >>, Identifier(print)))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_181():
    """Test array used in binary expression"""
    source = "func main() -> void { let x = arr[0] + arr[1]; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, "
                "BinaryOp(ArrayAccess(Identifier(arr), IntegerLiteral(0)), +, ArrayAccess(Identifier(arr), IntegerLiteral(1))))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_182():
    """Test array assigned to array index"""
    source = "func main() -> void { a[0] = b[1]; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, [Assignment("
                "ArrayAccessLValue(Identifier(a), IntegerLiteral(0)), "
                "ArrayAccess(Identifier(b), IntegerLiteral(1)))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_183():
    """Test array inside return"""
    source = "func main() -> [int; 2] { return [0, 1]; }"
    expected = ("Program(funcs=[FuncDecl(main, [], [int; 2], "
                "[ReturnStmt(ArrayLiteral([IntegerLiteral(0), IntegerLiteral(1)]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_184():
    """Test nested array assignment"""
    source = "func main() -> void { a[0][1] = b[2][3]; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, [Assignment("
                "ArrayAccessLValue(ArrayAccess(Identifier(a), IntegerLiteral(0)), IntegerLiteral(1)), "
                "ArrayAccess(ArrayAccess(Identifier(b), IntegerLiteral(2)), IntegerLiteral(3)))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_185():
    """Test array access with expression index"""
    source = "func main() -> void { x[a + 1] = 99; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, [Assignment("
                "ArrayAccessLValue(Identifier(x), BinaryOp(Identifier(a), +, IntegerLiteral(1))), "
                "IntegerLiteral(99))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_186():
    """Test const of array without type annotation"""
    source = "const B = [true, false];"
    expected = ("Program(consts=[ConstDecl(B, ArrayLiteral([BooleanLiteral(True), BooleanLiteral(False)]))])")
    assert str(ASTGenerator(source).generate()) == expected

def test_187():
    """Test function that returns array access"""
    source = "func get() -> int { return a[0]; }"
    expected = ("Program(funcs=[FuncDecl(get, [], int, "
                "[ReturnStmt(ArrayAccess(Identifier(a), IntegerLiteral(0)))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_188():
    """Test array as part of binary op with literal"""
    source = "func main() -> void { let x = arr[0] * 2; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[VarDecl(x, BinaryOp(ArrayAccess(Identifier(arr), IntegerLiteral(0)), *, IntegerLiteral(2)))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_189():
    """Test multi-function with shared array const"""
    source = """
    const N: [int; 3] = [1, 2, 3];
    func main() -> void { print(N[0]); }
    """
    expected = ("Program(consts=[ConstDecl(N, [int; 3], "
                "ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]))], "
                "funcs=[FuncDecl(main, [], void, "
                "[ExprStmt(FunctionCall(Identifier(print), [ArrayAccess(Identifier(N), IntegerLiteral(0))]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_190():
    """Test assignment to deeply indexed array"""
    source = "func main() -> void { grid[1][2][3] = 1; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, [Assignment("
                "ArrayAccessLValue(ArrayAccess(ArrayAccess(Identifier(grid), IntegerLiteral(1)), IntegerLiteral(2)), IntegerLiteral(3)), "
                "IntegerLiteral(1))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_191():
    """Test return binary op between array access and literal"""
    source = "func main() -> bool { return arr[0] == 1; }"
    expected = ("Program(funcs=[FuncDecl(main, [], bool, "
                "[ReturnStmt(BinaryOp(ArrayAccess(Identifier(arr), IntegerLiteral(0)), ==, IntegerLiteral(1)))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_192():
    """Test if with array access condition"""
    source = "func main() -> void { if (flags[0]) { return; } }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, "
                "[IfStmt(condition=ArrayAccess(Identifier(flags), IntegerLiteral(0)), "
                "then_stmt=BlockStmt([ReturnStmt()]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_193():
    """Test pipeline with function call"""
    source = "func main() -> void { data >> process(1, 2); }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, [ExprStmt("
                "BinaryOp(Identifier(data), >>, FunctionCall(Identifier(process), [IntegerLiteral(1), IntegerLiteral(2)])))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_194():
    """Test function return pipeline expression"""
    source = "func chain(x: int) -> int { return x >> double >> inc; }"
    expected = ("Program(funcs=[FuncDecl(chain, [Param(x, int)], int, "
                "[ReturnStmt(BinaryOp(BinaryOp(Identifier(x), >>, Identifier(double)), >>, Identifier(inc)))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_195():
    """Test complex array+function call+binary op"""
    source = "func main() -> void { let x = get()[0] + arr[1]; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, "
                "BinaryOp(ArrayAccess(FunctionCall(Identifier(get), []), IntegerLiteral(0)), +, "
                "ArrayAccess(Identifier(arr), IntegerLiteral(1))))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_196():
    """Test nested if with return inside"""
    source = "func main() -> void { if (x) { if (y) { return; } } }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, [IfStmt(condition=Identifier(x), "
                "then_stmt=BlockStmt([IfStmt(condition=Identifier(y), "
                "then_stmt=BlockStmt([ReturnStmt()]))]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_197():
    """Test return nested function call"""
    source = "func main() -> int { return sum(get(1)); }"
    expected = ("Program(funcs=[FuncDecl(main, [], int, "
                "[ReturnStmt(FunctionCall(Identifier(sum), [FunctionCall(Identifier(get), [IntegerLiteral(1)])]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_198():
    """Test assignment with str(...) + array access"""
    source = "func main() -> void { s = str(arr[0]) + \"!\"; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, [Assignment("
                "IdLValue(s), BinaryOp(FunctionCall(Identifier(str), [ArrayAccess(Identifier(arr), IntegerLiteral(0))]), +, StringLiteral('!')))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_199():
    """Test for loop over function call result"""
    source = "func main() -> void { for (x in getItems()) { print(x); } }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, [ForStmt(x, FunctionCall(Identifier(getItems), []), "
                "BlockStmt([ExprStmt(FunctionCall(Identifier(print), [Identifier(x)]))]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_200():
    """Test return array access in complex expression"""
    source = "func main() -> int { return (arr[0] + arr[1]) * 2; }"
    expected = ("Program(funcs=[FuncDecl(main, [], int, "
                "[ReturnStmt(BinaryOp(BinaryOp(ArrayAccess(Identifier(arr), IntegerLiteral(0)), +, "
                "ArrayAccess(Identifier(arr), IntegerLiteral(1))), *, IntegerLiteral(2)))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_201():
    """Test sum of array elements"""
    source = """
    func sum(arr: [int; 5]) -> int {
        let s = 0;
        for (x in arr) {
            s = s + x;
        }
        return s;
    }
    """
    expected = (
        "Program(funcs=[FuncDecl(sum, [Param(arr, [int; 5])], int, ["
        "VarDecl(s, IntegerLiteral(0)), "
        "ForStmt(x, Identifier(arr), BlockStmt([Assignment(IdLValue(s), BinaryOp(Identifier(s), +, Identifier(x)))])), "
        "ReturnStmt(Identifier(s))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_202():
    """Test count even numbers in array"""
    source = """
    func countEven(arr: [int; 10]) -> int {
        let c = 0;
        for (x in arr) {
            if (x % 2 == 0) {
                c = c + 1;
            }
        }
        return c;
    }
    """
    expected = (
        "Program(funcs=[FuncDecl(countEven, [Param(arr, [int; 10])], int, ["
        "VarDecl(c, IntegerLiteral(0)), "
        "ForStmt(x, Identifier(arr), BlockStmt(["
        "IfStmt(condition=BinaryOp(BinaryOp(Identifier(x), %, IntegerLiteral(2)), ==, IntegerLiteral(0)), "
        "then_stmt=BlockStmt([Assignment(IdLValue(c), BinaryOp(Identifier(c), +, IntegerLiteral(1)))])"
        ")])), "
        "ReturnStmt(Identifier(c))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_203():
    """Test find max in array"""
    source = """
    func max(arr: [int; 5]) -> int {
        let m = arr[0];
        for (x in arr) {
            if (x > m) {
                m = x;
            }
        }
        return m;
    }
    """
    expected = (
        "Program(funcs=[FuncDecl(max, [Param(arr, [int; 5])], int, ["
        "VarDecl(m, ArrayAccess(Identifier(arr), IntegerLiteral(0))), "
        "ForStmt(x, Identifier(arr), BlockStmt(["
        "IfStmt(condition=BinaryOp(Identifier(x), >, Identifier(m)), "
        "then_stmt=BlockStmt([Assignment(IdLValue(m), Identifier(x))])"
        ")])), "
        "ReturnStmt(Identifier(m))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_204():
    """Test isPrime function"""
    source = """
    func isPrime(n: int) -> bool {
        if (n < 2) {
            return false;
        }
        for (i in [2, 3, 4, n - 1]) {
            if (n % i == 0) {
                return false;
            }
        }
        return true;
    }
    """
    expected = (
        "Program(funcs=[FuncDecl(isPrime, [Param(n, int)], bool, ["
        "IfStmt(condition=BinaryOp(Identifier(n), <, IntegerLiteral(2)), "
        "then_stmt=BlockStmt([ReturnStmt(BooleanLiteral(False))])), "
        "ForStmt(i, ArrayLiteral([IntegerLiteral(2), IntegerLiteral(3), IntegerLiteral(4), "
        "BinaryOp(Identifier(n), -, IntegerLiteral(1))]), "
        "BlockStmt([IfStmt(condition=BinaryOp(BinaryOp(Identifier(n), %, Identifier(i)), ==, IntegerLiteral(0)), "
        "then_stmt=BlockStmt([ReturnStmt(BooleanLiteral(False))]))])), "
        "ReturnStmt(BooleanLiteral(True))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_205():
    """Test reverse array"""
    source = """
    func reverse(arr: [int; 5]) -> [int; 5] {
        let rev = [0, 0, 0, 0, 0];
        let i = 0;
        for (x in arr) {
            rev[4 - i] = x;
            i = i + 1;
        }
        return rev;
    }
    """
    expected = (
        "Program(funcs=[FuncDecl(reverse, [Param(arr, [int; 5])], [int; 5], ["
        "VarDecl(rev, ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0)])), "
        "VarDecl(i, IntegerLiteral(0)), "
        "ForStmt(x, Identifier(arr), BlockStmt(["
        "Assignment(ArrayAccessLValue(Identifier(rev), BinaryOp(IntegerLiteral(4), -, Identifier(i))), Identifier(x)), "
        "Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1)))"
        "])), "
        "ReturnStmt(Identifier(rev))"
        "])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_206():
    """Test deeply nested arithmetic and comparison"""
    source = "func main() -> bool { return (1 + 2 * 3) < 10 && 4 != 5 || 6 > 7; }"
    expected = (
        "Program(funcs=[FuncDecl(main, [], bool, [ReturnStmt("
        "BinaryOp(BinaryOp(BinaryOp(BinaryOp(IntegerLiteral(1), +, BinaryOp(IntegerLiteral(2), *, IntegerLiteral(3))), <, IntegerLiteral(10)), "
        "&&, BinaryOp(IntegerLiteral(4), !=, IntegerLiteral(5))), ||, BinaryOp(IntegerLiteral(6), >, IntegerLiteral(7)))"
        ")])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_207():
    """Test mix of unary, binary, array access, and function call"""
    source = "func main() -> void { let x = !(a[1] + f(b - 2)); }"
    expected = (
        "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, "
        "UnaryOp(!, BinaryOp(ArrayAccess(Identifier(a), IntegerLiteral(1)), +, "
        "FunctionCall(Identifier(f), [BinaryOp(Identifier(b), -, IntegerLiteral(2))]))))])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_208():
    """Test nested pipeline with binary and call"""
    source = "func main() -> void { let x = data >> filter(a > 1) >> map(b + 2); }"
    expected = (
        "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, "
        "BinaryOp(BinaryOp(Identifier(data), >>, "
        "FunctionCall(Identifier(filter), [BinaryOp(Identifier(a), >, IntegerLiteral(1))])), >>, "
        "FunctionCall(Identifier(map), [BinaryOp(Identifier(b), +, IntegerLiteral(2))])))])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_209():
    """Test combined logic and math with full precedence"""
    source = "func main() -> bool { return a + b * c > d && !(e <= f || g == h); }"
    expected = (
        "Program(funcs=[FuncDecl(main, [], bool, [ReturnStmt("
        "BinaryOp(BinaryOp(BinaryOp(Identifier(a), +, BinaryOp(Identifier(b), *, Identifier(c))), >, Identifier(d)), &&, "
        "UnaryOp(!, BinaryOp(BinaryOp(Identifier(e), <=, Identifier(f)), ||, BinaryOp(Identifier(g), ==, Identifier(h)))))"
        ")])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_210():
    """Test extreme nesting of all expression types"""
    source = 'func main() -> void { let x = !((a[0] >> clean(1)) + str(b[1] * 2)); }'
    expected = (
        "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, "
        "UnaryOp(!, BinaryOp(BinaryOp(ArrayAccess(Identifier(a), IntegerLiteral(0)), >>, "
        "FunctionCall(Identifier(clean), [IntegerLiteral(1)])), +, "
        "FunctionCall(Identifier(str), [BinaryOp(ArrayAccess(Identifier(b), IntegerLiteral(1)), *, IntegerLiteral(2))])))"
        ")])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_211():
    """Test precedence of * over +"""
    source = "func main() -> int { return 1 + 2 * 3; }"
    expected = ("Program(funcs=[FuncDecl(main, [], int, [ReturnStmt("
                "BinaryOp(IntegerLiteral(1), +, BinaryOp(IntegerLiteral(2), *, IntegerLiteral(3)))"
                ")])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_211():
    """Test precedence of * over +"""
    source = "func main() -> int { return 1 + 2 * 3; }"
    expected = ("Program(funcs=[FuncDecl(main, [], int, [ReturnStmt("
                "BinaryOp(IntegerLiteral(1), +, BinaryOp(IntegerLiteral(2), *, IntegerLiteral(3)))"
                ")])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_212():
    """Test unary outside binary"""
    source = "func main() -> bool { return !a == b; }"
    expected = ("Program(funcs=[FuncDecl(main, [], bool, [ReturnStmt("
                "BinaryOp(UnaryOp(!, Identifier(a)), ==, Identifier(b))"
                ")])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_213():
    """Test deep array access"""
    source = "func main() -> int { return a[0][1][2]; }"
    expected = ("Program(funcs=[FuncDecl(main, [], int, [ReturnStmt("
                "ArrayAccess(ArrayAccess(ArrayAccess(Identifier(a), IntegerLiteral(0)), IntegerLiteral(1)), IntegerLiteral(2))"
                ")])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_214():
    """Test function call result array access"""
    source = "func main() -> int { return get()[0]; }"
    expected = ("Program(funcs=[FuncDecl(main, [], int, [ReturnStmt("
                "ArrayAccess(FunctionCall(Identifier(get), []), IntegerLiteral(0))"
                ")])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_215():
    """Test assignment with nested ArrayAccessLValue"""
    source = "func main() -> void { a[0][1] = 99; }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, [Assignment("
                "ArrayAccessLValue(ArrayAccess(Identifier(a), IntegerLiteral(0)), IntegerLiteral(1)), "
                "IntegerLiteral(99))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_216():
    """Test pipeline with function call (with args)"""
    source = "func main() -> void { let x = data >> filter(1) >> map(2); }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, "
                "BinaryOp(BinaryOp(Identifier(data), >>, FunctionCall(Identifier(filter), [IntegerLiteral(1)])), >>, "
                "FunctionCall(Identifier(map), [IntegerLiteral(2)])))])])")
    assert str(ASTGenerator(source).generate()) == expected


def test_218():
    """Test return without expression"""
    source = "func main() -> void { return; }"
    expected = "Program(funcs=[FuncDecl(main, [], void, [ReturnStmt()])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_219():
    """Test expression statement with function call"""
    source = "func main() -> void { hello(); }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, [ExprStmt("
                "FunctionCall(Identifier(hello), []))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_220():
    """Test expression statement with function call and binary arg"""
    source = "func main() -> void { log(1 + 2); }"
    expected = ("Program(funcs=[FuncDecl(main, [], void, [ExprStmt("
                "FunctionCall(Identifier(log), [BinaryOp(IntegerLiteral(1), +, IntegerLiteral(2))]))])])")
    assert str(ASTGenerator(source).generate()) == expected

def test_226():
    """Nested unary operators and array access"""
    source = "func main() -> bool { return !!arr[1]; }"
    expected = (
        "Program(funcs=[FuncDecl(main, [], bool, [ReturnStmt("
        "UnaryOp(!, UnaryOp(!, ArrayAccess(Identifier(arr), IntegerLiteral(1))))"
        ")])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_227():
    """Pipeline with array access result"""
    source = "func main() -> void { let x = (data >> clean)[1]; }"
    expected = (
        "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, "
        "ArrayAccess(BinaryOp(Identifier(data), >>, Identifier(clean)), IntegerLiteral(1))"
        ")])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_228():
    """If with pipeline condition and function call"""
    source = "func main() -> void { if ((get() >> filter)[0] > 10) { return; } }"
    expected = (
        "Program(funcs=[FuncDecl(main, [], void, [IfStmt(condition="
        "BinaryOp(ArrayAccess(BinaryOp(FunctionCall(Identifier(get), []), >>, Identifier(filter)), IntegerLiteral(0)), >, IntegerLiteral(10)), "
        "then_stmt=BlockStmt([ReturnStmt()]))])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_229():
    """Unary with nested binary and function call"""
    source = "func main() -> void { let x = !((a[0] + f(1)) * 2); }"
    expected = (
        "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, "
        "UnaryOp(!, BinaryOp(BinaryOp(ArrayAccess(Identifier(a), IntegerLiteral(0)), +, "
        "FunctionCall(Identifier(f), [IntegerLiteral(1)])), *, IntegerLiteral(2))))])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_230():
    """While with complex logical condition"""
    source = "func main() -> void { while (!(a[0] + 1 < 5 || foo())) { break; } }"
    expected = (
        "Program(funcs=[FuncDecl(main, [], void, [WhileStmt("
        "UnaryOp(!, BinaryOp("
            "BinaryOp(BinaryOp(ArrayAccess(Identifier(a), IntegerLiteral(0)), +, IntegerLiteral(1)), <, IntegerLiteral(5)), "
            "||, FunctionCall(Identifier(foo), []))), "
        "BlockStmt([BreakStmt()]))])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_231():
    """Return pipeline with function call and expression"""
    source = "func main() -> bool { return (arr >> map)[0] + 1 == 10; }"
    expected = (
        "Program(funcs=[FuncDecl(main, [], bool, [ReturnStmt("
        "BinaryOp(BinaryOp(ArrayAccess(BinaryOp(Identifier(arr), >>, Identifier(map)), IntegerLiteral(0)), +, IntegerLiteral(1)), ==, IntegerLiteral(10))"
        ")])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_232():
    """Let binding with pipeline and function call arg"""
    source = "func main() -> void { let x = data >> filter(x % 2 == 0); }"
    expected = (
        "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, "
        "BinaryOp(Identifier(data), >>, FunctionCall(Identifier(filter), "
        "[BinaryOp(BinaryOp(Identifier(x), %, IntegerLiteral(2)), ==, IntegerLiteral(0))])))])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_233():
    """Array access with index from function call"""
    source = "func main() -> int { return arr[getIndex()]; }"
    expected = (
        "Program(funcs=[FuncDecl(main, [], int, [ReturnStmt("
        "ArrayAccess(Identifier(arr), FunctionCall(Identifier(getIndex), []))"
        ")])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_234():
    """ExprStmt with function call on binary + pipeline"""
    source = "func main() -> void { print((arr >> map)[0] + 1); }"
    expected = (
        "Program(funcs=[FuncDecl(main, [], void, [ExprStmt("
        "FunctionCall(Identifier(print), [BinaryOp(ArrayAccess(BinaryOp(Identifier(arr), >>, Identifier(map)), IntegerLiteral(0)), +, IntegerLiteral(1))]))])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_235():
    """Return empty array literal"""
    source = "func main() -> [int; 0] { return []; }"
    expected = (
        "Program(funcs=[FuncDecl(main, [], [int; 0], [ReturnStmt(ArrayLiteral([]))])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_236():
    """Test <= inside nested binary expression"""
    source = "func main() -> bool { return a + 1 <= b * 2; }"
    expected = (
        "Program(funcs=[FuncDecl(main, [], bool, [ReturnStmt("
        "BinaryOp(BinaryOp(Identifier(a), +, IntegerLiteral(1)), <=, "
        "BinaryOp(Identifier(b), *, IntegerLiteral(2)))"
        ")])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_237():
    """Test >= with array access and pipeline"""
    source = "func main() -> bool { return (data >> process)[0] >= 10; }"
    expected = (
        "Program(funcs=[FuncDecl(main, [], bool, [ReturnStmt("
        "BinaryOp(ArrayAccess(BinaryOp(Identifier(data), >>, Identifier(process)), IntegerLiteral(0)), >=, IntegerLiteral(10))"
        ")])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_238():
    """Test if with all relational operators"""
    source = """
    func main() -> void {
        if (a < b && b <= c && c == d && d != e && e >= f && f > g) {
            return;
        }
    }
    """
    expected = (
        "Program(funcs=[FuncDecl(main, [], void, [IfStmt(condition="
        "BinaryOp("
            "BinaryOp("
                "BinaryOp("
                    "BinaryOp("
                        "BinaryOp(BinaryOp(Identifier(a), <, Identifier(b)), &&, BinaryOp(Identifier(b), <=, Identifier(c))), &&, "
                        "BinaryOp(Identifier(c), ==, Identifier(d))), &&, "
                    "BinaryOp(Identifier(d), !=, Identifier(e))), &&, "
                "BinaryOp(Identifier(e), >=, Identifier(f))), &&, "
            "BinaryOp(Identifier(f), >, Identifier(g))"
        "), then_stmt=BlockStmt([ReturnStmt()]))])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_239():
    """Test division operator in expression"""
    source = "func main() -> int { return a / b + c; }"
    expected = (
        "Program(funcs=[FuncDecl(main, [], int, [ReturnStmt("
        "BinaryOp(BinaryOp(Identifier(a), /, Identifier(b)), +, Identifier(c))"
        ")])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_240():
    """Division with array access"""
    source = "func main() -> float { return data[0] / 2.0; }"
    expected = (
        "Program(funcs=[FuncDecl(main, [], float, [ReturnStmt("
        "BinaryOp(ArrayAccess(Identifier(data), IntegerLiteral(0)), /, FloatLiteral(2.0))"
        ")])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_241():
    """Test double negative unary"""
    source = "func main() -> int { return --a; }"
    expected = (
        "Program(funcs=[FuncDecl(main, [], int, [ReturnStmt("
        "UnaryOp(-, UnaryOp(-, Identifier(a)))"
        ")])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_242():
    """Test alternating unary logic and negative"""
    source = "func main() -> bool { return !-!a; }"
    expected = (
        "Program(funcs=[FuncDecl(main, [], bool, [ReturnStmt("
        "UnaryOp(!, UnaryOp(-, UnaryOp(!, Identifier(a))))"
        ")])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_243():
    """Double logical NOT on binary expression"""
    source = "func main() -> bool { return !!(a + b); }"
    expected = (
        "Program(funcs=[FuncDecl(main, [], bool, [ReturnStmt("
        "UnaryOp(!, UnaryOp(!, BinaryOp(Identifier(a), +, Identifier(b))))"
        ")])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_244():
    """Negative of logical NOT on multiplication"""
    source = "func main() -> int { return -!(a * b); }"
    expected = (
        "Program(funcs=[FuncDecl(main, [], int, [ReturnStmt("
        "UnaryOp(-, UnaryOp(!, BinaryOp(Identifier(a), *, Identifier(b))))"
        ")])])"
    )
    assert str(ASTGenerator(source).generate()) == expected

def test_245():
    """Test multidimensional array literal"""
    source = """
    func main() -> void {
    a[2] >> b; // (1) expr stmt pepline, have ';'
    }
    """
    expected = ("Program(funcs=[FuncDecl(main, [], void, [ExprStmt(BinaryOp(ArrayAccess(Identifier(a), IntegerLiteral(2)), >>, Identifier(b)))])])")
    assert str(ASTGenerator(source).generate()) == expected