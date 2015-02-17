#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# interpret.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #2. ***************
#  ****************************************************************
#

exec(open("parse.py").read())

Node = dict
Leaf = str

def evaluate(env, e):
    if type(e) == Leaf:
        if e == 'True':
            return True
        if e == 'False':
            return False
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Number':
                n = children[0]
                return n
            if label == 'Plus':
                e1 = children[0]
                e2 = children[1]
                n1 = evaluate(env, e1)
                n2 = evaluate(env, e2)
                return n1 + n2
            if label == 'Array':
                x = children[0]['Variable'][0]
                if x in env:
                    arr = env[x]
                e = children[1]
                k = evaluate(env, e)
                return arr[k]
            if label == 'Variable':
                x = children[0]
                if x in env:
                    return env[x]
                else:
                    print(x + ' is unbound.')
                    exit()
def execute(env, s):
    if type(s) == Leaf:
        if s == 'End':
            return (env, [])
    if type(s) == Node:
        for label in s:
            children = s[label]
            if label == 'Assign':
                x = children[0]['Variable'][0]
                e0 = children[1]
                e1 = children[2]
                e2 = children[3]
                p1 = children[4]
                env1 = env
                n0 = evaluate(env1,e0)
                n1 = evaluate(env1,e1)
                n2 = evaluate(env1,e2)
                env1[x] = [n0,n1,n2]
                (env2, o1) = execute(env1, p1)
                return (env2, o1)
            if label == 'For':
                x = children[0]['Variable'][0]
                p1 = children[1]
                p2 = children[2]
                env[x] = 0
                env1 = env
                (env2, o1) = execute(env1, p1)
                env2[x] = 1
                (env3, o2) = execute(env2, p1)
                env3[x] = 2
                (env4, o3) = execute(env3, p1)
                (env5, o4) = execute(env4, p2)
                return (env5, o1+o2+o3+o4)
            if label == 'Print':
                e = children[0]
                p = children[1]
                v = evaluate(env, e)
                o = execute(env, p)[1]
                return (env, [v] + o)

def interpret(s):
    (env, o) = execute({}, tokenizeAndParse(s))
    return o

#print(tokenizeAndParse('print @a[1];'))
#eof
