import ply.lex as lex
import minipar.interpreter as inter

# Tokens list
tokens = [
    'SEQ', 'PAR', 'IF', 'ELSE', 'WHILE', 'LOG',
    'SEND', 'RECEIVE',
    'ID', 'INT', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'COMMA', 'EQUALS', 'LESS_THAN', 'GREATER_THAN', 
    'LESS_THAN_EQUALS', 'GREATER_THAN_EQUALS', 
    'EQUALS_EQUALS', 'NOT_EQUALS', 'COMMENT', 'C_CHANNEL', 'DOT',
    'FIBONACCI', 'FACTORIAL'
]

# Regular expressions for the tokens
t_SEQ = r'SEQ'
t_PAR = r'PAR'
t_IF = r'if'
t_ELSE = r'else'
t_WHILE = r'while'
t_LOG = r'log'
t_SEND = r'send'
t_RECEIVE = r'receive'
t_FIBONACCI = r'fibonacci'
t_FACTORIAL = r'factorial'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_EQUALS = r'='
t_LESS_THAN = r'<'
t_GREATER_THAN = r'>'
t_LESS_THAN_EQUALS = r'<='
t_GREATER_THAN_EQUALS = r'>='
t_EQUALS_EQUALS = r'=='
t_NOT_EQUALS = r'!='
t_C_CHANNEL = r'c_channel'
t_DOT = r'\.'


# Ignore all white spaces
t_ignore = ' \t\n\r'

# Rule for complex tokens
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    reserved = {
        'SEQ', 'PAR', 'if', 'else', 'while', 'log',
        'send', 'receive', 'c_channel', 'fibonacci', 'factorial'
    }
    if t.value in reserved:
        t.type = t.value.upper()
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"[^"\n]*"|\'[^\'\n]*\''
    t.value = t.value[1:-1]  # Remove ticks
    return t

# Remove illegal characters
def t_error(t):
    inter.has_error = True
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

def t_COMMENT(t):
    r'\#.*\n?'
    pass  # Ignore comments


# Create lexical analyzer
lexer = lex.lex()
