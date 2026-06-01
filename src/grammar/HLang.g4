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

// ==========================================
// LEXER - TOKENS
// ==========================================

// Keywords (before ID)
BOOL       : 'bool'    ;
BREAK      : 'break'   ;
CONST      : 'const'   ;
CONTINUE   : 'continue';
ELSE       : 'else'    ;
FLOAT      : 'float'   ;
FOR        : 'for'     ;
FUNC       : 'func'    ;
IF         : 'if'      ;
IN         : 'in'      ;
INT        : 'int'     ;
LET        : 'let'     ;
RETURN     : 'return'  ;
STRING     : 'string'  ;
VOID       : 'void'    ;
WHILE      : 'while'   ;
TRUE       : 'true'    ;
FALSE      : 'false'   ;

// Numeric Literals
INT_LIT  : INT_PART;
FLOAT_LIT: INT_PART DECI_PART EXPO_PART? ;

// String Literals & Errors
STRING_LIT    : '"' (ESC_SEQ | STRING_CHAR)* '"'        { self.text = self.text[1:-1] };
ILLEGAL_ESCAPE: '"' (ESC_SEQ | STRING_CHAR)* UNESC_SEQ  { self.text = self.text[1:] };
UNCLOSE_STRING: '"' (ESC_SEQ | STRING_CHAR)*            { self.text = self.text[1:] };

// Operators (2 ky tu duoc catch truoc)
PIPE_LINE            : '>>' ;
FUNCTION_RETURN_TYPE : '->' ;
EQUAL                : '==' ;
NEQUAL               : '!=' ;
LTE                  : '<=' ;
GTE                  : '>=' ;
AND                  : '&&' ;
OR                   : '||' ;

MUL        : '*' ;
PLUS       : '+' ;
MINUS      : '-' ;
DIV        : '/' ;
MODU       : '%' ;
LT         : '<' ;
GT         : '>' ;
NOT        : '!' ;
ASSIGNMENT : '=' ;
COLON      : ':' ;
DOT        : '.' ;

// Separators
LPAREN  : '(' ;
RPAREN  : ')' ;
LBRACK  : '[' ;
RBRACK  : ']' ;
LCBRACK : '{' ;
RCBRACK : '}' ;
COMMA   : ',' ;
SEMI    : ';' ;

// Identifier
ID: (LETTER | UNDERSCORE) (LETTER | DIGIT | UNDERSCORE)*;

// Comments
LINE_COMMENT  : '//' [\u0000-\u0009\u000B\u000C\u000E-\u007F]* -> skip ;
BLOCK_COMMENT : '/*'    (BLOCK_COMMENT | [\u0000-\u007F])*?     '*/' -> skip ;
WS            : [ \t\r\n]+ -> skip ;

// cac ky tu con lai, CO THE CATCH do nam trong 0-127 nhung khong dung toi
ERR_HASH      : '#' ;
ERR_DOLLAR    : '$' ;
ERR_QUESTION  : '?' ;
ERR_AT        : '@' ;
ERR_BACKSLASH : '\\';
ERR_CARET     : '^' ;
ERR_BACKTICK  : '`' ;
ERR_TILDE     : '~' ;
ERR_QUOTE     : '\'' ;
ERR_AMP       : '&' ;
ERR_BAR       : '|' ;
ERR_NON_PRINTABLE   : [\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F] ;

ERROR_CHAR: . ;

// Fragments
fragment INT_PART    : DIGIT+;
fragment DECI_PART   : '.' DIGIT*;
fragment EXPO_PART   : [eE] [+-]? DIGIT+ ;
fragment STRING_CHAR:   [\u0020-\u0021\u0023-\u005B\u005D-\u007E];
fragment ESC_SEQ     : '\\' [ntr"\\];
fragment UNESC_SEQ   : '\\' ~[ntr"\\];
fragment LETTER      : [A-Za-z];
fragment DIGIT       : [0-9];
fragment UNDERSCORE  : '_';

// ==========================================
// PARSER - GRAMMAR
// ==========================================

program: (funcdecl | constdecl)* EOF;

constdecl: CONST ID (COLON type1)? ASSIGNMENT expr SEMI;

// Literals ở tầng Parser
literal
    : INT_LIT
    | FLOAT_LIT
    | bool_lit
    | STRING_LIT
    | array_lit
    ;

bool_lit : TRUE | FALSE;
array_lit: LBRACK (expr (COMMA expr)*)? RBRACK;

// Expressions & Precedence (8 cao nhat -> 0 thap nhat)
expr :  expr1  (PIPE_LINE expr1)*;
expr1:  expr2  (OR expr2)*;
expr2:  expr3  (AND expr3)*;
expr3:  expr4  ((EQUAL | NEQUAL) expr4)*;
expr4:  expr5  ((LT | LTE | GT | GTE) expr5)*;
expr5:  expr6  ((PLUS | MINUS) expr6)*;
expr6:  expr7  ((MUL | DIV | MODU) expr7)*;
expr7:  (NOT | MINUS | PLUS)* expr8;
expr8:  primary_expression (LBRACK expr RBRACK)*;

primary_expression
    : literal
    | func_call
    | ID
    | LPAREN expr RPAREN
    ;

func_call    : ID LPAREN argument_list? RPAREN;
argument_list: expr (COMMA expr)*;

statement
    : expression_stmt
    | vardecl_stmt
    | constdecl
    | assignment_stmt
    | conditional_stmt
    | loop_stmt
    | controlflow_stmt
    | block_stmt
    ;

expression_stmt : expr SEMI;
vardecl_stmt    : LET ID (COLON type1)? ASSIGNMENT expr SEMI;
assignment_stmt : expr8 ASSIGNMENT expr SEMI;

conditional_stmt
    : IF LPAREN expr RPAREN statement_block
      (ELSE IF LPAREN expr RPAREN statement_block)*
      (ELSE statement_block)?
    ;

statement_block: LCBRACK statement* RCBRACK;

loop_stmt
    : WHILE LPAREN expr RPAREN statement_block
    | FOR LPAREN ID IN expr RPAREN statement_block
    ;

controlflow_stmt
    : BREAK SEMI
    | CONTINUE SEMI
    | RETURN expr? SEMI
    ;

block_stmt: LCBRACK statement* RCBRACK;

type1
    : primitiveType
    | arrayType
    ;

primitiveType: INT | FLOAT | BOOL | STRING | VOID;
arrayType    : LBRACK type1 SEMI INT_LIT RBRACK;

funcdecl    : FUNC ID LPAREN parameterList? RPAREN FUNCTION_RETURN_TYPE type1 body;
parameterList: parameter (COMMA parameter)*;
parameter   : ID COLON type1;
body        : LCBRACK statement* RCBRACK;
