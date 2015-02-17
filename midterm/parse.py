#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# parse.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #1. ***************
#  ****************************************************************
#

import re

def parse(seqs, tmp, top = True):
    for (label, seq) in seqs:
        tokens = tmp[0:]
        (ss, es) = ([], [])
        for x in seq:
            if type(x) == type(""):
                if tokens[0] == x:
                    tokens = tokens[1:]
                    ss = ss + [x]
                else: break
            else:
                r = x(tokens, False)
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]
        if len(ss) + len(es) == len(seq) and (not top or len(tokens) == 0):
            return ({label:es} if len(es) > 0 else label, tokens)

def number(tokens, top = True):
    if re.compile(r"(-(0|[1-9][0-9]*)|(0|[1-9][0-9]*))").match(tokens[0]):
        return ({"Number": [int(tokens[0])]}, tokens[1:])

def variable(tokens, top = True):
    if re.compile(r"[a-z][A-Za-z0-9]*").match(tokens[0]) and tokens[0] not in ['true', 'false']:
        return ({"Variable": [tokens[0]]}, tokens[1:])

def expression(tmp, top = True):
    tokens = tmp[0:]
    r = leftExpression(tokens, False)
    if not r is None:
        (e1, tokens) = r
        if len(tokens) > 0 and tokens[0] == '+':
            r = expression(tokens[1:], False)
            if not r is None:
                (e2, tokens) = r
                return ({'Plus':[e1,e2]}, tokens)
        else:
            return (e1, tokens)

def leftExpression(tmp, top = True):
    r = parse([\
        ('True', ['true']),\
        ('False', ['false']),\
        ('Array', ['@', variable, '[', expression, ']'])
        ], tmp, top)
    if not r is None:
        return r

    tokens = tmp[0:]
    r = variable(tokens, False)
    if not r is None:
        return r

    tokens = tmp[0:]
    r = number(tokens, False)
    if not r is None:
        return r


def program(tmp, top = True):
    if len(tmp) == 0:
        return ('End', [])
    r = parse([\
        ('Print', ['print', expression, ';', program]),\
        ('Assign',  ['assign', variable, ':=', '[', expression,',', expression,',', expression, ']', ';', program]),\
        ('For', ['for', variable, '{', program, '}', program]),\
        ('End', [])\
        ], tmp, top)
    if not r is None:
        return r

def tokenizeAndParse(s):
    tokens = re.split(r"(\s+|assign|:=|print|\+|;|true|false|for|\{|}|\[|]|@|,)", s)
    tokens = [t for t in tokens if not t.isspace() and not t == ""]
    (p, tokens) = program(tokens)
    return p



#eof
