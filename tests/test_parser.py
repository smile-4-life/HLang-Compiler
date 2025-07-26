from utils import Parser

# Valid cases
def test_001():
    """Valid empty function"""
    source = "func main() -> void {}"
    expected = "success"
    assert Parser(source).parse() == expected

def test_002():
    """Function with params and return"""
    source = "func add(a: int, b: int) -> int { return a + b; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_003():
    """Multiple top-level functions"""
    source = """func foo() -> void {} 
                func bar() -> int { return 1; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_004():
    """Const declaration"""
    source = "const PI: float = 3.14;"
    expected = "success"
    assert Parser(source).parse() == expected

def test_005():
    """Variable declaration with type"""
    source = "func main() -> void { let x: int = 42; }"
    expected = "success"
    assert Parser(source).parse() == expected

# Error cases
def test_006():
    """Missing return type"""
    source = "func main() {}"
    expected = "Error on line 1 col 12: {"
    assert Parser(source).parse() == expected

def test_007():
    """Invalid return type"""
    source = "func main() -> 123 {}"
    expected = "Error on line 1 col 15: 123"
    assert Parser(source).parse() == expected

def test_008():
    """Missing arrow in return type"""
    source = "func main() void {}"
    expected = "Error on line 1 col 12: void"
    assert Parser(source).parse() == expected

def test_009():
    """Missing function body"""
    source = "func main() -> void"
    expected = "Error on line 1 col 19: <EOF>"
    assert Parser(source).parse() == expected

def test_010():
    """Nested functions"""
    source = "func outer() -> void { func inner() -> void {} }"
    expected = "Error on line 1 col 23: func"
    assert Parser(source).parse() == expected

# Control flow
def test_011():
    """Valid if-else"""
    source = """func test() -> void {
        if (x > 0) { 
            return; 
        } else { 
            return; 
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_012():
    """If without else"""
    source = "func test() -> void { if (true) {let a = 1+2;let b = a;} }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_013():
    """Missing if condition"""
    source = "func test() -> void { if () {} }"
    expected = "Error on line 1 col 26: )"
    assert Parser(source).parse() == expected

def test_014():
    """ implicit type conversion to boolean not in parser so success"""
    source = "func test() -> void { if (123) {} }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_015():
    """Valid while loop"""
    source = "func test() -> void { while (true) {} }"
    expected = "success"
    assert Parser(source).parse() == expected

# Variables and types
def test_016():
    """Variable without initializer"""
    source = "func test() -> void { let x: int; }"
    expected = "Error on line 1 col 32: ;"
    assert Parser(source).parse() == expected

def test_017():
    """Invalid type annotation"""
    source = "func test() -> void { let x: 123 = 1; }"
    expected = "Error on line 1 col 29: 123"
    assert Parser(source).parse() == expected

def test_018():
    """Array type missing size"""
    source = "func test() -> void { let arr: [int] = [1]; }"
    expected = "Error on line 1 col 35: ]"
    assert Parser(source).parse() == expected

def test_019():
    """Invalid array literal"""
    source = "func test() -> void { let arr = [1, 2,]; }"
    expected = "Error on line 1 col 38: ]"
    assert Parser(source).parse() == expected

def test_020():
    """Multi-dimensional array"""
    source = "func test() -> void { let mat: [[int; 2]; 2] = [[1,2],[3,4]]; }"
    expected = "success"
    assert Parser(source).parse() == expected

# Expressions
def test_021():
    """Complex expression"""
    source = "func test() -> void { let x = (a + b) * c >> foo(d); }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_022():
    """Invalid operator sequence"""
    source = "func test() -> void { let x = a * / b; }"
    expected = "Error on line 1 col 34: /"
    assert Parser(source).parse() == expected

def test_023():
    """Missing expression"""
    source = "func test() -> void { let x = ; }"
    expected = "Error on line 1 col 30: ;"
    assert Parser(source).parse() == expected

def test_024():
    """Invalid parenthesized expr"""
    source = "func test() -> void { let x = (; }"
    expected = "Error on line 1 col 31: ;"
    assert Parser(source).parse() == expected

def test_025():
    """Array access"""
    source = "func test() -> void { let x = arr[1+2]; }"
    expected = "success"
    assert Parser(source).parse() == expected

# Function calls
def test_026():
    """Valid function call"""
    source = "func test() -> void { foo(1, 2); }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_027():
    """Missing call arguments"""
    source = "func test() -> void { foo(,); }"
    expected = "Error on line 1 col 26: ,"
    assert Parser(source).parse() == expected

def test_028():
    """Malformed call"""
    source = "func test() -> void { foo(1, 2; }"
    expected = "Error on line 1 col 30: ;"
    assert Parser(source).parse() == expected

def test_029():
    """Nested calls"""
    source = "func test() -> void { foo(bar(1)); }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_030():
    """Pipeline operator"""
    source = "func test() -> void { let x = a >> b(1) >> c; }"
    expected = "success"
    assert Parser(source).parse() == expected

# Return statements
def test_031():
    """Valid return with value"""
    source = "func test() -> int { return 42; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_032():
    """Return without value in void"""
    source = "func test() -> void { return; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_033():
    """Missing return in non-void but still success in parser"""
    source = "func test() -> int { let x = 42; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_034():
    """Return with value in void but still success in parser"""
    source = "func test() -> void { return 42; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_035():
    """Empty return in non-void but still success in parser"""
    source = "func test() -> int { return; }"
    expected = "success"
    assert Parser(source).parse() == expected

# Edge cases
def test_036():
    source = 'func test() -> void { let s = "cafe"; }'
    expected = "success" 
    assert Parser(source).parse() == expected

def test_037():
    """Huge integer literal"""
    source = "func test() -> void { let x = 12345678901234567890; }"
    expected = "success"  # Parser should accept, even if value too large
    assert Parser(source).parse() == expected

def test_038():
    """Weird whitespace"""
    source = "func \t test(\n)\r\n-> \v void { }"
    expected = "Error Token \v"
    assert Parser(source).parse() == expected

def test_039():
    """Minimal program"""
    source = "func f() -> void {}"
    expected = "success"
    assert Parser(source).parse() == expected

def test_040():
    """All operators together"""
    source = """func test() -> void { 
        let x = a + b - c * d / e % f == g != h < i <= j > k >= l && m || n;
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

# Complex cases
def test_041():
    """Complex valid program"""
    source = """
    const PI = 3.14;
    
    func factorial(n: int) -> int {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }
    
    func main() -> void {
        let nums = [1, 2, 3];
        for (num in nums) {
            print(str(factorial(num)));
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_042():
    """Multiple errors"""
    source = """
    func test() {
        let x = ;
        if () {}
        return 1;
    }"""
    expected = "Error on line 2 col 16: {"
    assert Parser(source).parse() == expected

def test_043():
    """Deeply nested"""
    source = """
    func test() -> void {
        if (true) {
            while (false) {
                for (x in []) {
                    let y = x;
                }
            }
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_044():
    """Multiple array dimensions"""
    source = """
    func test() -> void {
        let mat: [[[int; 2]; 2]; 2] = [
            [[1,2],[3,4]],
            [[5,6],[7,8]]
        ];
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_045():
    """Complex pipeline"""
    source = """
    func test() -> void {
        let result = data
            >> filter(x > 0)
            >> map(fn)
            >> reduce(0, add);
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

# Error recovery
def test_046():
    """Missing closing brace"""
    source = """
    func test() -> void {
        if (true) {
            let x = 1;
    """
    expected = "Error on line 5 col 4: <EOF>"
    assert Parser(source).parse() == expected

def test_047():
    """Extra closing brace"""
    source = """
    func test() -> void {
        let x = 1;
        }
    }"""
    expected = "Error on line 5 col 4: }"
    assert Parser(source).parse() == expected

def test_048():
    """Malformed array type"""
    source = "func test() -> void { let arr: [int; = [1]; }"
    expected = "Error on line 1 col 37: ="
    assert Parser(source).parse() == expected

def test_049():
    """Invalid parameter list"""
    source = "func test(a: int, b) -> void {}"
    expected = "Error on line 1 col 19: )"
    assert Parser(source).parse() == expected

def test_050():
    """Everything wrong"""
    source = """
    func {
        let = ;
        if {}
        return
    }"""
    expected = "Error on line 2 col 9: {"
    assert Parser(source).parse() == expected

def test_051():
    """Negative integer literal"""
    source = "func test() -> void { let x = -42; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_052():
    """Unary plus"""
    source = "func test() -> void { let x = +42; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_053():
    """Float literal"""
    source = "func test() -> void { let pi = 3.1415; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_054():
    """String with escape sequence"""
    source = r'func test() -> void { let s = "line\\n"; }'
    expected = "success"
    assert Parser(source).parse() == expected

def test_055():
    source = "func test() -> int { let a = []; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_056():
    """Empty array literal"""
    source = "func test() -> void { let a = []; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_057():
    """Unary minus on function call"""
    source = "func test() -> void { let x = -foo(); }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_058():
    """Unary plus on parenthesized expression"""
    source = "func test() -> void { let x = +((1)); }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_059():
    """String concatenation using +"""
    source = 'func test() -> void { let s = "a" + "b"; }'
    expected = "success"
    assert Parser(source).parse() == expected

def test_060():
    """Modulo operator with variable"""
    source = "func test() -> void { let x = a % 2; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_061():
    """Logical and"""
    source = "func test() -> void { let x = a && b; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_062():
    """Logical or"""
    source = "func test() -> void { let x = a || b; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_063():
    """Comparison chain"""
    source = "func test() -> void { let x = a < b <= c; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_064():
    """Invalid logic chaining"""
    source = "func test() -> void { let x = && a; }"
    expected = "Error on line 1 col 30: &&"
    assert Parser(source).parse() == expected

def test_065():
    """Negated expression"""
    source = "func test() -> void { let x = !(a == b); }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_066():
    """Missing logic operand"""
    source = "func test() -> void { let x = a || ; }"
    expected = "Error on line 1 col 35: ;"
    assert Parser(source).parse() == expected

def test_067():
    """Logic with function call"""
    source = "func test() -> void { let x = foo() && true; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_068():
    """Multiple return statements"""
    source = "func test() -> int { return 1; return 2; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_069():
    """Boolean literal"""
    source = "func test() -> void { let b = true; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_070():
    """Logical expression with parens"""
    source = "func test() -> void { let x = (a && b) || c; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_071():
    """Unclosed parenthesis"""
    source = "func test() -> void { let x = (a + b; }"
    expected = "Error on line 1 col 36: ;"
    assert Parser(source).parse() == expected

def test_072():
    """Extra semicolon"""
    source = "func test() -> void { let x = 1;; }"
    expected = "Error on line 1 col 32: ;"
    assert Parser(source).parse() == expected

def test_073():
    """Invalid escape in string"""
    source = 'func test() -> void { let s = "abc"; }'
    expected = "success"
    assert Parser(source).parse() == expected

def test_074():
    """Empty string"""
    source = 'func test() -> void { let s = ""; }'
    expected = "success"
    assert Parser(source).parse() == expected

def test_075():
    """Illegal character"""
    source = "func test() -> void { let x = 1 @ 2; }"
    expected = "Error on line 1 col 32: @"
    assert Parser(source).parse() == expected

def test_076():
    """Double quotes inside string"""
    source = 'func test() -> void { let s = "\\"quoted\\""; }'
    expected = "success"
    assert Parser(source).parse() == expected

def test_077():
    """Missing semicolon"""
    source = "func test() -> void { let x = 1 }"
    expected = "Error on line 1 col 32: }"
    assert Parser(source).parse() == expected

def test_078():
    """Use of undefined token"""
    source = "func test() -> void { let x = a # b; }"
    expected = "Error on line 1 col 32: #"
    assert Parser(source).parse() == expected

def test_079():
    """Multiline string with newline inside"""
    source = '''func test() -> void { let s = "abc
def"; }'''
    expected = "success"
    assert Parser(source).parse() == expected

def test_080():
    """Tab character"""
    source = "func test()\t-> void { let x = 1; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_081():
    """Nested function calls with math"""
    source = "func test() -> void { let x = add(1, mul(2, 3)); }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_082():
    """Pipeline with string"""
    source = 'func test() -> void { let s = "abc" >> upper >> trim; }'
    expected = "success"
    assert Parser(source).parse() == expected

def test_083():
    """Pipeline with missing function"""
    source = 'func test() -> void { let s = "a" >> ; }'
    expected = "Error on line 1 col 37: ;"
    assert Parser(source).parse() == expected

def test_084():
    """Nested parens"""
    source = "func test() -> void { let x = (((1))); }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_085():
    """Multiple pipeline steps"""
    source = "func test() -> void { let x = a >> b >> c >> d; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_086():
    """Pipeline with non-call"""
    source = "func test() -> void { let x = a >> 123; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_087():
    """Expression with mixed unary and binary"""
    source = "func test() -> void { let x = -a * +b; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_088():
    """Multiple assignment"""
    source = "func test() -> void { let a = b = c = 1; }"
    expected = "Error on line 1 col 32: ="
    assert Parser(source).parse() == expected

def test_089():
    """Single identifier"""
    source = "func test() -> void { a; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_090():
    """Function with no params"""
    source = "func hello() -> void { print(\"hi\"); }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_091():
    """Scope shadowing"""
    source = """
    func test() -> void {
        let x = 1;
        {
            let x = 2;
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_092():
    """Return from inner block"""
    source = """
    func test() -> int {
        {
            return 1;
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_093():
    """Return inside loop"""
    source = """
    func test() -> int {
        while (true) {
            return 1;
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_094():
    """Nested array literal"""
    source = "func test() -> void { let x = [[1,2],[3,4]]; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_095():
    """Empty function call"""
    source = "func test() -> void { do_nothing(); }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_096():
    """Function with single statement"""
    source = "func test() -> void { 42; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_097():
    """Missing colon in param"""
    source = "func add(a int) -> int { return a; }"
    expected = "Error on line 1 col 11: int"
    assert Parser(source).parse() == expected

def test_098():
    """Pipeline with nested calls"""
    source = "func test() -> void { let x = a >> b(c(d)); }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_099():
    """Invalid token in comment"""
    source = "func test() -> void { // invalid @\nlet x = 1; }"
    expected = "success"
    assert Parser(source).parse() == expected

def test_100():
    """Empty block"""
    source = "func test() -> void { {} }"
    expected = "success"
    assert Parser(source).parse() == expected
