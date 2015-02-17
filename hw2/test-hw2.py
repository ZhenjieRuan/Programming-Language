import re

############################################################
# Load the files. Change the path if necessary.
exec(open('parse.py').read())
exec(open('interpret.py').read())

def check(name, function, inputs_result_pairs):
    passed = 0
    for (inputs, result) in inputs_result_pairs:
        try:
            output = function(inputs[0], inputs[1]) if len(inputs) == 2 else function(inputs[0])
        except:
            output = None

        if output == result: passed = passed + 1
        else: print("\n  Failed on:\n    "+name+"("+', '.join([str(i) for i in inputs])+")\n\n"+"  Should be:\n    "+str(result)+"\n\n"+"  Returned:\n    "+str(output)+"\n")
    print("Passed " + str(passed) + " of " + str(len(inputs_result_pairs)) + " tests.")
    print("")

############################################################
# The tests.

print("Problem #1, part (a), variable()...")
try: variable
except: print("The variable() function is not defined.")
else: check('variable', variable, [\
    ([["x"]], ('x', [])),\
    ([["test"]], ('test', [])),\
    ([["camelNotation123"]], ('camelNotation123', [])),\
    ([["123"]], None),\
    ([["123abc"]], None)\
    ])

print("Problem #1, part (a), number()...")
try: number
except: print("The number() function is not defined.")
else: check('number', number, [\
    ([["123"]], (123, [])),\
    ([["0"]], (0, [])),\
    ([["1010"]],(1010, [])),\
    ([["-456"]],(-456, [])),\
    ([["abc"]], None)\
    ])

print("Problem #1, part (b), formula()...")
try: formula
except: print("The formula() function is not defined.")
else: check('formula', formula, [\
    (["true".split(" ")], ('True', [])),\
    (["false".split(" ")], ('False', [])),\
    (["true xor false".split(" ")], ({'Xor': ['True', 'False']}, [])),\
    (["( true xor false )".split(" ")], ({'Parens': [{'Xor': ['True', 'False']}]}, [])),\
    (["not ( true ) xor false".split(" ")], ({'Xor': [{'Not': ['True']}, 'False']}, [])),\
    (["x".split(" ")], ({'Variable': ['x']}, [])),\
    (["x xor not ( y )".split(" ")], ({'Xor': [{'Variable': ['x']}, {'Not': [{'Variable': ['y']}]}]}, [])),\
    (["true xor false xor true xor false".split(" ")], ({'Xor': ['True', {'Xor': ['False', {'Xor': ['True', 'False']}]}]}, [])),\
    (["x xor y xor not ( z ) xor true".split(" ")], ({'Xor': [{'Variable': ['x']}, {'Xor': [{'Variable': ['y']}, {'Xor': [{'Not': [{'Variable': ['z']}]}, 'True']}]}]}, [])),\
    (["not ( a xor b ) xor true".split(" ")], ({'Xor': [{'Not': [{'Xor': [{'Variable': ['a']}, {'Variable': ['b']}]}]}, 'True']}, [])),\
    (["0 + 1".split(" ")], None),\
    (["( 0 + 1 )".split(" ")], None),\
    (["0 xor 1".split(" ")], None),\
    (["not 123".split(" "), True], None)\
    ])

print("Problem #1, part (c), term()...")
try: term
except: print("The term() function is not defined.")
else: check('term', term, [\
    (["123".split(" ")], ({'Number':[123]}, [])),\
    (["0".split(" ")], ({'Number':[0]}, [])),\
    (["x".split(" ")], ({'Variable': ['x']}, [])),\
    (["0 + 1".split(" ")], ({'Plus': [{'Number': [0]}, {'Number': [1]}]}, [])),\
    (["x + ( 1 + 2 )".split(" ")], ({'Plus': [{'Variable': ['x']}, {'Parens': [{'Plus': [{'Number': [1]}, {'Number': [2]}]}]}]}, [])),\
    (["( x + 1 ) + 2".split(" ")], ({'Plus': [{'Parens': [{'Plus': [{'Variable': ['x']}, {'Number': [1]}]}]}, {'Number': [2]}]}, [])),\
    (["1 + 2 * 3" .split(" ")], ({'Plus': [{'Number': [1]}, {'Mult': [{'Number': [2]}, {'Number': [3]}]}]}, [])),\
    (["( 1 + 2 ) * 3" .split(" ")], ({'Mult': [{'Parens': [{'Plus': [{'Number': [1]}, {'Number': [2]}]}]}, {'Number': [3]}]}, [])),\
    (["1 + 2 * 3 + 4".split(" ")], ({'Plus': [{'Number': [1]}, {'Plus': [{'Mult': [{'Number': [2]}, {'Number': [3]}]}, {'Number': [4]}]}]}, [])),\
    (["1 + 2 + log ( z ) + 0".split(" ")], ({'Plus': [{'Number': [1]}, {'Plus': [{'Number': [2]}, {'Plus': [{'Log': [{'Variable': ['z']}]}, {'Number': [0]}]}]}]}, [])),\
    (["log ( a * b ) * 2".split(" ")], ({'Mult': [{'Log': [{'Mult': [{'Variable': ['a']}, {'Variable': ['b']}]}]}, {'Number': [2]}]}, [])),\
    ])

print("Problem #1, part (d), program()...")
try: program
except: print("The program() function is not defined.")
else: check('program', program, [\
    (["print true ;".split(" ")], ({'Print': ['True', 'End']}, [])),\
    (["assign x := 3 + 4 ; print x * x ;".split(" ")], ({'Assign': [{'Variable': ['x']}, {'Plus': [{'Number': [3]}, {'Number': [4]}]}, {'Print': [{'Mult': [{'Variable': ['x']}, {'Variable': ['x']}]}, 'End']}]}, [])),\
    (["assign x := true xor false ; print false ;".split(" ")], ({'Assign': [{'Variable': ['x']}, {'Xor': ['True', 'False']}, {'Print': ['False', 'End']}]}, [])),\
    (["if true { print 1 ; } print 0 ;".split(" ")], ({'If': ['True', {'Print': [{'Number': [1]}, 'End']}, {'Print': [{'Number': [0]}, 'End']}]}, [])),\
    (["while true { if false { print 0 ; } print 1 ; } print 2 ;".split(" ")], ({'While': ['True', {'If': ['False', {'Print': [{'Number': [0]}, 'End']}, {'Print': [{'Number': [1]}, 'End']}]}, {'Print': [{'Number': [2]}, 'End']}]}, [])),\
    (["assign x := 1 + 2 ; while false { assign y := a xor b ; }".split(" ")], ({'Assign': [{'Variable': ['x']}, {'Plus': [{'Number': [1]}, {'Number': [2]}]}, {'While': ['False', {'Assign': [{'Variable': ['y']}, {'Xor': [{'Variable': ['a']}, {'Variable': ['b']}]}, 'End']}, 'End']}]}, [])),\
    ([[]], ('End', [])),\
    (["print 1 + 2 + log ( z ) + 0 ; assign y := 1 + 2 + log ( z ) + 0 ; print log ( 4 ) + y ;".split(" ")], ({'Print': [{'Plus': [{'Number': [1]}, {'Plus': [{'Number': [2]}, {'Plus': [{'Log': [{'Variable': ['z']}]}, {'Number': [0]}]}]}]}, {'Assign': [{'Variable': ['y']}, {'Plus': [{'Number': [1]}, {'Plus': [{'Number': [2]}, {'Plus': [{'Log': [{'Variable': ['z']}]}, {'Number': [0]}]}]}]}, {'Print': [{'Plus': [{'Log': [{'Number': [4]}]}, {'Variable': ['y']}]}, 'End']}]}]}, [])),\
    (["assign x := true ; while x { assign x := false ; } print x ;".split(" ")], ({'Assign': [{'Variable': ['x']}, 'True', {'While': [{'Variable': ['x']}, {'Assign': [{'Variable': ['x']}, 'False', 'End']}, {'Print': [{'Variable': ['x']}, 'End']}]}]}, [])),\
    (["prong true ;".split(" "), True], None),\
    (["print true ; false ;".split(" "), True], None),\
    (["123 ;".split(" "), True], None),\
    (["123 + 456".split(" "), True], None),\
    (["if { print true ; }".split(" "), True], None)\
    ])

print("Problem #2, part (a), evalTerm()...")
try: evalTerm
except: print("The evalTerm() function is not defined.")
else: check('evalTerm', evalTerm, [\
    ([{}, {'Number': [123]}], 123),\
    ([{'x':10}, {'Variable': ['x']}], 10),\
    ([{}, {'Plus': [{'Number': [1]}, {'Plus': [{'Mult': [{'Number': [2]}, {'Number': [3]}]}, {'Number': [4]}]}]}], 11),\
    ([{}, {'Plus': [{'Number': [0]}, {'Number': [1]}]}], 1),\
    ([{'x':2, 'y':3}, {'Plus': [{'Variable': ['y']}, {'Variable': ['x']}]}], 5),\
    ([{'z':32}, {'Log': [{'Variable': ['z']}]}], 5),\
    ([{'x':4}, {'Parens': [{'Plus': [{'Number': [1]}, {'Number': [2]}]}]}], 3),\
    ([{'x':4}, {'Plus': [{'Variable': ['x']}, {'Parens': [{'Plus': [{'Number': [1]}, {'Number': [2]}]}]}]}], 7)\
    ])

print("Problem #2, part (b), evalFormula()...")
try: evalFormula
except: print("The evalFormula() function is not defined.")
else: check('evalFormula', evalFormula, [\
    ([{}, 'True'], True),\
    ([{}, {'Xor': ['True', 'False']}], True),\
    ([{'x':True}, {'Variable':['x']}], True),\
    ([{'x':True, 'y':False}, {'Xor': [{'Not':[{'Variable': ['y']}]}, {'Variable': ['x']}]}], False),\
    ([{}, {'Parens': [{'Xor': ['True', 'False']}]}], True),\
    ([{'x':False}, {'Parens': [{'Xor': [{'Parens': [{'Xor': ['True', {'Variable': ['x']}]}]}, 'False']}]}], True)\
    ])

print("Problem #2, part (c), execProgram()...")
try: execProgram
except: print("The execProgram() function is not defined.")
else: check('execProgram', execProgram, [\
    ([{}, 'End'], ({}, [])),\
    ([{}, {'Print': ['False', 'End']}], ({}, [False])),\
    ([{'y':False}, {'Print': [{'Not':[{'Variable':['y']}]}, 'End']}], ({'y': False}, [True])),\
    ([{'x':123}, {'Assign': [{'Variable': ['x']}, 'True', {'Print': [{'Variable': ['x']}, 'End']}]}], ({'x': True}, [True])),\
    ([{}, {'Assign': [{'Variable': ['x']}, 'True', {'If': [{'Variable': ['x']}, {'While': [{'Not': [{'Variable': ['x']}]}, {'Print': [{'Number': [123]}, 'End']}, 'End']}, {'Print': [{'Variable': ['x']}, 'End']}]}]}], ({'x': True}, [True])),\
    ])

print("Problem #2, part (d), interpret()...")
try: interpret
except: print("The interpret() function is not defined.")
else: check('interpret', interpret, [\
    (["print true;"], [True]),\
    (["print 1 + 2 + 3;"], [6]),\
    (["assign x := 3+4 ; print x*x+1;"], [50]),\
    (["assign x := true; if x { print x; } print x;"], [True, True]),\
    (["assign x := true; while x { print x; assign x := false; } print x;"], [True, False]),\
    ([""], []),\
    (["assign x := true; if x { while not ( x ) { print 123; } } print x;"], [True]),\
    (["assign x := true; if x { while x xor false { print 123; assign x := x xor true; } } print x;"], [123, False]),\
    (["assign x := true; assign y := true; while x { while y { print x; assign y := x xor y; } assign x := x xor true; } print x; print y;"], [True, False, False]),\
    (["print true; false;".split(" ")], None),\
    (["123;".split(" ")], None),\
    (["123 + 456".split(" ")], None),\
    (["if { print true; }".split(" ")], None)\
    ])

#eof