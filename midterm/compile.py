#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# compile.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #3. ***************
#  ****************************************************************
#

from random import randint
exec(open('parse.py').read())
exec(open('interpret.py').read())
exec(open('optimize.py').read())
exec(open('machine.py').read())
exec(open('analyze.py').read())

Leaf = str
Node = dict

def freshStr():
    return str(randint(0,10000000))

def compileExpression(env, e, heap):
    if type(e) == Leaf:
        if e == 'True':
            heap = heap + 1
            inst = ['set ' + str(heap) + ' 1']
            return (inst, heap, heap)
        if e == 'False':
            heap = heap + 1
            inst = ['set ' + str(heap) + ' 0']
            return (inst, heap, heap)
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Variable':
                f = children[0]
                addr = env[f]
                return ([], addr, heap)
            if label == 'Number':
                n = children[0]
                heap = heap + 1
                return (['set ' + str(heap) + ' ' + str(n)], heap, heap)

    # Complete 'True', 'False', 'Array', and 'Plus' cases for Problem #3.
            if label == 'Array':
                variable = children[0]['Variable'][0]
                addrV = env[variable]
                e = children[1]
                (insts1, addr1, heap1) = compileExpression(env, e, heap)
                heap2 = heap1 + 1
                insts = insts1 + \
                        copy(addr1, 1) + \
                        ['set 2' + ' ' + str(addrV),\
                         'add'\
                         ] + copyFromRef(0, heap2)
                return (insts, heap2, heap2)
            if label == 'Plus':
                t1 = children[0]
                t2 = children[1]
                (inst1, addr1, heap1) = compileExpression(env, t1, heap)
                (inst2, addr2, heap2) = compileExpression(env, t2, heap1)
                insts = \
                    inst1 +\
                    inst2 +\
                    copy(addr1, '1')+\
                    copy(addr2, '2')+\
                    ['add']
                return (insts, 0, heap2)


def compileProgram(env, s, heap = 6): # Set initial heap default address.
    if type(s) == Leaf:
        if s == 'End':
            return (env, [], heap)

    if type(s) == Node:
        for label in s:
            children = s[label]
            if label == 'Print':
                [e, p] = children
                (instsE, addr, heap) = compileExpression(env, e, heap)
                (env, instsP, heap) = compileProgram(env, p, heap)
                return (env, instsE + copy(addr, 5) + instsP, heap)

    # Complete 'Assign' case for Problem #3.
            if label == 'Assign':
                x = children[0]['Variable'][0]
                (insts1, addr1, heap1) = compileExpression(env, children[1], heap)
                (insts2, addr2, heap2) = compileExpression(env, children[2], heap1)
                (insts3, addr3, heap3) = compileExpression(env, children[3], heap2)
                p1 = children[4]
                insts = insts1 + copy(addr1, heap3 + 1) + insts2 + copy(addr2, heap3 + 2) + insts3 + copy(addr3, heap3 + 3)
                env[x] = heap3 + 1
                (env1, instsP, heap4) = compileProgram(env, p1, heap3 + 3)
                return (env1, insts + instsP, heap4)


def compile(s):
    p = tokenizeAndParse(s)

    if not typeProgram({}, p) == None:
        p = foldConstants(p)
        p = unrollLoops(p)


        (env, insts, heap) = compileProgram({}, p)
        return insts

def compileAndSimulate(s):
    return simulate(compile(s))


#print(compile('assign b := [2+5,3,4];assign c := [@b[0] + @b[0],3,7];for i {print @c[i];}'))
#print(compileAndSimulate('assign b := [2+5,3,4];assign c := [@b[0] + @b[0],5,7];for i {print @c[i];}'))
#eof
