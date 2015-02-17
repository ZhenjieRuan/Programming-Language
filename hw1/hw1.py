#hw1
import re


#1.a

def tokenize(l,s):
    regularExpression = '(\s+'
    for i in l:
        for x in ['+','*','(',')']:
            if i == x:
                i = '\\' + x
        regularExpression += ('|' + i)
    regularExpression += ')'
    tokens = [t for t in re.split(regularExpression,s)]
    return [t for t in tokens if not t.isspace() and not t =='']


#1.b

def directions(tokens):
    if tokens[0] == 'stop' and tokens[1] == ';':
        return ('Stop',tokens[2:])
    if tokens[0] == 'forward'and tokens[1] == ';':
        (e1,tokens) = directions(tokens[2:])
        return({'Forward':[e1]},tokens)
    if tokens[0] == 'reverse'and tokens[1] == ';':
        (e1,tokens) = directions(tokens[2:])
        return({'Reverse':[e1]},tokens)
    if tokens[0] == 'left'and tokens[1] == 'turn' and tokens[2] == ';':
        (e1,tokens) = directions(tokens[3:])
        return({'LeftTurn':[e1]},tokens)
    if tokens[0] == 'right'and tokens[1] == 'turn' and tokens[2] == ';':
        (e1,tokens) = directions(tokens[3:])
        return({'RightTurn':[e1]},tokens)
        

def number(tokens):
    if re.match(r"^([1-9][0-9]*)$", tokens[0]):
        return ({"Number": [int(tokens[0])]}, tokens[1:])
def numberForTerm(tokens):
    if re.match(r"^([1-9][0-9]*)$", tokens[0]):
        return (int(tokens[0]), tokens[1:])

def variableForTerm(token):
    if not type(token[0]) == type(''):
        return None
    if token[0] == '':
        return None
    if re.match(r"^([a-zA-Z]+)$", token[0]):
        return (token[0],token[1:])
#2.a

def variable(tokens):
    if not type(tokens[0]) == type(''):
        return None
    if tokens[0] == '':
        return None
    if re.match(r"^([a-z][a-zA-Z]+)$", tokens[0]):
        return (tokens[0],tokens[1:])

#2.b
def term(token):
    return termHelper(token)

def termHelper(token, top = False):
    seqs = [\
         ('Plus', ['plus','(',term,',',term,')',]),\
         ('Mult', ['mult','(',term,',',term,')',]),\
         ('Log' , ['log','(',term,')']),\
         ('Variable',['@',variableForTerm]),\
         ('Number',['#',numberForTerm]),\
         ('Plus', ['(',term,'+',term,')']),\
         ('Mult', ['(',term,'*',term,')'])\
        ]

    for(label, seq) in seqs:
        tokens = token[0:]
        terminal = []
        nonterminal = []
        for t in seq:
            if type(t) == type(""):
                if tokens[0] == t:
                    tokens = tokens[1:]
                    terminal = terminal + [t]
                else: 
                    break
            else:
                returned = t(tokens)
                if not returned is None:
                    (e, tokens) = returned
                    nonterminal = nonterminal + [e]
        if len(terminal) + len(nonterminal) == len(seq):
            if not top or len(tokens) == 0:
                return ({label:nonterminal} if len(nonterminal) > 0 else label, tokens)


#2.c
def formula(token, top = False):
     seqs = [\
           ('True',['true']),\
           ('False',['false']),\
           ('Not',['not','(',formula,')']),\
           ('And',['and','(',formula,',',formula,')']),\
           ('Or',['or','(',formula,',',formula,')']),\
           ('Equal',['equal','(',term,',',term,')']),\
           ('LessThan',['less','than','(',term,',',term,')']),\
           ('GreaterThan',['greater','than','(',term,',',term,')']),\
           ('And',['(',formula,'&&',formula,')']),\
           ('Or',['(',formula,'||',formula,')']),\
           ('Equal',['(',term,'=','=',term,')']),\
           ('LessThan',['(',term,'<',term,')']),\
           ('GreaterThan',['(',term,'>',term,')'])\
          ]

     for(label, seq) in seqs:
        tokens = token[0:]  #make a copy of the tokens
        ss = []             #count the token consumed
        es = []             #list of the children
        for x in seq:
            if type(x) == type(''):
                if x == tokens[0]:
                    tokens = tokens[1:]  #the first token matches,cut it
                    ss = ss + [x]        # add the cutted token into consumed list
                else:
                    break
            else:
                r = x(tokens)
                if not r is None:
                    (e, tokens) = r
                    es  = es + [e]
        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                return ({label:es} if len(es) > 0 else label, tokens)


#2.d
def program(tokens, top = False):
    if tokens[0] == 'end' and tokens[1] == ';':
        tokens = tokens[2:]
        if not top or len(tokens) == 0:
            return('End',tokens)

    if tokens[0] == 'print':
        r = term(tokens[1:])
        if not r is None:
            (e1,tokens) = r
            if tokens[0] == ';':
                r = program(tokens[1:])
                if not r is None:
                    (e2,tokens) = r
                    if not top or len(tokens) == 0:
                        return ({'Print':[e1,e2]},tokens)
        else:
            r = formula(tokens[1:])
            if not r is None:
                (e3,tokens) = r
                if tokens[0] == ';':
                    r = program(tokens[1:])
                    if not r is None:
                        (e4,tokens) = r
                        if not top or len(tokens) == 0:
                            return ({'Print':[e3,e4]},tokens)
    if tokens[0] == 'assign':
        if tokens[1] == '@':
            r = variable(tokens[2:])
            if not r is None:
                (e5,tokens) = r
                if tokens[0] == ':' and tokens[1] == '=':
                    r = term(tokens[2:])
                    if not r is None:
                        (e6,tokens) = r
                        if tokens[0] == ';':
                            r = program(tokens[1:])
                            if not r is None:
                                (e7,tokens) = r
                                if not top or len(tokens) == 0:
                                    return ({'Assign': [e5,e6,e7]},tokens)


#2.e
def complete(string, top = False):
    seqs = ['print','assign','end','true','false','not','and','or','equal','less','than','greater','plus','mult','log','@','#',',',';','(',')',':','=','|','&','<','>','+','*']
    tokens = tokenize(seqs,string)
    r = term(tokens)
    if not r is None:
        (e1, tokens) = r
        if not top or len(tokens) == 0:
            return e1
    else:
        r = formula(tokens)
        if not r is None:
            (e2, tokens) = r
            if not top or len(tokens) == 0:
                return e2
        else:
            r = program(tokens)
            if not r is None:
                (e3, tokens) = r
                if not top or len(tokens) == 0:
                    return e3






