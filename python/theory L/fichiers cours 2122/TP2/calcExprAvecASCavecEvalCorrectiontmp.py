#from genereTreeGraphviz2 import printTreeGraph
var = {}
var_function = {}

#for python
reserved = {

   'print' : 'PRINT',
    'if'   : 'IF',
    'while'   : 'WHILE',
    'for'   : 'FOR',
    'function':'FUNCTION'

   }

tokens = [
    'NAME','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE',
    'LPAREN','RPAREN', 'COLON', 'AND', 'OR', 'EQUAL', 'EQUALS', 'LOWER','HIGHER',
    'LBRACE','RBRACE'
    ]+list(reserved.values())

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
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'




def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t

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
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'LOWER', 'HIGHER', 'EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),

)
 
   
    
def p_start(p):
    'start : linst'
    p[0] = ('start', p[1])
    print('Arbre de dérivation = ',p[0])
    #printTreeGraph(p[1])
    print('CALC> ',eval_inst(p[1]))

def p_line(p):
    '''linst : linst inst COLON
            | inst COLON'''
    # s = 'print(1+2); x=4; x=x+1;x=x+2;
    # s = 'print(1+2); x=4; x=x+1;           x=x+2;'
    # s = 'print(1+2); x=4;                  x=x+1;
    # s = 'print(1+2);                       x=4;
    # s =  print(1+2);                       last to execute
    if len(p) == 4 :
        p[0] = ('bloc', p[1], p[2])
    else:
        p[0] = ('bloc', p[1], 'empty')
def p_expression_function(p):
    '''inst : FUNCTION NAME LPAREN RPAREN LBRACE linst RBRACE
            | FUNCTION NAME LPAREN inst RPAREN LBRACE linst RBRACE'''
    if len(p) == 8:
        p[0] = ('functionEmpty', p[2], p[6])
    elif len(p) == 9:
        p[0] = ('functionPrame', p[2], p[4], p[7])

def p_expression_function_call(p):
    'inst : NAME LPAREN RPAREN COLON'
    p[0] = ('call',p[1],"Empty")



def p_statement_assign(p):
    'inst : NAME EQUAL expression'
    # var[key] = value
    p[0] = ('assign', p[1], p[3])
    #print(p[0])


def p_statement_print(p):
    '''inst : PRINT LPAREN expression RPAREN'''

    #t[Any thing] is determine from you grammar above
    p[0] = ('print', p[3])
    #'print(1+2);x=4;x=x+1;'

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
    
def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] =  p[2] 

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_error(p):
    print("Syntax error at '%s'" % p.value)

def p_expression_name(p):
    'expression : NAME'
    p[0] = p[1]

def p_expression_if(p):
    'inst : IF LPAREN  expression RPAREN  LBRACE linst RBRACE'
    p[0] = ('if', p[3], p[6])

def p_expression_while(p):
    'inst : WHILE LPAREN  expression RPAREN  LBRACE linst RBRACE'
    p[0] = ('while', p[3], p[6])

def p_expression_for(p):
    'inst : FOR LPAREN inst COLON expression COLON inst RPAREN LBRACE linst RBRACE'
    p[0] = ('for', p[3], p[5],p[7],p[10])



       

#--***---***--**--


import ply.yacc as yacc
yacc.yacc()



def eval_expression (t):
    #print('eval de ',t, type(t), len(t))

    if type(t) is int:
        return t

    elif type(t) is str:
        return var[t] #store---
    #print('tree not tuple', t)



    elif type(t) is  tuple:
        if t[0] == '+' :  return eval_expression(t[1]) + eval_expression(t[2])
        if t[0] == '-':  return eval_expression(t[1]) - eval_expression(t[2])
        if t[0] == '*' :  return eval_expression(t[1]) * eval_expression(t[2])
        if t[0] == '/':  return eval_expression(t[1]) / eval_expression(t[2])
        if t[0] == '|':  return eval_expression(t[1]) | eval_expression(t[2])
        if t[0] == '&':  return eval_expression(t[1]) & eval_expression(t[2])
        #return boolean
        if t[0] == '>':  return eval_expression(t[1]) > eval_expression(t[2])
        if t[0] == '<':  return eval_expression(t[1]) < eval_expression(t[2])
        if t[0] == '==':  return eval_expression(t[1]) == eval_expression(t[2])

    return 'UNK'

def eval_inst(t):

    print("eval_expression = ",t)
    if t == "Empty":
        return
    elif t[0] == "bloc":
        eval_inst(t[1])
        eval_inst(t[2])

    elif t[0] == "print":
        print("calcBase= ",eval_expression(t[1]))

    elif t[0] == "assign":
        var[t[1]] = eval_expression(t[2])


    elif t[0] == 'if':
        if eval_expression(t[1]):
            eval_inst(t[2])

    elif t[0] == 'while':
        while bool(eval_expression(t[1])) == True:
            eval_inst(t[2])


    elif t[0] == 'for':
        eval_inst(t[1]) #initialization
        while bool(eval_expression(t[2])) == True:
            eval_inst(t[3]) #initialization + loop increamnet
            eval_inst(t[4]) #block in print

    elif t[0] == 'functionEmpty':
            var_function[t[1]] = ("Empty",t[2])

    elif t[0] == 'call':
        eval_inst(var_function[t[1]][1])    

        #{'carre': ('empty', ('bloc', ('print', 2), 'empty'))} 
        #{NOM : (paramètres, corps)}


       






#s = 'a = (1+1)+1;print(a);if(1>0);'
#s = 'toto=2; titi = toto+2; if(titi<toto){print(titi);};'
#s = 'toto=2; titi = toto+2; while(titi<toto){print(titi);};'
#s = 'for(i=0; i<10; i=i+1){print(i);};'
#s='function carre(){print(2);}; carre();'




yacc.parse(s)

# elif t[0] in ['+', '-', '*', '/', '<', '>', '&', '|']:
#   return eval_expression(t)