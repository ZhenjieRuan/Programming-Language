from math import log,floor
import re
exec(open('parse.py').read())

def tokenize(l,s):
    regularExpression = '(\s+'
    l = (re.escape(x) for x in l)
    for i in l:
        regularExpression += '|'
        '''
        if i == '+' or i == '*' or i == '(' or i == ')' or i == '|':
            regularExpression += '\\'
        '''
        regularExpression += i
    regularExpression += ')'
    tokens = [t for t in re.split(regularExpression,s)]
    return [t for t in tokens if not t.isspace() and not t =='']

def vnot(v):
    if v == True:  return False
    if v == False: return True

def vand(v1, v2):
    if v1 == True  and v2 == True:  return True
    if v1 == True  and v2 == False: return False
    if v1 == False and v2 == True:  return False
    if v1 == False and v2 == False: return False

def vor(v1, v2):
    if v1 == True  and v2 == True:  return True
    if v1 == True  and v2 == False: return True
    if v1 == False and v2 == True:  return True
    if v1 == False and v2 == False: return False

def vxor(v1,v2):
    if v1 == True  and v2 == True:  return False
    if v1 == True  and v2 == False: return True
    if v1 == False and v2 == True:  return True
    if v1 == False and v2 == False: return False




Node = dict
Leaf = str
'''
[Term-Number]

 Σ, n ⇓ n
[Term-Variable]
 Σ(x) = v
 Σ, x ⇓ v
[Term-Parens]
 Σ, t ⇓ v
 Σ, ( t ) ⇓ v
[Term-Log]
 Σ, t ⇓ v
 Σ, log ( t ) ⇓ ⌊ log2 (v) ⌋
[Term-Plus]
 Σ, t1 ⇓ v1           Σ, t2 ⇓ v2
 Σ, t1 + t2 ⇓ v1 + v2
[Term-Mult]
 Σ, t1 ⇓ v1           Σ, t2 ⇓ v2
 Σ, t1 * t2 ⇓ v1 ⋅ v2
'''
def evalTerm(env, t):
    if type(t) == Node:
        for label in t:
            children = t[label]
            if label == 'Log':
                f = children[0]
                v = evalTerm(env, f)
                return floor(log(v, 2))
            elif label == 'Parens':
                f = children[0]
                v = evalTerm(env, f)
                return v
            elif label == 'Plus':
                f1 = children[0]
                v1 = evalTerm(env, f1)
                f2 = children[1]
                v2 = evalTerm(env, f2)
                return v1 + v2
            elif label == 'Mult':
                f1 = children[0]
                v1 = evalTerm(env, f1)
                f2 = children[1]
                v2 = evalTerm(env, f2)
                return v1*v2
            elif label == 'Number':
                x = children[0]
                return x
            elif label == 'Variable':
                x = children[0]
                if x in env:
                    return env[x]
                else:
                    print(x + 'is  unbound.')
                    exit()
'''
[Formula-True]

 Σ, true ⇓ true
[Formula-False]

 Σ, false ⇓ false
[Formula-Variable]
 Σ(x) = v
 Σ, x ⇓ v
[Formula-Parens]
 Σ, f ⇓ v
 Σ, ( f ) ⇓ v
[Formula-Not]
 Σ, f ⇓ v
 Σ, not f ⇓ ¬ v
[Formula-Xor]
 Σ, f1 ⇓ v1           Σ, f2 ⇓ v2
 Σ, f1 xor f2 ⇓ v1 ⊕ v2
'''


def evalFormula(env,f):
    if type(f) == Node:
        for label in f:
            children = f[label]
            if label == 'Parens':
                c = children[0]
                v = evalFormula(env, c)
                return v
            elif label == 'Not':
                c = children[0]
                v = evalFormula(env,c)
                return vnot(v)
            elif label == 'Xor':
                c1 = children[0]
                v1 = evalFormula(env,c1)
                c2 = children[1]
                v2 = evalFormula(env,c2)
                return vxor(v1,v2)
            elif label == 'Variable':
                x = children[0]
                if x in env:
                    return env[x]
                else:
                    print(x + 'is  unbound.')
                    exit()
    elif type(f) == Leaf:
        if f == 'True':
            return True
        if f == 'False':
            return False


'''
execProgram
[Statement-Print]
 Σ1, p ⇓ Σ2, o           Σ1, e ⇓ v
 Σ1, print e ; p ⇓ Σ2, v;o
[Statement-Assign]
 Σ1 ⊎ {x ↦ v}, p ⇓ Σ2, o           Σ1, e ⇓ v
 Σ1, assign x := e ; p ⇓ Σ2, o
[Statement-If-False]
 Σ1, p2 ⇓ Σ2, o1           Σ1, e ⇓ false
 Σ1, if e { p1 } p2 ⇓ Σ2, o1
[Statement-If-True]
 Σ1, p1 ⇓ Σ2, o1           Σ2, p2 ⇓ Σ3, o2           Σ1, e ⇓ true
 Σ1, if e { p1 } p2 ⇓ Σ3, o1;o2
[Statement-While-False]
 Σ1, p2 ⇓ Σ2, o1           Σ1, e ⇓ false
 Σ1, while e { p1 } p2 ⇓ Σ2, o1
[Statement-While-True]
  Σ1, p1 ⇓ Σ2, o1           Σ2, while e { p1 } p2 ⇓ Σ3, o2           Σ1, e ⇓ true
 Σ1, while e { p1 } p2 ⇓ Σ3, o1;o2
[Statement-End]

 Σ, end ; ⇓ Σ, o0
'''



def execProgram(env,s):
    if type(s) == Leaf:
        if s == 'End':
            return (env,[])
    elif type(s) == Node:
        for label in s:
            if label == 'Print':
                children = s[label]
                f = children[0]
                p = children[1]
                v = evaluate(env,f)
                (env, o) = execProgram(env, p)
                return(env, [v] + o)
            elif label == 'Assign':
                children = s[label]
                x = children[0]['Variable'][0]
                f = children[1]
                p = children[2]
                v = evaluate(env, f)
                env[x] = v
                (env, o) = execProgram(env, p)
                return (env, o)
            elif label == 'If':
                children = s[label]
                e = children[0]
                p1 = children[1]
                p2 = children[2]
                env1 = env
                if evaluate(env1, e):
                    (env2, o1) = execProgram(env1, p1)
                    (env3, o2) = execProgram(env2, p2)
                    return (env3, o1 + o2)
                else:
                    (env2, o1) = execProgram(env1, p2)
                    return (env2, o1)
            elif label == 'While':
                children = s[label]
                e = children[0]
                loop = {'While': children}
                p1 = children[1]
                p2 = children[2]
                env1 = env
                if evaluate(env1, e):
                    (env2, o1) = execProgram(env1, p1)
                    (env3, o2) = execProgram(env2, loop)
                    return (env3, o1 + o2)
                else:
                    (env2, o1) = execProgram(env1, p2)
                    return (env2, o1)


def evaluate(env,p):
    if not evalTerm(env,p) == None:
        return evalTerm(env,p)
    else:
        return evalFormula(env,p)


def interpret(string):
    seqs = ['print','assign','end','true','false','not','and','xor','equal','less','than','greater','plus','mult','log','@','#',',','|',';','(',')',':=','&','<','>',"+","*"]
    tokens = tokenize(seqs, string)
    parsed = program(tokens)
    return execProgram({},parsed[0])[1]






