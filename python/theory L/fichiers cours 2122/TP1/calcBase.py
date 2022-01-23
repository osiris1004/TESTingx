# -----------------------------------------------------------------------------
# calc.py
#
# Expressions arithmétiques sans variables
# -----------------------------------------------------------------------------
#

from genereTreeGraphviz2 import printTreeGraph

VAR = {};

#statement keus
reserved = {
   'if' : 'IF',
   'then' : 'THEN',
   'print' : 'PRINT'
   }
#
tokens = [
    'NAME','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE',
    'LPAREN','RPAREN', 'COLON', 'AND', 'OR', 'EQUAL', 'EQUALS', 'LOWER','HIGHER'
    ]+list(reserved.values())


#t object use to store input
# Tokens
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t


# Tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUAL  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COLON = r';'
t_AND  = r'\&'
t_OR  = r'\|'
t_EQUALS  = r'=='
t_LOWER  = r'\<'
t_HIGHER  = r'\>'


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
import ply.lex as lex

lexer = lex.lex()

# Parsing rules

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'LOWER', 'HIGHER', 'EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)


def p_start(t):
    #linst === expression
    ''' start : linst'''
    t[0] = ('start', t[1])
    print(t[0])
    printTreeGraph(t[0])
    # eval(t[1])
    # evalInst(t[1])


def p_line(t):
    '''linst : linst inst
            | inst '''

    # s = 'print(1+2); x=4; x=x+1;           x=x+2;'
    # s = 'print(1+2); x=4;                  x=x+1;
    # s = 'print(1+2);                       x=4;
    # s =  print(1+2);                       last to execute
    if len(t) == 3:
        t[0] = ('bloc', t[1], t[2])
    else:
        t[0] = ('bloc', t[1], 'empty')


def p_statement_assign(t):
    'inst : NAME EQUAL expression COLON'
    t[0] = ('assign', t[1], t[3])



def p_statement_print(t):
    'inst : PRINT LPAREN expression RPAREN COLON'

    #t[Any thing] is determine from you grammar above
    t[0] = ('print', t[3])
    #'print(1+2);x=4;x=x+1;'


# def p_statement_expr(t):
#    'inst : expression COLON'
#
#    t[0] = t[1]


def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression OR expression
                  | expression AND expression
                  | expression EQUALS expression
                  | expression LOWER expression
                  | expression HIGHER expression
                  | expression DIVIDE expression'''
    t[0] = (t[2], t[1], t[3])


def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]


def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]


def p_expression_number(t):
    'expression : NUMBER'

    t[0] = t[1]


def p_expression_name(t):
    'expression : NAME'

    t[0] = t[1]


def p_error(t):
    print("Syntax error at '%s'" % t.value)


import ply.yacc as yacc

parser = yacc.yacc()

# s='1+2;x=4 if ;x=x+1;'
s = 'print(1+2);x=4;x=x+1;'

# with open("1.in") as file: # Use file to refer to the file object

# s = file.read()

parser.parse(s)


