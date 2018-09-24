from expression import *
tokens = (
    'VAR', 'ZERO', 'ONE',
    'AND', 'OR','IMPLY','IFF','NOT',
    'LPAREN', 'RPAREN',
    )

#tokens

t_OR = r'\\/'
t_AND = r'/\\'
t_IMPLY = r'->'
t_IFF = r'<->'
t_NOT = r'~'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ZERO = r'0'
t_ONE = r'1'

def t_VAR(t):
    r'[a-zA-Z]\w*'
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

import ply.lex as lex
lexer = lex.lex()

precedence = (
    ('right','IFF'),
    ('right','IMPLY'),
    ('left','OR'),
    ('left','AND'),
    ('left','NOT'),
    )

def p_expression_binop(t):
    '''expression : expression OR expression
                  | expression AND expression
                  | expression IFF expression
                  | expression IMPLY expression
    '''
    t[0] = BinopExp(t[2],t[1],t[3])

def p_expression_negate(t):
    'expression : NOT expression'

    t[0] = NegExp(t[2])

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_term(t):
    '''expression : ZERO
                  | ONE
                  | VAR
    '''
    t[0] = TermExp(t[1])

def p_error(t):
    print(f'Syntax error at {t[1]}')

import ply.yacc as yacc
parser = yacc.yacc()

