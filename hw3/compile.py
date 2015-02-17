#########################################################
#
# CAS CS 320, Fall 2014
# Assignment 3
# compile.py
# Zhenjie Ruan
#
exec(open("interpret.py").read())
exec(open("parse.py").read())
exec(open("machine.py").read())

Node = dict
Leaf = str

'''
compileTerm
 takes three arguments:
 env is a mapping from variables to memory addresses,
 t is a term parse tree,
 heap is the memory address of the current top of the heap.
 The function should return a tuple (insts, addr, heap)
 in which insts is a sequence of machine language instructions
 (represented as a Python list of strings) that perform
 the computation represented by the parse tree,
 addr is the address of the result,
 and heap is an integer representing the memory of the top of the heap after the computation is performed.

 term	::=
number | variable | term + term

'''

def compileTerm(env, t, heap, fresh = 0):
    if type(t) == Node:
        for label in t:
            children = t[label]
            if label == 'Number':
                t = children[0]
                heap = heap + 1
                insts = 'set ' + str(heap) + ' ' + str(t)
                return ([insts], heap, heap, fresh)
            if label == 'Variable':
                t = children[0]
                addr = env[t] # the address that stored value for variable
                return ([], addr, heap, fresh)
            if label == 'Plus':
                t1 = children[0]
                t2 = children[1]
                (inst1, addr1, heap1, fresh1) = compileTerm(env, t1, heap, fresh)
                (inst2, addr2, heap2, fresh2) = compileTerm(env, t2, heap1, fresh1)
                insts = \
                    inst1 +\
                    inst2 +\
                    copy(addr1, '1')+\
                    copy(addr2, '2')+\
                    ['add']
                return (insts, 0, heap2, fresh2)




'''
formula	::=	true | false | variable | not formula | formula and formula | formula or formula
'''
def compileFormula(env, f, heap, fresh = 0):
    if type(f) == Leaf:
        if f == 'True':
            heap = heap + 1
            insts = 'set ' + str(heap) + ' 1'
            return([insts], heap, heap, fresh)
        if f == 'False':
            heap = heap + 1
            insts = 'set ' + str(heap) + ' 0'
            return([insts], heap, heap, fresh)
    if type(f) == Node:
        for label in f:
            children = f[label]
            if label == 'Variable':
                f = children[0]
                addr = env[f] # the address that stored value for variable
                return ([], addr, heap, fresh)
            if label == 'Not':
                f = children[0]
                (insts, addr, heap1, fresh) = compileFormula(env, f, heap)
                instsNot = \
                    ['branch setZero' + str(fresh) + ' ' + str(heap1),\
                     'set ' + str(heap1) + ' 1',\
                     'goto finish' + str(fresh),\
                     'label setZero' + str(fresh),\
                     'set ' + str(heap1) + ' 0',\
                     'label finish' + str(fresh)\
                     ]
                return (insts + instsNot, heap1, heap1, fresh + 1)
            if label == 'Or':
                [f1,f2] = children
                (insts1, addr1, heap1, fresh1) = compileFormula(env, f1, heap)
                (insts2, addr2, heap2, fresh2) = compileFormula(env, f2, heap1, fresh1)
                heap3 = heap2 + 1
                instsOr = \
                     copy(addr1, '1') + \
                     copy(addr2, '2') + \
                     ['add',\
                     'branch setOne' + str(fresh2) + ' 0',\
                     'goto finish' + str(fresh2),\
                     'label setOne' + str(fresh2),\
                     'set 0 1',\
                     'label finish' + str(fresh2)] +\
                     copy('0', str(heap3))
                return (insts1 + insts2 + instsOr, heap3, heap3, fresh2 + 1)
            if label == 'And':
                [f1,f2] = children
                (insts1, addr1, heap1, fresh1) = compileFormula(env, f1, heap)
                (insts2, addr2, heap2, fresh2) = compileFormula(env, f2, heap1, fresh1)
                heap3 = heap2 + 1
                instsAnd = \
                    ['set ' + str(heap3) + ' 0',\
                     'branch testFirst' + str(fresh2) + ' ' + str(addr1),\
                     'goto finish' + str(fresh2),\
                     'label testFirst' + str(fresh2),\
                     'branch setOne' + str(fresh2) + ' ' + str(addr2),\
                     'goto finish' + str(fresh2),\
                     'label setOne' + str(fresh2),\
                     'set ' + str(heap3) + ' 1',\
                     'label finish' + str(fresh2)\
                    ]
                return (insts1 + insts2 + instsAnd, heap3, heap3, fresh2 + 1)

def compileExpression(env, e, heap, fresh = 0):
    if not compileTerm(env, e, heap) == None:
        return compileTerm(env, e, heap)
    else:
        return compileFormula(env, e, heap, fresh)

'''
The function should return a tuple (env, insts, heap) in which env is an updated environment,
insts is a sequence of machine language instructions
(represented as a Python list of strings)
that perform the computation represented by the parse tree,
and heap is an integer representing the memory of the top of the heap after the computation is performed.
'''

def compileProgram(env, s, heap, fresh = 0):
    if type(s) == Leaf:
        if s == "End":
            return(env, [], heap, fresh)
    if type(s) == Node:
        for label in s:
            children = s[label]
            if label == "Print":
                p1 = children[0]
                p2 = children[1]
                (insts1, addr1, heap1, fresh1) = compileExpression(env, p1, heap)
                (env, insts2, heap2, fresh2) = compileProgram(env, p2, heap1, fresh1)
                instsOut = copy(addr1, '5')
                return(env, insts1 + instsOut + insts2, heap2, fresh2)
            if label == "Assign":
                t1 = children[0]["Variable"][0]
                e1 = children[1]
                p1 = children[2]
                (insts1, addr1, heap1, fresh1) = compileExpression(env, e1, heap)
                env[t1] = addr1
                (env1, insts2, heap2, fresh2) = compileProgram(env, p1, heap1, fresh1)
                return (env1, insts1 + insts2, heap2, fresh2)
            if label == "If":
                e1 = children[0]
                p1 = children[1]
                p2 = children[2]
                (insts1, addr1, heap1, fresh1) = compileExpression(env, e1, heap)
                (env1, insts2, heap2, fresh2) = compileProgram(env, p1, heap1, fresh1)
                (env2, insts3, heap3, fresh3) = compileProgram(env1, p2, heap2, fresh2)
                instsIf = \
                        insts1 + \
                        ['branch body' + str(fresh3) + ' ' + str(addr1),\
                         'goto rest' + str(fresh3),\
                         'label body' + str(fresh3) \
                        ] + \
                        insts2 + \
                        ['label rest' + str(fresh3)] + \
                        insts3
                return (env2, instsIf, heap3, fresh3)
            if label == "While":
                e1 = children[0]
                p1 = children[1]
                p2 = children[2]
                (insts1, addr1, heap1, fresh1) = compileExpression(env, e1, heap)
                (env1, insts2, heap2, fresh2) = compileProgram(env, p1, heap1, fresh1)
                (env2, insts3, heap3, fresh3) = compileProgram(env1, p2, heap2, fresh2)
                instsWhile = \
                            insts1 + \
                           ['goto check' + str(fresh3),\
                            'label body' + str(fresh3)\
                            ] + \
                            insts2 + \
                           ['label check' + str(fresh3),\
                            'branch body' + str(fresh3) + ' ' + str(addr1)
                            ] + \
                            insts3
                return (env2, instsWhile, heap3, fresh3)
            if label == "Procedure":
                t1 = children[0]["Variable"][0]
                p1 = children[1]
                p2 = children[2]
                (env1, insts1, heap1, fresh1) = compileProgram(env, p1, heap, fresh)
                (env2, insts2, heap2, fresh2) = compileProgram(env1, p2, heap1, fresh1)
                instsProcedure = procedure(t1, insts1)
                return (env2, instsProcedure + insts2, heap2, fresh2)
            if label == "Call":
                t1 = children[0]["Variable"][0]
                p1 = children[1]
                (env1, insts1, heap1, fresh1) = compileProgram(env, p1, heap, fresh)
                instsCall = call(t1)
                return(env1, instsCall + insts1, heap1, fresh1)



def compile(s):
    tokenized = tokenizeAndParse(s)
    return ['set 7 -1'] + compileProgram({}, tokenized, 7)[1]
                


