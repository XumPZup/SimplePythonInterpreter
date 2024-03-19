import ply.yacc as yacc
from minipar.interpreter import symbol_table
from minipar.lexer import tokens
import minipar.interpreter as inter 


# Operators' priority 
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('nonassoc', 'LESS_THAN', 'GREATER_THAN', 'LESS_THAN_EQUALS', 'GREATER_THAN_EQUALS', 'EQUALS_EQUALS', 'NOT_EQUALS'),
)


# Sytactic rules
def p_programa_minipar(p):
    '''programa_minipar : bloco_stmt'''
    p[0] = p[1]

def p_bloco_stmt(p):
    '''bloco_stmt : bloco_SEQ
                  | bloco_PAR
                  | bloco_stmt bloco_SEQ
                  | bloco_stmt bloco_PAR'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2])

def p_bloco_SEQ(p):
    '''bloco_SEQ : SEQ stmts'''
    p[0] = ('SEQ', p[2])

def p_bloco_PAR(p):
    '''bloco_PAR : PAR stmts'''
    p[0] = ('PAR', p[2])

def p_bloco_IF(p):
    '''bloco_IF : IF LPAREN bool RPAREN LBRACE stmts RBRACE'''
    p[0] = ('IF', p[3], p[6])

def p_bloco_WHILE(p):
    '''bloco_WHILE : WHILE LPAREN bool RPAREN LBRACE stmts RBRACE'''
    p[0] = ('WHILE', p[3], p[6])

def p_bloco_LOG(p):
    '''bloco_LOG : LOG LPAREN output_args RPAREN'''
    p[0] = ('LOG', p[3])

def p_output_args(p):
    '''output_args : expr
                   | output_args COMMA expr'''
    if len(p) == 2:
        p[0] = (p[1],)
    else:
        p[0] = p[1] + (p[3],)

def p_stmts(p):
    '''stmts : stmt
             | stmts stmt'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_stmt(p):
    '''stmt : atribuicao
            | bloco_IF
            | bloco_WHILE
            | bloco_LOG
            | c_channel
            | c_channel_stmt
            | fibonacci
            | factorial'''
    p[0] = p[1]

def p_fibonacci(p):
    '''fibonacci : FIBONACCI LPAREN INT RPAREN'''
    p[0] = ('FIBONACCI', p[3]) 

def p_factorial(p):
    '''factorial : FACTORIAL LPAREN INT RPAREN'''
    p[0] = ('FACTORIAL', p[3]) 

def p_atribuicao(p):
    '''atribuicao : ID EQUALS expr
                  | ID EQUALS STRING
                  | ID EQUALS receive_stmt'''
                  
    p[0] = ('=', p[1], p[3])
    if p[1] not in symbol_table: 
        symbol_table[p[1]] = p[3]

def p_expr(p):
    '''expr : INT
            | STRING
            | expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr
            | expr LESS_THAN expr
            | expr GREATER_THAN expr
            | expr LESS_THAN_EQUALS expr
            | expr GREATER_THAN_EQUALS expr
            | expr EQUALS_EQUALS expr
            | expr NOT_EQUALS expr
            '''
 
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_expr_id(p):
    '''expr : ID'''
    if p[1] not in symbol_table:
        print(f"Semantic error: variable '{p[1]}' was not defined")
        inter.has_error = True
    p[0] = p[1]

def p_bool(p):
    '''bool : expr'''
    p[0] = p[1]

def p_comment(p):
    '''comment : COMMENT'''
    pass  # Comments are ignored

def p_c_channel(p):
    '''c_channel : C_CHANNEL ID LPAREN STRING COMMA STRING RPAREN'''
    p[0] = ('C_CHANNEL', p[2], p[4], p[6])

    inter.channels[p[2]] = (p[4],p[6])

def p_c_channel_stmt(p):
    '''c_channel_stmt : send_stmt
                      | receive_stmt''' 
    p[0] = p[1]

def p_send_stmt(p):
    '''send_stmt : ID DOT SEND LPAREN ID COMMA expr COMMA expr COMMA expr RPAREN
                 | ID DOT SEND LPAREN ID RPAREN'''
    if len(p) == 7:
            p[0] = (p[1], 'SEND', p[5])
    elif len(p) == 13:
        p[0] = (p[1], 'SEND', p[5], p[7], p[9], p[11])
    
    if p[1] not in inter.channels:
        print(f"Semantic error: variable '{p[1]}' in '{p[1]}.{p[3]}()' was not defined")
        inter.has_error = True

def p_receive_stmt(p):
    '''receive_stmt : ID DOT RECEIVE LPAREN ID COMMA expr COMMA expr COMMA expr RPAREN
                    | ID DOT RECEIVE LPAREN ID RPAREN'''
    if len(p) == 7:
            p[0] = (p[1], 'RECEIVE', p[5])
    elif len(p) == 13:
        p[0] = (p[1], 'RECEIVE', p[5], p[7], p[9], p[11])
    
    if p[1] not in inter.channels:
        print(f"Semantic error: variable '{p[1]}' in '{p[1]}.{p[3]}()' was not defined")
        inter.has_error = True

def p_error(p):
    inter.has_error = True
    if p:
        print(f"Semantic error at line {p.lineno}, token '{p.value}'")
        exit()
        
    else:
        print("Smantic error: unexpected end of the file")
    parser.errok()
    
# Create syntactic analyzer
parser = yacc.yacc()
