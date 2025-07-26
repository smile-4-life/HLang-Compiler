grammar HLang;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type

    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

//2 ki tu nen duoc catch truoc 1 ki tu
EQUAL:  '==';
NEQUAL: '!=';
LTE:    '<=';
GTE:    '>=';
AND:    '&&';
OR:     '||';
PIPE_LINE: '>>';
FUNCTION_RETURN_TYPE: '->';

//comment
fragment DBSLASH:      '//';
fragment OPENCOMMENT:  '/*';
fragment CLOSECOMMENT: '*/';
LINE_COMMENT
    : DBSLASH [\t\u0020-\u007E]* -> skip
    ;

BLOCK_COMMENT
    : OPENCOMMENT (BLOCK_COMMENT | .)*? CLOSECOMMENT -> skip
    ;

//0-31: not printable
//SPACE       : ' '     ; // 32 (wrote in skip case)
NOT         : '!'     ; // 33
fragment DBQUOTE: '"'   ; // 34
HASH        : '#'     ; // 35
DOLLAR      : '$'     ; // 36
MODU        : '%'     ; // 37
AMP         : '&'     ; // 38
QUOTE       : '\''    ; // 39
LB          : '('     ; // 40
RB          : ')'     ; // 41
MUL         : '*'     ; // 42
PLUS        : '+'     ; // 43
COMMA       : ','     ; // 44
MINUS       : '-'     ; // 45
DOT         : '.'     ; // 46
DIV         : '/'     ; // 47

// 48–57: (0–9)

COLON       : ':'     ; // 58
SEMI        : ';'     ; // 59
LT          : '<'     ; // 60
ASSIGNMENT  : '='     ; // 61
GT          : '>'     ; // 62
QUESTION    : '?'     ; // 63
AT          : '@'     ; // 64

// 65–90: (A–Z) 

LP          : '['     ; // 91
BACKSLASH   : '\\'    ; // 92
RP          : ']'     ; // 93
CARET       : '^'     ; // 94
UNDERSCORE  : '_'     ; // 95
BACKTICK    : '`'     ; // 96

// 97–122: (a–z)

LCB         : '{'     ; // 123
PIPE        : '|'     ; // 124
RCB         : '}'     ; // 125
TILDE       : '~'     ; // 126

//keywords
BOOL      : 'bool'    ;
BREAK     : 'break'   ;
CONST     : 'const'   ;
CONTINUE  : 'continue';
ELSE      : 'else'    ;
FLOAT     : 'float'   ;
FOR       : 'for'     ;
FUNC      : 'func'    ;
IF        : 'if'      ;
IN        : 'in'      ;
INT       : 'int'     ;
LET       : 'let'     ;
RETURN    : 'return'  ;
STRING    : 'string'  ;
VOID      : 'void'    ;
WHILE     : 'while'   ;
fragment FALSE     : 'false'   ;
fragment  TRUE     : 'true'    ;

//LITERALS
literals: INT_LIT | FLOAT_LIT | BOOL_LIT | STRING_LIT | array_lit;

//integer literal
INT_LIT: INT_PART;
fragment INT_PART: DIGIT+;

//float literal
FLOAT_LIT: INT_PART DECI_PART EXPO_PART?;
fragment DECI_PART: DOT DIGIT*;
fragment EXPO_PART: [eE] (PLUS | MINUS)? DIGIT+;

//boolean literal
BOOL_LIT: (TRUE | FALSE)
    ;

//string literal
STRING_LIT:     DBQUOTE (ESC_SEQ | STRING_CHAR)* DBQUOTE    {
    self.text = self.text[1:-1]
    };
//illegal escape
ILLEGAL_ESCAPE: DBQUOTE (ESC_SEQ | STRING_CHAR)* UNESC_SEQ  {
    self.text = self.text[1:]
    };
//unclose string
UNCLOSE_STRING: DBQUOTE (ESC_SEQ | STRING_CHAR)*            {
    self.text = self.text[1:]
    };

//string helper
fragment STRING_CHAR:   [\u0020-\u0021\u0023-\u005B\u005D-\u007E];
fragment ESC_SEQ    :   '\\'  [ntr"\\];
fragment UNESC_SEQ  :   '\\' ~[ntr"\\];

array_lit: LP (expr (COMMA expr)*)? RP;

//catch keyword before ID
fragment LETTER: [A-Za-z];
fragment DIGIT:[0-9];    
ID: (LETTER | UNDERSCORE) (LETTER | DIGIT | UNDERSCORE)*;

/////////////////////////////////////////
/////////////// PARSER //////////////////
/////////////////////////////////////////
program: (funcdecl | constdecl)*  EOF; 

constdecl: CONST ID (COLON type1)? ASSIGNMENT expr SEMI;

//funcdecl locates at bottom

//primitive_type: INT | FLOAT | BOOL | STRING | VOID;

expr:   expr1 (PIPE_LINE expr1)*;
expr1:  expr2 (OR expr2)*;
expr2:  expr3 (AND expr3)*;
expr3:  expr4 ((EQUAL | NEQUAL) expr4)*;
expr4:  expr5 ((LT | LTE | GT | GTE) expr5)*;
expr5:  expr6 ((PLUS | MINUS) expr6)*;
expr6:  expr7 ((MUL | DIV | MODU) expr7)*;
expr7:  (NOT | MINUS | PLUS)* expr8;
expr8: primary_expression (LP expr RP)*;

// atom 
primary_expression
    : literals
    | identifier
    | func_call
    | LB expr RB
    ;

//identifier
identifier: ID;

//function call
func_call: identifier LB argument_list? RB;
argument_list: expr (COMMA expr)*;

statement
    : expression_stmt
    | vardecl_stmt
    | assignment_stmt
    | conditional_stmt
    | loop_stmt
    | controlflow_stmt
    | block_stmt
    ;

// Expression statements
expression_stmt
    : expr SEMI
    ;

// Variable declarations
vardecl_stmt
    : LET ID (COLON type1)? ASSIGNMENT expr SEMI
    ;

// Assignment statements
assignment_stmt
    : expr8 ASSIGNMENT expr SEMI
    ;

// Conditional statements
conditional_stmt
    : IF LB expr RB statement_block (ELSE IF LB expr RB statement_block)* (ELSE statement_block)?
    ;

//statement_block
statement_block: LCB statement* RCB;

// Loop statements
loop_stmt
    : whileLoop
    | forLoop
    ;
whileLoop
    : WHILE LB        expr  RB statement_block
    ;
forLoop
    : FOR   LB  ID IN expr  RB statement_block
    ;

// Control flow statements
controlflow_stmt
    :    break_stmt
    | continue_stmt
    |   return_stmt
    ;

break_stmt
    :        BREAK SEMI
    ;

continue_stmt
    :     CONTINUE SEMI
    ;

return_stmt
    : RETURN expr? SEMI
    ;

// Block statements
block_stmt
    : LCB statement* RCB
    ;

type1
    :   primitiveType
    |       arrayType
    | userDefinedType
    ;

primitiveType
    : INT
    | FLOAT
    | BOOL
    | STRING
    | VOID
    ;

arrayType
    :
    (LP arrayType SEMI INT_LIT RP) | (LP type1 SEMI INT_LIT RP)
    ;

userDefinedType
    : ID  // For custom types/classes
    ;


// All funcdecl
funcdecl
    : FUNC ID LB parameterList? RB FUNCTION_RETURN_TYPE type1 body
    ;

// Parameter list
parameterList
    : parameter (COMMA parameter)*
    ;

// Single parameter
parameter
    : ID COLON type1
    ;

// Function call
functionCall
    : expr LB argumentList? RB
    ;

// Argument list
argumentList
    : expr (SEMI expr)*
    ;

// Block (function body)
body
    : LCB statement* RCB
    ;

WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs 

ERROR_CHAR: .;