from utils import Tokenizer

def test_001():
    """Test single character identifier"""
    source = "x"
    expected = "x,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_002():
    """Test identifier starting with underscore"""
    source = "_value"
    expected = "_value,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_003():
    """Test mixed case identifier"""
    source = "mixedCase"
    expected = "mixedCase,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_004():
    """Test identifier with numbers"""
    source = "var123"
    expected = "var123,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_005():
    """Test long identifier"""
    source = "a"*50 + "1"*50
    expected = ("a"*50 + "1"*50) + ",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_006():
    """Test 'func' keyword"""
    source = "func"
    expected = "func,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_007():
    """Test 'let' keyword"""
    source = "let"
    expected = "let,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_008():
    """Test 'const' keyword"""
    source = "const"
    expected = "const,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_009():
    """Test 'if' keyword"""
    source = "if"
    expected = "if,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_010():
    """Test 'else' keyword"""
    source = "else"
    expected = "else,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_011():
    """Test 'while' keyword"""
    source = "while"
    expected = "while,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_012():
    """Test 'for' keyword"""
    source = "for"
    expected = "for,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_013():
    """Test 'return' keyword"""
    source = "return"
    expected = "return,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_014():
    """Test 'true' literal"""
    source = "true"
    expected = "true,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_015():
    """Test 'false' literal"""
    source = "false"
    expected = "false,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_016():
    """Test positive integer literal"""
    source = "42"
    expected = "42,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_017():
    """Test zero integer literal"""
    source = "0"
    expected = "0,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_018():
    """Test negative integer literal"""
    source = "-17"
    expected = "-,17,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_019():
    """Test integer with leading zeros"""
    source = "007"
    expected = "007,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_020():
    """Test float literal"""
    source = "3.14"
    expected = "3.14,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_021():
    """Test negative float literal"""
    source = "-2.5"
    expected = "-,2.5,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_022():
    """Test float with trailing decimal"""
    source = "42."
    expected = "42.,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_023():
    """Test float with exponent"""
    source = "1.23e10"
    expected = "1.23e10,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_024():
    """Test negative float with exponent"""
    source = "-4.56E-3"
    expected = "-,4.56E-3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_025():
    """Test basic string literal"""
    source = '"Hello"'
    expected = "Hello,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_026():
    """Test empty string literal"""
    source = '""'
    expected = ",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_027():
    """Test string with escape sequences"""
    source = r'"Line\nTab\tQuote\""'
    expected = r"Line\nTab\tQuote\",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_028():
    """Test unclosed string error"""
    source = '"Hello'
    expected = "Unclosed String: Hello"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_029():
    """Test illegal escape sequence"""
    source = r'"Bad \x escape"'
    expected = "Illegal Escape In String: Bad \\x"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_030():
    """Test addition operator"""
    source = "+"
    expected = "+,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_031():
    """Test subtraction operator"""
    source = "-"
    expected = "-,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_032():
    """Test multiplication operator"""
    source = "*"
    expected = "*,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_033():
    """Test division operator"""
    source = "/"
    expected = "/,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_034():
    """Test modulo operator"""
    source = "%"
    expected = "%,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_035():
    """Test equality operator"""
    source = "=="
    expected = "==,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_036():
    """Test inequality operator"""
    source = "!="
    expected = "!=,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_037():
    """Test less than operator"""
    source = "<"
    expected = "<,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_038():
    """Test less than or equal operator"""
    source = "<="
    expected = "<=,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_039():
    """Test greater than operator"""
    source = ">"
    expected = ">,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_040():
    """Test greater than or equal operator"""
    source = ">="
    expected = ">=,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_041():
    """Test logical AND operator"""
    source = "&&"
    expected = "&&,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_042():
    """Test logical OR operator"""
    source = "||"
    expected = "||,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_043():
    """Test logical NOT operator"""
    source = "!"
    expected = "!,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_044():
    """Test assignment operator"""
    source = "="
    expected = "=,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_045():
    """Test type annotation operator"""
    source = ":"
    expected = ":,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_046():
    """Test function return type operator"""
    source = "->"
    expected = "->,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_047():
    """Test pipeline operator"""
    source = ">>"
    expected = ">>,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_048():
    """Test parentheses"""
    source = "()"
    expected = "(,),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_049():
    """Test square brackets"""
    source = "[]"
    expected = "[,],EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_050():
    """Test curly braces"""
    source = "{}"
    expected = "{,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_051():
    """Test identifier after number without space"""
    source = "123abc"
    expected = "123,abc,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_052():
    """Test float with multiple decimals"""
    source = "3.14.15"
    expected = "3.14,.,15,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_053():
    """Test minus after number"""
    source = "123-456"
    expected = "123,-,456,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_054():
    """Test plus after number"""
    source = "123+456"
    expected = "123,+,456,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_055():
    """Test float starting with decimal"""
    source = ".14159"
    expected = ".,14159,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_056():
    """Test invalid float exponent"""
    source = "1.2e3.4"
    expected = "1.2e3,.,4,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_057():
    """Test string with only escape character"""
    source = r'"\"'
    expected = r"Unclosed String: \""
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_058():
    """Test string with unterminated escape"""
    source = "Hello '"
    expected = "Hello,Error Token '"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_059():
    """Test string with ASCII control characters"""
    source = '"\\x00\\x1F"'
    expected = "Illegal Escape In String: \\x"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_060():
    """Test string with unicode escape (should fail)"""
    source = r'"\u263A"'
    expected = "Illegal Escape In String: \\u"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_061():
    """Test operator without spaces between"""
    source = "x++y"
    expected = "x,+,+,y,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_062():
    """Test invalid operator combination"""
    source = "x**y"
    expected = "x,*,*,y,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_063():
    """Test comment inside string"""
    source = '"Hello // World"'
    expected = "Hello // World,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_064():
    """Test unclosed block comment"""
    source = "/* comment */"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_065():
    """Test nested block comments"""
    source = "/* Outer /* Inner */ Still outer */"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_066():
    """Test line comment inside block comment"""
    source = "/* // This is inside */"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_067():
    """Test empty block comment"""
    source = "/**/"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_068():
    """Test minus vs negative number"""
    source = "x-1"
    expected = "x,-,1,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_069():
    """Test whitespace in strange places"""
    source = "x  + \t \n \r 1"
    expected = "x,+,1,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_070():
    """Test tab in string"""
    source = '"Hello\tWorld"'
    expected = "Hello\tWorld,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_071():
    source =  ' "AHIHI'
    expected = "Unclosed String: AHIHI"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_072():
    """Test carriage return in string"""
    source = '"Hello\\x World"'
    expected = "Illegal Escape In String: Hello\\x"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_073():
    """Test string with only quote"""
    source = '"'
    expected = "Unclosed String: "
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_074():
    """Test string with backslash at end"""
    source = '"Hello\"'
    expected = "Hello,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_075():
    """Test invalid characters"""
    source = "x @ y"
    expected = "x,@,y,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_076():
    """Test non-ASCII characters"""
    source = "café"
    expected = 'caf,Error Token é'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_077():
    """invalid ID"""
    source = "012e"
    expected = '012,e,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_078():
    """Test minus after exponent must be 1.e-3"""
    source = "1.e-3"
    expected = "1.e-3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_079():
    """Test invalid float (multiple e's) e4 is ID"""
    source = "1.2e3e4"
    expected = "1.2e3,e4,EOF" 
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_080():
    """Test float with capital E"""
    source = "1.2E3"
    expected = "1.2E3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_081():
    """Test minus after exponent must be 1.e-3"""
    source = "1e-3"
    expected = "1,e,-,3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_082():
    """Test plus after exponent"""
    source = "1.e+3"
    expected = "1.e+3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_083():
    """Test empty exponent"""
    source = "1e"
    expected = "1,e,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_084():
    """Test exponent without number - ID"""
    source = "e9"
    expected = "e9,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_085():
    """Test dot after exponent"""
    source = "1.e3.4"
    expected = "1.e3,.,4,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_086():
    """Test multiple dots in float"""
    source = "1.2.3"
    expected = "1.2,.,3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_087():
    """Test minus minus sequence"""
    source = "x--y"
    expected = "x,-,-,y,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_088():
    """Test plus plus sequence"""
    source = "x++y"
    expected = "x,+,+,y,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_089():
    """Test arrow vs greater than"""
    source = "x->y>z"
    expected = "x,->,y,>,z,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_090():
    """Test pipe pipe (should be logical OR)"""
    source = "x||y"
    expected = "x,||,y,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_091():
    """Test ampersand ampersand (should be logical AND)"""
    source = "x&&y"
    expected = "x,&&,y,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_092():
    """Test exclamation equals (should be inequality)"""
    source = "x!=y"
    expected = "x,!=,y,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_093():
    """Test less than equals (should be <=)"""
    source = "x<=y"
    expected = "x,<=,y,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_094():
    """Test greater than equals (should be >=)"""
    source = "x>=y"
    expected = "x,>=,y,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_095():
    """Test equals equals (should be equality)"""
    source = "x==y"
    expected = "x,==,y,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_096():
    """Test right shift vs two greater thans"""
    source = "x>>y"
    expected = "x,>>,y,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_097():
    """Test minus greater than (should be ->)"""
    source = "x->y"
    expected = "x,->,y,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_098():
    """Test all operators together"""
    source = "x+y-z*a/b%c==d!=e<f<=g>h>=i&&j||k!l"
    expected = "x,+,y,-,z,*,a,/,b,%,c,==,d,!=,e,<,f,<=,g,>,h,>=,i,&&,j,||,k,!,l,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_099():
    """Test all separators together"""
    source = "()[]{},;:"
    expected = "(,),[,],{,},,,;,:,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_100():
    """Test everything mixed together"""
    source = 'let x: int = 42 + (3.14 * "Hello\\nWorld"); // Comment'
    expected = 'let,x,:,int,=,42,+,(,3.14,*,Hello\\nWorld,),;,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected