from utils import Checker
# 1. Test case cho Redeclared Variable trong cùng scope
def test001():
    source = """
func example() -> void {
    let x = 10;
    let x = 20;
}
"""
    expected = "Redeclared Variable: x"
    assert Checker(source).check_from_source() == expected

def test002():
    source = """
// Error: Redeclared Function in global scope
func calculate() -> int { return 42; }
func calculate() -> int { return 24; }  // Redeclared(Function, calculate)
"""
    expected = "Redeclared Function: calculate"
    assert Checker(source).check_from_source() == expected

def test003():
    source = """
// Error: Redeclared Constant in global scope
const PI = 3.14;
const PI = 3.14159;  // Redeclared(Constant, PI)
"""
    expected = "Redeclared Constant: PI"
    assert Checker(source).check_from_source() == expected

def test004():
    source = """
// Error: Redeclared Constant in global scope
func process(x: int, y: float, x: bool) -> void {  // Redeclared(Parameter, x)
    print("Processing");
}
"""
    expected = "Redeclared Parameter: x"
    assert Checker(source).check_from_source() == expected

def test005():
    source = """
// Error: Redeclared Constant in global scope
func process(x: int, y: float, x: bool) -> void {  // Redeclared(Parameter, x)
    print("Processing");
}
"""
    expected = "Redeclared Parameter: x"
    assert Checker(source).check_from_source() == expected

def test005():
    source = """
// Error: Redeclared in nested block (same level)
func nested() -> void {
    if (true) {
        let temp = 1;
        let temp = 2;  // Redeclared(Variable, temp)
    }
}
"""
    expected = "Redeclared Variable: temp"
    assert Checker(source).check_from_source() == expected

def test006():
    source = """
// Valid: Shadowing (different scopes)
const globalVar = 100;
func shadowExample() -> void {
    let globalVar = 200;  // Valid: shadows global variable
    {
        let globalVar = 300;  // Valid: shadows function-scope variable
    }
}
func main()->void{}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test007():
    source = """
func main() -> void {
    print(str(undeclaredVar));  // Undeclared(Identifier(), undeclaredVar)
}

"""
    expected = "Undeclared Identifier: undeclaredVar"
    assert Checker(source).check_from_source() == expected

def test008():
    source = """
// Error: Undeclared function
func main() -> void {
    undeclaredFunc();           // Undeclared(Function(), undeclaredFunc)
}

"""
    expected = "Undeclared Function: undeclaredFunc"
    assert Checker(source).check_from_source() == expected

def test009():
    source = """
// Error: Variable used before declaration
func beforeDeclaration() -> void {
    let result = x + 10;  // Undeclared(Identifier(), x)
    let x = 5;
}
"""
    expected = "Undeclared Identifier: x"
    assert Checker(source).check_from_source() == expected

def test010():
    source = """
// Error: Out of scope variable
func scopeError() -> void {
    if (true) {
        let localVar = 42;
    }
    print(str(localVar));  // Undeclared(Identifier(), localVar)
}
"""
    expected = "Undeclared Identifier: localVar"
    assert Checker(source).check_from_source() == expected

def test011():
    source = """
// Error: Shadowed variable not accessible
func shadowError() -> void {
    let x = 10;
    {
        let x = 20;  // Shadows outer x
        {
            let y = x + 5;  // Uses inner x (20)
        }
        let z = y + 1;  // Undeclared(Identifier(), y) - y is out of scope
    }
}
"""
    expected = "Undeclared Identifier: y"
    assert Checker(source).check_from_source() == expected

def test012():
    source = """
// Valid: Forward reference to global function
// Valid: Forward reference to global function
func validCall() -> void {
    globalFunc();  // Valid: globalFunc declared later but in global scope
}
func globalFunc() -> void {
    print("Global function");
}
func main()->void{}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test014():
    source = """
const MAX_VALUE = 100;
func constError() -> void {
    let value = MAX_VALUE + 1;  // Undeclared(Identifier(), MAX_VALUE)
}
func main()->void{}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test015():
    source = """
func main() -> void {
let numbers = [1, 2, 3];
let result1 = numbers["invalid"]; // TypeMismatchInExpression - string index
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(numbers), StringLiteral('invalid'))"
    assert Checker(source).check_from_source() == expected

def test016():
    source = """
func main() -> void {
let numbers = [1, 2, 3];
let result2 = numbers[3.14];          // TypeMismatchInExpression - float index
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(numbers), FloatLiteral(3.14))"
    assert Checker(source).check_from_source() == expected

def test017():
    source = """
func main() -> void {
    let numbers = [1, 2, 3];
    let result3 = numbers[true];          // TypeMismatchInExpression - bool index
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(numbers), BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test018():
    source = """
func main() -> void {
    let x = 5;
    let y = true;
    let sum = x + y;                      // TypeMismatchInExpression - int + bool
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(Identifier(x), +, Identifier(y))"
    assert Checker(source).check_from_source() == expected

def test019():
    source = """
func main() -> void {
    let x = 5;
    let comparison = x < "hello";         // TypeMismatchInExpression - int < string
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(Identifier(x), <, StringLiteral('hello'))"
    assert Checker(source).check_from_source() == expected

def test020():
    source = """
func main() -> void {
    let x = 5;
    let equality = x == 5.0;              // TypeMismatchInExpression - int == float
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(Identifier(x), ==, FloatLiteral(5.0))"
    assert Checker(source).check_from_source() == expected

def test021():
    source = """
func main() -> void {
    let x = 5;
    let y = true;
    let logical = x && y;                 // TypeMismatchInExpression - int && bool
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(Identifier(x), &&, Identifier(y))"
    assert Checker(source).check_from_source() == expected

def test022():
    source = """
func main() -> void {
    let condition = !42;                  // TypeMismatchInExpression - !int
}
"""
    expected = "Type Mismatch In Expression: UnaryOp(!, IntegerLiteral(42))"
    assert Checker(source).check_from_source() == expected

def test023():
    source = """
func main() -> void {
    let negative = -true;                 // TypeMismatchInExpression - -bool
}
"""
    expected = "Type Mismatch In Expression: UnaryOp(-, BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test024():
    source = """
func main() -> void {
    let positive = +"text";               // TypeMismatchInExpression - +string
}
"""
    expected = "Type Mismatch In Expression: UnaryOp(+, StringLiteral('text'))"
    assert Checker(source).check_from_source() == expected

def test025():
    source = """
func main() -> void {
    let voidResult = printMessage("hi");  // TypeMismatchInExpression - void function in expression
}

func printMessage(msg: string) -> void {
    print(msg);
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(printMessage), [StringLiteral('hi')])"
    assert Checker(source).check_from_source() == expected

def test026():
    source = """
func main() -> void {
    let wrongArgs = add(5, "hello");      // TypeMismatchInExpression - int, string to int, int
}

func add(a: int, b: int) -> int {
    return a + b;
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(add), [IntegerLiteral(5), StringLiteral('hello')])"
    assert Checker(source).check_from_source() == expected

def test027():
    source = """
func main() -> void {
    let tooFewArgs = multiply(5);         // TypeMismatchInExpression - 1 arg to 2-param function
}

func multiply(a: int, b: int) -> int {
    return a * b;
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(multiply), [IntegerLiteral(5)])"
    assert Checker(source).check_from_source() == expected

def test028():
    source = """
func main() -> void {
    let tooManyArgs = getValue(1, 2);     // TypeMismatchInExpression - 2 args to 0-param function
}

func getValue() -> int {
    return 42;
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(getValue), [IntegerLiteral(1), IntegerLiteral(2)])"
    assert Checker(source).check_from_source() == expected

def test029():
    source = """
func arrayErrors() -> void {
    let intArray: [int; 3] = [1, 2, 3];
    let floatArray: [float; 3] = [1.0, 2.0, 3.0];
    let result1 = intArray[floatArray[0]];    // TypeMismatchInExpression - float index
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(intArray), ArrayAccess(Identifier(floatArray), IntegerLiteral(0)))"
    assert Checker(source).check_from_source() == expected

def test030():
    source = """
func arrayErrors() -> void {
    let intArray: [int; 3] = [1, 2, 3];
    let stringArray: [string; 2] = ["a", "b"];
    let result2 = stringArray[intArray];      // TypeMismatchInExpression - array index
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(stringArray), Identifier(intArray))"
    assert Checker(source).check_from_source() == expected

def test031():
    source = """
func arrayErrors() -> void {
    let intArray: [int; 3] = [1, 2, 3];
    let stringArray: [string; 2] = ["a", "b"];
    let mixed2 = intArray[0] + stringArray[0]; // TypeMismatchInExpression - int + string
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(ArrayAccess(Identifier(intArray), IntegerLiteral(0)), +, ArrayAccess(Identifier(stringArray), IntegerLiteral(0)))"
    assert Checker(source).check_from_source() == expected

def test032():
    source = """
func nestedErrors() -> void {
    let arr = [1, 2, 3];
    let result = arr[arr[true]];              // TypeMismatchInExpression - bool index in inner access
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(arr), BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test033():
    source = """
func nestedErrors() -> void {
    let complex = (5 + 3) * ("hello" + 2);   // TypeMismatchInExpression - string + int
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(StringLiteral('hello'), +, IntegerLiteral(2))"
    assert Checker(source).check_from_source() == expected

def test034():
    source = """
func main() -> void {
    let numbers = [1, 2, 3];
    let result1 = numbers["invalid"];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(numbers), StringLiteral('invalid'))"
    assert Checker(source).check_from_source() == expected

def test035():
    source = """
func main() -> void {
    let numbers = [1, 2, 3];
    let result2 = numbers[3.14];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(numbers), FloatLiteral(3.14))"
    assert Checker(source).check_from_source() == expected

def test036():
    source = """
func main() -> void {
    let numbers = [1, 2, 3];
    let result3 = numbers[true];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(numbers), BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test037():
    source = """
func main() -> void {
    let x = 5;
    let y = true;
    let sum = x + y;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(Identifier(x), +, Identifier(y))"
    assert Checker(source).check_from_source() == expected

def test038():
    source = """
func main() -> void {
    let x = 5;
    let comparison = x < "hello";
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(Identifier(x), <, StringLiteral('hello'))"
    assert Checker(source).check_from_source() == expected

def test039():
    source = """
func main() -> void {
    let x = 5;
    let equality = x == 5.0;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(Identifier(x), ==, FloatLiteral(5.0))"
    assert Checker(source).check_from_source() == expected

def test040():
    source = """
func main() -> void {
    let x = 5;
    let y = true;
    let logical = x && y;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(Identifier(x), &&, Identifier(y))"
    assert Checker(source).check_from_source() == expected

def test041():
    source = """
func main() -> void {
    let condition = !42;
}
"""
    expected = "Type Mismatch In Expression: UnaryOp(!, IntegerLiteral(42))"
    assert Checker(source).check_from_source() == expected

def test042():
    source = """
func main() -> void {
    let negative = -true;
}
"""
    expected = "Type Mismatch In Expression: UnaryOp(-, BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test043():
    source = """
func main() -> void {
    let positive = +"text";
}
"""
    expected = "Type Mismatch In Expression: UnaryOp(+, StringLiteral('text'))"
    assert Checker(source).check_from_source() == expected

def test044():
    source = """
func printMessage(msg: string) -> void {
    print(msg);
}
func main() -> void {
    let voidResult = printMessage("hi");
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(printMessage), [StringLiteral('hi')])"
    assert Checker(source).check_from_source() == expected

def test045():
    source = """
func add(a: int, b: int) -> int {
    return a + b;
}
func main() -> void {
    let wrongArgs = add(5, "hello");
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(add), [IntegerLiteral(5), StringLiteral('hello')])"
    assert Checker(source).check_from_source() == expected

def test046():
    source = """
func multiply(a: int, b: int) -> int {
    return a * b;
}
func main() -> void {
    let tooFewArgs = multiply(5);
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(multiply), [IntegerLiteral(5)])"
    assert Checker(source).check_from_source() == expected

def test047():
    source = """
func getValue() -> int {
    return 42;
}
func main() -> void {
    let tooManyArgs = getValue(1, 2);
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(getValue), [IntegerLiteral(1), IntegerLiteral(2)])"
    assert Checker(source).check_from_source() == expected

def test048():
    source = """
func main() -> void {
    let intArray: [int; 3] = [1, 2, 3];
    let floatArray: [float; 3] = [1.0, 2.0, 3.0];
    let result1 = intArray[floatArray[0]];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(intArray), ArrayAccess(Identifier(floatArray), IntegerLiteral(0)))"
    assert Checker(source).check_from_source() == expected

def test049():
    source = """
func main() -> void {
    let intArray: [int; 3] = [1, 2, 3];
    let stringArray: [string; 2] = ["a", "b"];
    let result2 = stringArray[intArray];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(stringArray), Identifier(intArray))"
    assert Checker(source).check_from_source() == expected

def test050():
    source = """
func main() -> void {
    let intArray: [int; 3] = [1, 2, 3];
    let stringArray: [string; 2] = ["a", "b"];
    let mixed2 = intArray[0] + stringArray[0];
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(ArrayAccess(Identifier(intArray), IntegerLiteral(0)), +, ArrayAccess(Identifier(stringArray), IntegerLiteral(0)))"
    assert Checker(source).check_from_source() == expected

def test051():
    source = """
func main() -> void {
    let arr = [1, 2, 3];
    let result = arr[arr[true]];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(arr), BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test052():
    source = """
func main() -> void {
    let complex = (5 + 3) * ("hello" + 2);
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(StringLiteral('hello'), +, IntegerLiteral(2))"
    assert Checker(source).check_from_source() == expected

def test053():
    source = """
func main() -> void {
    let intArray: [int; 3] = [1, 2, 3];
    let floatArray: [float; 3] = [1.0, 2.0, 3.0];
    let mixed1 = intArray[0] + floatArray[0];
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test054():
    source = """
func example() -> void {
    let x = 10;
    let x = 20;
}
"""
    expected = "Redeclared Variable: x"
    assert Checker(source).check_from_source() == expected

def test055():
    source = """
func calculate() -> int { return 42; }
func calculate() -> int { return 24; }
"""
    expected = "Redeclared Function: calculate"
    assert Checker(source).check_from_source() == expected

def test056():
    source = """
const PI = 3.14;
const PI = 3.14159;
"""
    expected = "Redeclared Constant: PI"
    assert Checker(source).check_from_source() == expected

def test057():
    source = """
func process(x: int, y: float, x: bool) -> void {
    print("Processing");
}
"""
    expected = "Redeclared Parameter: x"
    assert Checker(source).check_from_source() == expected

def test058():
    source = """
func mixed() -> void {
    let value = 42;
    const value = 100;
}
"""
    expected = "Redeclared Constant: value"
    assert Checker(source).check_from_source() == expected

def test059():
    source = """
func nested() -> void {
    if (true) {
        let temp = 1;
        let temp = 2;
    }
}
"""
    expected = "Redeclared Variable: temp"
    assert Checker(source).check_from_source() == expected

def test060():
    source = """
const globalVar = 100;
func shadowExample() -> void {
    let globalVar = 200;
    {
        let globalVar = 300;
    }
}
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test061():
    source = """
func main() -> void {
    print(str(undeclaredVar));
}
"""
    expected = "Undeclared Identifier: undeclaredVar"
    assert Checker(source).check_from_source() == expected

def test062():
    source = """
func main() -> void {
    undeclaredFunc();
}
"""
    expected = "Undeclared Function: undeclaredFunc"
    assert Checker(source).check_from_source() == expected

def test063():
    source = """
func beforeDeclaration() -> void {
    let result = x + 10;
    let x = 5;
}
"""
    expected = "Undeclared Identifier: x"
    assert Checker(source).check_from_source() == expected

def test064():
    source = """
func scopeError() -> void {
    if (true) {
        let localVar = 42;
    }
    print(str(localVar));
}
"""
    expected = "Undeclared Identifier: localVar"
    assert Checker(source).check_from_source() == expected

def test065():
    source = """
func shadowError() -> void {
    let x = 10;
    {
        let x = 20;
        {
            let y = x + 5;
        }
        let z = y + 1;
    }
}
"""
    expected = "Undeclared Identifier: y"
    assert Checker(source).check_from_source() == expected

def test066():
    source = """
func validCall() -> void {
    globalFunc();
}
func globalFunc() -> void {
    print("Global function");
}
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test067():
    source = """
func constError() -> void {
    let value = MAX_VALUE + 1;
}
const MAX_VALUE = 100;
func main() -> void {}
"""
    expected = "Undeclared Identifier: MAX_VALUE"
    assert Checker(source).check_from_source() == expected

def test068():
    source = """
const MAX_VALUE = 100;
func constError() -> void {
    let value = MAX_VALUE + 1;
}
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test069():
    source = """
func main() -> void {
    let numbers = [1, 2, 3];
    let result1 = numbers["invalid"];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(numbers), StringLiteral('invalid'))"
    assert Checker(source).check_from_source() == expected

def test070():
    source = """
func main() -> void {
    let numbers = [1, 2, 3];
    let result2 = numbers[3.14];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(numbers), FloatLiteral(3.14))"
    assert Checker(source).check_from_source() == expected

def test071():
    source = """
func main() -> void {
    let numbers = [1, 2, 3];
    let result3 = numbers[true];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(numbers), BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test072():
    source = """
func main() -> void {
    let x = 5;
    let y = true;
    let sum = x + y;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(Identifier(x), +, Identifier(y))"
    assert Checker(source).check_from_source() == expected

def test073():
    source = """
func main() -> void {
    let x = 5;
    let comparison = x < "hello";
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(Identifier(x), <, StringLiteral('hello'))"
    assert Checker(source).check_from_source() == expected

def test074():
    source = """
func main() -> void {
    let x = 5;
    let equality = x == 5.0;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(Identifier(x), ==, FloatLiteral(5.0))"
    assert Checker(source).check_from_source() == expected

def test075():
    source = """
func main() -> void {
    let x = 5;
    let y = true;
    let logical = x && y;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(Identifier(x), &&, Identifier(y))"
    assert Checker(source).check_from_source() == expected

def test076():
    source = """
func main() -> void {
    let condition = !42;
}
"""
    expected = "Type Mismatch In Expression: UnaryOp(!, IntegerLiteral(42))"
    assert Checker(source).check_from_source() == expected

def test077():
    source = """
func main() -> void {
    let negative = -true;
}
"""
    expected = "Type Mismatch In Expression: UnaryOp(-, BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test078():
    source = """
func main() -> void {
    let positive = +"text";
}
"""
    expected = "Type Mismatch In Expression: UnaryOp(+, StringLiteral('text'))"
    assert Checker(source).check_from_source() == expected

def test079():
    source = """
func main() -> void {
    let voidResult = printMessage("hi");
}

func printMessage(msg: string) -> void {
    print(msg);
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(printMessage), [StringLiteral('hi')])"
    assert Checker(source).check_from_source() == expected

def test080():
    source = """
func main() -> void {
    let wrongArgs = add(5, "hello");
}

func add(a: int, b: int) -> int {
    return a + b;
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(add), [IntegerLiteral(5), StringLiteral('hello')])"
    assert Checker(source).check_from_source() == expected

def test081():
    source = """
func main() -> void {
    let tooFewArgs = multiply(5);
}

func multiply(a: int, b: int) -> int {
    return a * b;
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(multiply), [IntegerLiteral(5)])"
    assert Checker(source).check_from_source() == expected

def test082():
    source = """
func main() -> void {
    let tooManyArgs = getValue(1, 2);
}

func getValue() -> int {
    return 42;
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(getValue), [IntegerLiteral(1), IntegerLiteral(2)])"
    assert Checker(source).check_from_source() == expected

def test083():
    source = """
func arrayErrors() -> void {
    let intArray: [int; 3] = [1, 2, 3];
    let floatArray: [float; 3] = [1.0, 2.0, 3.0];
    let result1 = intArray[floatArray[0]];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(intArray), ArrayAccess(Identifier(floatArray), IntegerLiteral(0)))"
    assert Checker(source).check_from_source() == expected

def test084():
    source = """
func arrayErrors() -> void {
    let intArray: [int; 3] = [1, 2, 3];
    let stringArray: [string; 2] = ["a", "b"];
    let result2 = stringArray[intArray];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(stringArray), Identifier(intArray))"
    assert Checker(source).check_from_source() == expected

def test085():
    source = """
func arrayErrors() -> void {
    let intArray: [int; 3] = [1, 2, 3];
    let stringArray: [string; 2] = ["a", "b"];
    let mixed2 = intArray[0] + stringArray[0];
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(ArrayAccess(Identifier(intArray), IntegerLiteral(0)), +, ArrayAccess(Identifier(stringArray), IntegerLiteral(0)))"
    assert Checker(source).check_from_source() == expected

def test086():
    source = """
func nestedErrors() -> void {
    let arr = [1, 2, 3];
    let result = arr[arr[true]];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(arr), BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test087():
    source = """
func nestedErrors() -> void {
    let complex = (5 + 3) * ("hello" + 2);
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(StringLiteral('hello'), +, IntegerLiteral(2))"
    assert Checker(source).check_from_source() == expected

def test088():
    source = """
func main() -> void {
    let intArray: [int; 3] = [1, 2, 3];
    let floatArray: [float; 3] = [1.0, 2.0, 3.0];
    let mixed1 = intArray[0] + floatArray[0];
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test088():
    source = """
func main() -> void {
    let intArray: [int; 3] = [1, 2, 3];
    let floatArray: [float; 3] = [1.0, 2.0, 3.0];
    let mixed1 = intArray[0] + floatArray[0];
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test089():
    source = """
func printMessage(msg: string) -> void {
    print(msg);
}
func main() -> void {
    let voidResult = printMessage("hi");
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(printMessage), [StringLiteral('hi')])"
    assert Checker(source).check_from_source() == expected

def test090():
    source = """
func add(a: int, b: int) -> int {
    return a + b;
}
func main() -> void {
    let wrongArgs = add(5, "hello");
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(add), [IntegerLiteral(5), StringLiteral('hello')])"
    assert Checker(source).check_from_source() == expected

def test091():
    source = """
func multiply(a: int, b: int) -> int {
    return a * b;
}
func main() -> void {
    let tooFewArgs = multiply(5);
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(multiply), [IntegerLiteral(5)])"
    assert Checker(source).check_from_source() == expected

def test092():
    source = """
func getValue() -> int {
    return 42;
}
func main() -> void {
    let tooManyArgs = getValue(1, 2);
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(getValue), [IntegerLiteral(1), IntegerLiteral(2)])"
    assert Checker(source).check_from_source() == expected

def test093():
    source = """
func main() -> void {
    let intArray: [int; 3] = [1, 2, 3];
    let floatArray: [float; 3] = [1.0, 2.0, 3.0];
    let result1 = intArray[floatArray[0]];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(intArray), ArrayAccess(Identifier(floatArray), IntegerLiteral(0)))"
    assert Checker(source).check_from_source() == expected

def test094():
    source = """
func main() -> void {
    let intArray: [int; 3] = [1, 2, 3];
    let stringArray: [string; 2] = ["a", "b"];
    let result2 = stringArray[intArray];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(stringArray), Identifier(intArray))"
    assert Checker(source).check_from_source() == expected

def test095():
    source = """
func main() -> void {
    let intArray: [int; 3] = [1, 2, 3];
    let stringArray: [string; 2] = ["a", "b"];
    let mixed2 = intArray[0] + stringArray[0];
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(ArrayAccess(Identifier(intArray), IntegerLiteral(0)), +, ArrayAccess(Identifier(stringArray), IntegerLiteral(0)))"
    assert Checker(source).check_from_source() == expected

def test096():
    source = """
func main() -> void {
    let arr = [1, 2, 3];
    let result = arr[arr[true]];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(arr), BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test097():
    source = """
func main() -> void {
    let complex = (5 + 3) * ("hello" + 2);
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(StringLiteral('hello'), +, IntegerLiteral(2))"
    assert Checker(source).check_from_source() == expected

def test098():
    source = """
func example() -> void {
    let x = 10;
    let x = 20;
}
"""
    expected = "Redeclared Variable: x"
    assert Checker(source).check_from_source() == expected

def test099():
    source = """
func calculate() -> int { return 42; }
func calculate() -> int { return 24; }
"""
    expected = "Redeclared Function: calculate"
    assert Checker(source).check_from_source() == expected

def test100():
    source = """
const PI = 3.14;
const PI = 3.14159;
"""
    expected = "Redeclared Constant: PI"
    assert Checker(source).check_from_source() == expected

def test101():
    source = """
func process(x: int, y: float, x: bool) -> void {
    print("Processing");
}
"""
    expected = "Redeclared Parameter: x"
    assert Checker(source).check_from_source() == expected

def test102():
    source = """
func mixed() -> void {
    let value = 42;
    const value = 100;
}
"""
    expected = "Redeclared Constant: value"
    assert Checker(source).check_from_source() == expected

def test103():
    source = """
func nested() -> void {
    if (true) {
        let temp = 1;
        let temp = 2;
    }
}
"""
    expected = "Redeclared Variable: temp"
    assert Checker(source).check_from_source() == expected

def test104():
    source = """
const globalVar = 100;
func shadowExample() -> void {
    let globalVar = 200;
    {
        let globalVar = 300;
    }
}
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test105():
    source = """
func main() -> void {
    print(str(undeclaredVar));
}
"""
    expected = "Undeclared Identifier: undeclaredVar"
    assert Checker(source).check_from_source() == expected

def test106():
    source = """
func main() -> void {
    undeclaredFunc();
}
"""
    expected = "Undeclared Function: undeclaredFunc"
    assert Checker(source).check_from_source() == expected

def test107():
    source = """
func beforeDeclaration() -> void {
    let result = x + 10;
    let x = 5;
}
"""
    expected = "Undeclared Identifier: x"
    assert Checker(source).check_from_source() == expected

def test108():
    source = """
func scopeError() -> void {
    if (true) {
        let localVar = 42;
    }
    print(str(localVar));
}
"""
    expected = "Undeclared Identifier: localVar"
    assert Checker(source).check_from_source() == expected

def test109():
    source = """
func shadowError() -> void {
    let x = 10;
    {
        let x = 20;
        {
            let y = x + 5;
        }
        let z = y + 1;
    }
}
"""
    expected = "Undeclared Identifier: y"
    assert Checker(source).check_from_source() == expected

def test110():
    source = """
func validCall() -> void {
    globalFunc();
}
func globalFunc() -> void {
    print("Global function");
}
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test112():
    source = """
const MAX_VALUE = 100;
func constError() -> void {
    let value = MAX_VALUE + 1;
}
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test113():
    source = """
func main() -> void {
    let numbers = [1, 2, 3];
    let result1 = numbers["invalid"];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(numbers), StringLiteral('invalid'))"
    assert Checker(source).check_from_source() == expected

def test114():
    source = """
func main() -> void {
    let numbers = [1, 2, 3];
    let result2 = numbers[3.14];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(numbers), FloatLiteral(3.14))"
    assert Checker(source).check_from_source() == expected

def test115():
    source = """
func main() -> void {
    let numbers = [1, 2, 3];
    let result3 = numbers[true];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(numbers), BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test116():
    source = """
func main() -> void {
    let x = 5;
    let y = true;
    let sum = x + y;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(Identifier(x), +, Identifier(y))"
    assert Checker(source).check_from_source() == expected

def test117():
    source = """
func main() -> void {
    let x = 5;
    let comparison = x < "hello";
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(Identifier(x), <, StringLiteral('hello'))"
    assert Checker(source).check_from_source() == expected

def test118():
    source = """
func main() -> void {
    let x = 5;
    let equality = x == 5.0;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(Identifier(x), ==, FloatLiteral(5.0))"
    assert Checker(source).check_from_source() == expected

def test119():
    source = """
func main() -> void {
    let x = 5;
    let y = true;
    let logical = x && y;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(Identifier(x), &&, Identifier(y))"
    assert Checker(source).check_from_source() == expected

def test120():
    source = """
func main() -> void {
    let condition = !42;
}
"""
    expected = "Type Mismatch In Expression: UnaryOp(!, IntegerLiteral(42))"
    assert Checker(source).check_from_source() == expected

def test121():
    source = """
func main() -> void {
    let negative = -true;
}
"""
    expected = "Type Mismatch In Expression: UnaryOp(-, BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test122():
    source = """
func main() -> void {
    let positive = +"text";
}
"""
    expected = "Type Mismatch In Expression: UnaryOp(+, StringLiteral('text'))"
    assert Checker(source).check_from_source() == expected