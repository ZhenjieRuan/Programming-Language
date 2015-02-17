
import re

############################################################
# Load the file. Change the path if necessary.
exec(open('hw1-submitted.py').read())

def check(function, inputs_result_pairs):
    passed = 0
    for (inputs, result) in inputs_result_pairs:
        output = function(inputs[0], inputs[1]) if len(inputs) == 2 else function(inputs[0])

        # If the result includes the token list, take only the parse tree.
        output = output[0] if type(output) == tuple else output

        if output == result: passed = passed + 1
        else: print("\n    Failed on:\n    "+str(inputs)+"\n\n"+"    Should be:\n    "+str(result)+"\n\n"+"    Returned:\n    "+str(output)+"\n")
    print("Passed " + str(passed) + " of " + str(len(inputs_result_pairs)) + " tests.")
    print("")

############################################################
# The tests.

print("Problem #1, part (a)...")
try: tokenize
except: print("The tokenize() function is not defined.")
else:
    check(tokenize, [\
        ([['token'], "token token   token token   "], ['token', 'token', 'token', 'token']),\
        ([['example','test'], "example test example example"], ['example', 'test', 'example', 'example']),\
        ([['a','b','c','d','e',','], "a,b,c,d,e,d,c,b,a"], ['a', ',', 'b', ',', 'c', ',', 'd', ',', 'e', ',', 'd', ',', 'c', ',', 'b', ',', 'a']),\
        ([['up','down','left','right','stop',';'], "left; right; stop;"], ['left', ';', 'right', ';', 'stop', ';']),\
        ([['+','*','(',')','f','x','y','z'], "f(x+y)*z"], ['f','(','x','+','y',')','*','z'])\
        ])

print("\n\nProblem #1, part (b)...")
try: (tokenize, directions)
except: print("The tokenize() and/or directions() functions are not defined.")
else:
    check((lambda s: directions(tokenize(["forward","reverse","left","right","turn","stop",";"], s))), [\
        (["stop ;"], 'Stop'),\
        (["forward ; reverse ; forward ; stop ;"], {'Forward': [{'Reverse': [{'Forward': ['Stop']}]}]}),\
        (["stop;"], 'Stop'),\
        (["forward; reverse; forward; stop;"], {'Forward': [{'Reverse': [{'Forward': ['Stop']}]}]}),\
        (["reverse; forward; left turn; right turn; stop;"], {'Reverse': [{'Forward': [{'LeftTurn': [{'RightTurn': ['Stop']}]}]}]}),\
        (["right turn; reverse; left turn; right turn; reverse; forward; left turn; right turn; reverse; left turn; right turn; reverse; forward; left turn; stop;"], {'RightTurn': [{'Reverse': [{'LeftTurn': [{'RightTurn': [{'Reverse': [{'Forward': [{'LeftTurn': [{'RightTurn': [{'Reverse': [{'LeftTurn': [{'RightTurn': [{'Reverse': [{'Forward': [{'LeftTurn': ['Stop']}]}]}]}]}]}]}]}]}]}]}]}]}]}),\
        ])

print("\n\nProblem #2...")
try: complete
except: print("The complete() function is not defined.")
else: check(complete, [\
    (["end ;"], 'End'),\
    (["print true ; end ;"], {'Print': ['True', 'End']}),\
    (["print true ; print # 123 ; end ;"], {'Print': ['True', {'Print': [{'Number': [123]}, 'End']}]}),\
    (["assign @ x := # 1 ; end ;"], {'Assign': [{'Variable': ['x']}, {'Number': [1]}, 'End']}),\
    (["end;"], 'End'),\
    (["print true; end;"], {'Print': ['True', 'End']}),\
    (["assign @x:=#1;end;"], {'Assign': [{'Variable': ['x']}, {'Number': [1]}, 'End']}),\
    (["print true; print #123; end;"], {'Print': ['True', {'Print': [{'Number': [123]}, 'End']}]}),\
    (["print true; print #123; assign @x := #123; end;"], {'Print': ['True', {'Print': [{'Number': [123]}, {'Assign': [{'Variable': ['x']}, {'Number': [123]}, 'End']}]}]}),\
    (["print not(true); print plus(log(#4),#99); assign @x := #123; end;"], {'Print': [{'Not': ['True']}, {'Print': [{'Plus': [{'Log': [{'Number': [4]}]}, {'Number': [99]}]}, {'Assign': [{'Variable': ['x']}, {'Number': [123]}, 'End']}]}]}),\
    (["print not(true); assign @y := #10; print plus(log(#4),@y); assign @x := #123; print equal(@x,@y); end;"], {'Print': [{'Not': ['True']}, {'Assign': [{'Variable': ['y']}, {'Number': [10]}, {'Print': [{'Plus': [{'Log': [{'Number': [4]}]}, {'Variable': ['y']}]}, {'Assign': [{'Variable': ['x']}, {'Number': [123]}, {'Print': [{'Equal': [{'Variable': ['x']}, {'Variable': ['y']}]}, 'End']}]}]}]}]}),\
    (["assign @y := #100; assign @x := plus(mult(log(@y),#20),#30); print and(less than(@x, @y), or(equal(@y, #200), false)); end;"], {'Assign': [{'Variable': ['y']}, {'Number': [100]}, {'Assign': [{'Variable': ['x']}, {'Plus': [{'Mult': [{'Log': [{'Variable': ['y']}]}, {'Number': [20]}]}, {'Number': [30]}]}, {'Print': [{'And': [{'LessThan': [{'Variable': ['x']}, {'Variable': ['y']}]}, {'Or': [{'Equal': [{'Variable': ['y']}, {'Number': [200]}]}, 'False']}]}, 'End']}]}]}),\
    (["assign @a := #1; assign @b := log(plus(mult(log(@a),#2),#3)); print not(greater than(log(plus(mult(log(@a),#2),#3)),log(plus(mult(log(@a),#2),#3)))); print and(or(true,false), not(true)); end;"], {'Assign': [{'Variable': ['a']}, {'Number': [1]}, {'Assign': [{'Variable': ['b']}, {'Log': [{'Plus': [{'Mult': [{'Log': [{'Variable': ['a']}]}, {'Number': [2]}]}, {'Number': [3]}]}]}, {'Print': [{'Not': [{'GreaterThan': [{'Log': [{'Plus': [{'Mult': [{'Log': [{'Variable': ['a']}]}, {'Number': [2]}]}, {'Number': [3]}]}]}, {'Log': [{'Plus': [{'Mult': [{'Log': [{'Variable': ['a']}]}, {'Number': [2]}]}, {'Number': [3]}]}]}]}]}, {'Print': [{'And': [{'Or': ['True', 'False']}, {'Not': ['True']}]}, 'End']}]}]}]}),\
    ])

print("\n\nProblem #3...")
try: complete
except: print("The complete() function is not defined.")
else: check(complete, [\
    (["print ( # 2 + @ x ) ; end ;"], {'Print': [{'Plus': [{'Number': [2]}, {'Variable': ['x']}]}, 'End']}),\
    (["print (#2 * @x) ; end ;"], {'Print': [{'Mult': [{'Number': [2]}, {'Variable': ['x']}]}, 'End']}),\
    (["print (#2 == @x) ; end ;"], {'Print': [{'Equal': [{'Number': [2]}, {'Variable': ['x']}]}, 'End']}),\
    (["print (#2 < @x) ; end ;"], {'Print': [{'LessThan': [{'Number': [2]}, {'Variable': ['x']}]}, 'End']}),\
    (["print (#2 > @x) ; end ;"], {'Print': [{'GreaterThan': [{'Number': [2]}, {'Variable': ['x']}]}, 'End']}),\
    (["print (true && false) ; end ;"], {'Print': [{'And': ['True', 'False']}, 'End']}),\
    (["print (true || not(false)) ; end ;"], {'Print': [{'Or': ['True', {'Not': ['False']}]}, 'End']}),\
    (["print not(true); assign @y := #10; print (log(#4) + @y); assign @x := #123; print (@x == @y); end;"], {'Print': [{'Not': ['True']}, {'Assign': [{'Variable': ['y']}, {'Number': [10]}, {'Print': [{'Plus': [{'Log': [{'Number': [4]}]}, {'Variable': ['y']}]}, {'Assign': [{'Variable': ['x']}, {'Number': [123]}, {'Print': [{'Equal': [{'Variable': ['x']}, {'Variable': ['y']}]}, 'End']}]}]}]}]}),\
    (["assign @y := #100; assign @x := plus(mult(log(@y),#20),#30); print and((@x < @y), or((@y  == #200), false)); end;"], {'Assign': [{'Variable': ['y']}, {'Number': [100]}, {'Assign': [{'Variable': ['x']}, {'Plus': [{'Mult': [{'Log': [{'Variable': ['y']}]}, {'Number': [20]}]}, {'Number': [30]}]}, {'Print': [{'And': [{'LessThan': [{'Variable': ['x']}, {'Variable': ['y']}]}, {'Or': [{'Equal': [{'Variable': ['y']}, {'Number': [200]}]}, 'False']}]}, 'End']}]}]}),\
    (["assign @a := #1; assign @b := log(((log(@a)*#2)+#3)); print not((log(((log(@a) * #2) + #3))>log(plus(mult(log(@a),#2),#3)))); print and(or(true,false), not(true)); end;"], {'Assign': [{'Variable': ['a']}, {'Number': [1]}, {'Assign': [{'Variable': ['b']}, {'Log': [{'Plus': [{'Mult': [{'Log': [{'Variable': ['a']}]}, {'Number': [2]}]}, {'Number': [3]}]}]}, {'Print': [{'Not': [{'GreaterThan': [{'Log': [{'Plus': [{'Mult': [{'Log': [{'Variable': ['a']}]}, {'Number': [2]}]}, {'Number': [3]}]}]}, {'Log': [{'Plus': [{'Mult': [{'Log': [{'Variable': ['a']}]}, {'Number': [2]}]}, {'Number': [3]}]}]}]}]}, {'Print': [{'And': [{'Or': ['True', 'False']}, {'Not': ['True']}]}, 'End']}]}]}]}),\
    ])

#eof