# hw2

from math import log, floor
import re



#1.a
def variable(tokens):
    keywords = ['xor', 'not', 'true', 'false', 'log', 'print', 'assign', 'if', 'while']
    if not type(tokens[0]) == type(''):
        return None
    if tokens[0] == '':
        return None
    if re.match(r"^([a-z]|[a-z][a-zA-Z0-9]+)$", tokens[0]):
        for word in keywords:
            if tokens[0] == word:
                return (None, tokens[0:])
                break
        return (tokens[0], tokens[1:])


def variable1(tokens):
    keywords = ['xor', 'not', 'true', 'false', 'log', 'print', 'assign', 'if', 'while']
    if not type(tokens[0]) == type(''):
        return None
    if tokens[0] == '':
        return None
    if re.match(r"^([a-z]|[a-z][a-zA-Z0-9]+)$", tokens[0]):
        for word in keywords:
            if tokens[0] == word:
                return (None, tokens[0:])
                break
        return ({'Variable': [tokens[0]]}, tokens[1:])


def number(tokens):
    if re.match(r"^(-?[1-9][0-9]*)$", tokens[0]):
        return (int(tokens[0]), tokens[1:])
    elif re.match(r"^(-?[0-9])$", tokens[0]):
        return (int(tokens[0]), tokens[1:])


#1.b
def parse(seqs, token, top=False):
    for (label, seq) in seqs:
        tokens = token[0:]  #make a copy of the tokens
        ss = []  #count the token consumed
        es = []  #list of the children
        for x in seq:
            if type(x) == type(''):
                if x == tokens[0]:
                    tokens = tokens[1:]  #the first token matches,cut it
                    ss = ss + [x]  # add the cutted token into consumed list
                else:
                    break
            else:
                r = x(tokens)
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]
                    if len(tokens) == 0:
                        break
        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                if label == 'Left':
                    return (es[0], tokens)
                elif label == 'Factor':
                    return (es[0], tokens)
                else:
                    return ({label: es} if len(es) > 0 else label, tokens)


def formulaLeft(tokens):
    seqs = [ \
        ('Not', ['not', '(', formula0, ')']), \
        ('Parens', ['(', formula0, ')']), \
        ('True', ['true']), \
        ('False', ['false']), \
        ('Variable', [variable]) \
        ]

    return parse(seqs, tokens)


def formula0(tokens):
    seqs = [ \
        ('Xor', [formulaLeft, 'xor', formula0]), \
        ('Equal', [formulaLeft, '==', formula0]),\
        ('Equal', [term0, '==', term0]),\
        ('LessThan', [formulaLeft, '<', formula0]),\
        ('LessThan', [term0, '<', term0]),\
        ('Left', [formulaLeft]) \
        ]
    return parse(seqs, tokens)


def formula(tokens):
    (e1, tokens) = formula0(tokens)
    if not len(tokens) == 0:
        return None
    else:
        return (e1, tokens)



#1.c
def term(tokens):
    (e1, tokens) = term0(tokens)
    if not len(tokens) == 0:
        return None
    else:
        return (e1, tokens)


def term0(tokens):
    seqs = [ \
        ('Plus', [factor, '+', term0]), \
        ('Factor', [factor]) \
        ]

    return parse(seqs, tokens)


def factor(tokens):
    seqs = [ \
        ('Mult', [factorLeft, '*', factor]), \
        ('Left', [factorLeft]) \
        ]

    return parse(seqs, tokens)


def factorLeft(tokens):
    seqs = [ \
        ('Log', ['log', '(', term0, ')']), \
        ('Parens', ['(', term0, ')']), \
        ('Variable', [variable]), \
        ('Number', [number]) \
        ]

    return parse(seqs, tokens)


#1.d

def expressionTerm(tokens):
    if not term0(tokens) == None:
        (e2, tokens) = term0(tokens)
        if not e2 == None:
            return (e2, tokens)
    else:
        return None


def expressionFormula(tokens):
    if not formula0(tokens) == None:
        (e1, tokens) = formula0(tokens)
        if not e1 == None:
            return (e1, tokens)
    else:
        return None


def program(tokens):
    if not len(tokens) == 0:
        seqs = [ \
            ('Print', ['print', expressionTerm, ';', program]), \
            ('Print', ['print', expressionFormula, ';', program]), \
            ('Assign', ['assign', variable1, ':=', expressionTerm, ';', program]), \
            ('Assign', ['assign', variable1, ':=', expressionFormula, ';', program]), \
            ('If', ['if', expressionTerm, '{', program, '}', program]), \
            ('If', ['if', expressionFormula, '{', program, '}', program]), \
            ('While', ['while', expressionTerm, '{', program, '}', program]), \
            ('While', ['while', expressionFormula, '{', program, '}', program]) \
            ]

        if tokens[0] == '}':
            return ('End', tokens)

        return parse(seqs, tokens)
    else:
        return ('End', tokens)

    







  


