import sys
import ply.lex as lex
import ply.yacc as yacc

class Node:
    def __init__(self, name, length, children):
        self.name = name
        self.length = length
        self.children = children.copy()

def treeprint(n, depth=0):
    if n:
        for i in range(0, depth):
            print("|  ", end="")
        print(f"\"{n.name}\":{n.length}")
        for m in n.children:
            treeprint(m, depth + 1)

tokens = [
    'SEMI',
    'COMMA',
    'LPAREN',
    'RPAREN',
    'STRING',
    'NUMBER',
]

t_SEMI = r'\;'
t_COMMA = r'\,'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_STRING(t):
    r'([^\,\;\:\(\)\[\]]+)'
    t.type = 'STRING'
    return t

def t_NUMBER(t):
    r':([0-9]+\.?[0-9]+([Ee]-?[0-9]+)?|[0-9]+)'
    t.type = 'NUMBER'
    return t

# Grammar origins: http://scikit-bio.org/docs/0.5.2/generated/skbio.io.format.newick.html
# NEWICK ==> NODE ;
# NODE ==> FORMATTING SUBTREE FORMATTING NODE_INFO FORMATTING
# SUBTREE ==> ( CHILDREN ) | null
# NODE_INFO ==> LABEL | LENGTH | LABEL FORMATTING LENGTH | null
# FORMATTING ==> [ COMMENT_CHARS ] | whitespace | null
# CHILDREN ==> NODE | CHILDREN , NODE
# LABEL ==> ' ALL_CHARS ' | SAFE_CHARS
# LENGTH ==> : FORMATTING NUMBER
# COMMENT_CHARS ==> any
# ALL_CHARS ==> any
# SAFE_CHARS ==> any except: ,;:()[] and whitespace
# NUMBER ==> a decimal or integer

def p_newick(p):
    '''
    newick : node SEMI
    '''
    p[0] = p[1]

def p_node(p):
    '''
    node : subtree info
    '''
    p[0] = Node(p[2][0], p[2][1], p[1])

def p_subtree_children(p):
    '''
    subtree : LPAREN children RPAREN
    '''
    p[0] = p[2]

def p_subtree_empty(p):
    '''
    subtree : empty
    '''
    p[0] = []

def p_info_label(p):
    '''
    info : label
    '''
    p[0] = (p[1], -1.0)

def p_info_length(p):
    '''
    info : length
    '''
    p[0] = ("", p[1])

def p_info_full(p):
    '''
    info : label length
    '''
    p[0] = (p[1], p[2])

def p_info_empty(p):
    '''
    info : empty
    '''
    p[0] = ("", -1.0)

def p_children_single(p):
    '''
    children : node
    '''
    p[0] = [p[1]]

def p_children_multi(p):
    '''
    children : children COMMA node
    '''
    p[0] = p[1] + [p[3]]

def p_label(p):
    '''
    label : STRING
    '''
    p[0] = p[1]

def p_length(p):
    '''
    length : NUMBER
    '''
    p[0] = float(p[1][1:])

def p_empty(p):
    '''
    empty :
    '''

def t_error(t):
    raise Exception(f"lexing error: {t.value}")

def p_error(p):
    raise Exception(f"parsing error: {p.value}")

lex = lex.lex()
parser = yacc.yacc()
treeprint(parser.parse(sys.stdin.read()))
