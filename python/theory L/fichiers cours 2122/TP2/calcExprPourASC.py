from genereTreeGraphviz2 import printTreeGraph# à copier coller dans le script sinon

tokens = (
    'NUMBER','MINUS',
    'PLUS','TIMES','DIVIDE',
    'LPAREN','RPAREN'
    )

# Tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
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
lex.lex()

precedence = (
 
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
 
    )
 
   
    
def p_start(p):
    'start : expression'
    p[0] = ('START',p[1])
    print(p[0])
    printTreeGraph(p[0])

def p_expression_binop_plus(p):
    'expression : expression PLUS expression'
    
    
def p_expression_binop_times(p):
    'expression : expression TIMES expression'
    

 
    
def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    

def p_expression_number(p):
    'expression : NUMBER'
     

def p_error(p):
    print("Syntax error at '%s'" % p.value)

import ply.yacc as yacc
yacc.yacc()

s = '(1+2)*3'
yacc.parse(s)

    