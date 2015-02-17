#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# analyze.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #4. ***************
#  ****************************************************************
#

exec(open("parse.py").read())

Node = dict
Leaf = str

def typeExpression(env, e):
    if type(e) == Leaf:
        if e == 'True' or e == 'False':
            return 'Boolean'
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Number':
                return 'Number'

            if label == 'Variable':
                x = children[0]
                if x in env:
                    if not env[x] == 'Number':
                        return None
                    return 'Number'
                else:
                    #print('Something is wrong with variable')
                    return None



            elif label == 'Array':
                [x, e] = children
                x = x['Variable'][0]
                if x in env and env[x] == 'Array' and typeExpression(env, e) == 'Number':
                    return 'Number'

            elif label == 'Plus':
                [e1,e2] = children
                tyE1 = typeExpression(env, e1)
                tyE2 = typeExpression(env, e2)
                if tyE1 != 'Number' or tyE2 != 'Number':
                    #print('something is wrong with plus')
                    return None
                return 'Number'

def typeProgram(env, s):
    if type(s) == Leaf:
        if s == 'End':
            return 'Void'
    elif type(s) == Node:
        for label in s:
            if label == 'Print':
                [e, p] = s[label]
                #print(env)
                #print(e)
                #print(p)
                te = typeExpression(env, e)
                #print(te)
                tp = typeProgram(env, p)
                #print(tp)
                if te == 'Number' or te == 'Boolean':
                    if tp == 'Void':
                        return 'Void'
                #print('something is wrong with print')
                return None

            if label == 'Assign':
                [x, e0, e1, e2, p] = s[label]
                x = x['Variable'][0]
                if typeExpression(env, e0) == 'Number' and\
                   typeExpression(env, e1) == 'Number' and\
                   typeExpression(env, e2) == 'Number':
                     env[x] = 'Array'
                     if typeProgram(env, p) == 'Void':
                           return 'Void'

            if label == 'For':
                [x, p1, p2] = s[label]
                x = x['Variable'][0]
                env[x] = 'Number'
                #print(env)
                #print(p1)
                #print(p2)
                tp1 = typeProgram(env, p1)
                #print(tp1)
                tp2 = typeProgram(env, p2)
                if tp1 == 'Void' and tp2 == 'Void':
                    return 'Void'
                #print('something is wrong with for loop')
                return None

#eof