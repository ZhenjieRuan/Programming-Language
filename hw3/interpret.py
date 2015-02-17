######################################################################
#
# CAS CS 320, Fall 2014
# Assignment 3 (skeleton code)
# interpret.py
# Zhenjie Ruan
#


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







'''
term	::=	number | variable | term + term
formula	::=	true | false | variable | not formula | formula and formula | formula or formula
expression	::=	term | formula
program	::=print expression ; program
|variable := expression ; program
|if expression { program } program
|while expression { program } program
|procedure variable { program } program
|call variable ; program
|
'''

'''
[Term-Variable]
 Σ(x) = t           Σ, t ⇓ v
 Σ, x ⇓ v
[Formula-Variable]
 Σ(x) = f           Σ, f ⇓ v
 Σ, x ⇓ v
[Formula-Or-Short]
 Σ, f1 ⇓ true
 Σ, f1 or f2 ⇓ true
[Formula-Or]
 Σ, f1 ⇓ v1           Σ, f2 ⇓ v2
 Σ, f1 or f2 ⇓ v1 ∨ v2
[Formula-And-Short]
 Σ, f1 ⇓ false
 Σ, f1 and f2 ⇓ false
[Formula-And]
 Σ, f1 ⇓ v1           Σ, f2 ⇓ v2
 Σ, f1 and f2 ⇓ v1 ∧ v2
[Statement-Assign]
 Σ1 ⊎ {x ↦ e}, p ⇓ Σ2, o
 Σ1, assign x := e ; p ⇓ Σ2, o
[Statement-Procedure]
 Σ1 ⊎ {x ↦ p1}, p2 ⇓ Σ2, o
 Σ1, procedure x { p1 } p2 ⇓ Σ2, o
[Statement-Call]
 Σ1(x) = p1           Σ1, p1 ⇓ Σ2, o1           Σ2, p2 ⇓ Σ3, o2
 Σ1, call x ; p2 ⇓ Σ3, o1;o2

'''
exec(open("parse.py").read())

Node = dict
Leaf = str

def evalTerm(env, e):
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Number':
                x = children[0]
                return x
            elif label == 'Variable':
                x = children[0]
                if x in env:
<<<<<<< HEAD
                    return evalTerm(env, env[x])
                else:
                    print(x + 'is  unbound.')
=======
                    return
                else:
                    print(x + 'is unbound')
>>>>>>> a2e13d13cc1bd31a53e1a2d2d2dea428894ee85b
                    exit()
            elif label == 'Plus':
                f1 = children[0]
                v1 = evalTerm(env, f1)
                f2 = children[1]
                v2 = evalTerm(env, f2)
                return v1 + v2



def evalFormula(env, e):
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Not':
                c = children[0]
                v = evalFormula(env,c)
                return vnot(v)
            elif label == 'Variable':
                x = children[0]
                if x in env:
<<<<<<< HEAD
                    return evalFormula(env, env[x])
=======
                    return
>>>>>>> a2e13d13cc1bd31a53e1a2d2d2dea428894ee85b
                else:
                    print(x + 'is  unbound.')
                    exit()
            elif label == 'And':
                c1 = children[0]
                v1 = evalFormula(env,c1)
                if not v1:
                    return False
                else:
                    c2 = children[1]
                    v2 = evalFormula(env,c2)
                    return vand(v1,v2)
            elif label == 'Or':
                c1 = children[0]
                v1 = evalFormula(env,c1)
                if v1:
                    return True
                else:
                    c2 = children[1]
                    v2 = evalFormula(env,c2)
                    return vor(v1,v2)
    elif type(e) == Leaf:
        if e == 'True':
            return True
        if e == 'False':
            return False


def evalExpression(env, e): # Useful helper function.
    if not evalTerm(env,e) == None:
        return evalTerm(env,e)
    else:
        return evalFormula(env,e)

def execProgram(env, s):
    if type(s) == Leaf:
        if s == 'End':
            return (env,[])
    elif type(s) == Node:
        for label in s:
            if label == 'Print':
                children = s[label]
                f = children[0]
                p = children[1]
                v = evalExpression(env,f)
                (env, o) = execProgram(env, p)
                return(env, [v] + o)
            elif label == 'Assign':
                children = s[label]
                x = children[0]['Variable'][0]
                f = children[1]
                p = children[2]
                env[x] = f
                (env, o) = execProgram(env, p)
                return (env, o)
            elif label == 'Procedure':
                children = s[label]
<<<<<<< HEAD
                x = children[0]['Variable'][0]
                p1 = children[1]
                p2 = children[2]
                env[x] = p1
                (env2, o) = execProgram(env, p2)
=======
                env1 = env
                x = children[0]
                p1 = children[1]
                p2 = children[2]
                env1[x] = p1
                (env2, o) = execProgram(env1, p2)
>>>>>>> a2e13d13cc1bd31a53e1a2d2d2dea428894ee85b
                return (env2, o)
            elif label == 'Call':
                children = s[label]
                env1 = env
<<<<<<< HEAD
                x = children[0]['Variable'][0]
=======
                x = children[0]
>>>>>>> a2e13d13cc1bd31a53e1a2d2d2dea428894ee85b
                p1 = env1[x]
                p2 = children[1]
                (env2, o1) = execProgram(env1, p1)
                (env3, o2) = execProgram(env2, p2)
                return (env3, o1 + o2)
            elif label == 'If':
                children = s[label]
                e = children[0]
                p1 = children[1]
                p2 = children[2]
                env1 = env
                if evalExpression(env1, e):
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
                if evalExpression(env1, e):
                    (env2, o1) = execProgram(env1, p1)
                    (env3, o2) = execProgram(env2, loop)
                    return (env3, o1 + o2)
                else:
                    (env2, o1) = execProgram(env1, p2)
                    return (env2, o1)

def interpret(s):
    (env, o) = execProgram({}, tokenizeAndParse(s))
    return o

#eof
