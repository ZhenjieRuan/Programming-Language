############################################################
# Load the files. Change the path if necessary.
exec(open('parse.py').read())
exec(open('interpret.py').read())
exec(open('compile.py').read())
 
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
 
print("Problem #1")
try: tokenizeAndParse
except: print("The tokenizeAndParse() function is not defined.")
else: check('tokenizeAndParse', tokenizeAndParse, [\
    (["print true ;"], ({'Print': ['True', 'End']})),\
    (["print 4;"], ({'Print': [{'Number': [4]}, 'End']})),\
    (["print -1;"], ({'Print': [{'Number': [-1]}, 'End']})),\
    (["print 1 + 2;"], ({'Print': [{'Plus': [{'Number': [1]}, {'Number': [2]}]}, 'End']})),\
    (["print @a[1];"], ({'Print': [{'Array': [{'Variable': ['a']}, {'Number': [1]}]}, 'End']})),\
    (["assign a := [1,4,6];"], ({'Assign':[{'Variable':['a']}, {'Number':[1]}, {'Number':[4]}, {'Number':[6]}, 'End']})),\
    (["assign a := [1+2,4,6];"], ({'Assign':[{'Variable':['a']}, {'Plus':[{'Number':[1]},{'Number':[2]}]}, {'Number':[4]}, {'Number':[6]}, 'End']})),\
    (["assign a := [1,2,3]; for a { print 4; }"], ({'Assign': [{'Variable': ['a']}, {'Number': [1]}, {'Number': [2]}, {'Number': [3]}, {'For': [{'Variable': ['a']}, {'Print': [{'Number': [4]}, 'End']}, 'End']}]}))
    ])
 
print("Problem #2")
try: interpret
except: print("The interpret() function is not defined.")
else: check('interpret', interpret, [\
    (["print true;"], [True]),\
    (["print 4;"], [4]),\
    (["print 1 + 2;"], [3]),\
    (["assign a := [1,2,3]; print a;"], [[1,2,3]]),\
    (["assign a := [1+2,2,3]; print a;"], [[3,2,3]]),\
    (["assign a := [1+1,2+2,3+3]; print a;"], [[2,4,6]]),\
    (["assign a := [1,2,3]; print @a[1];"], [2]),\
    (["assign a := [1+1,2+2,3+3]; print @a[0]; print @a[1]; print @a[2];"], [2,4,6]),\
    (["assign a := [1,2,3]; for a { print 4; }"], [4, 4, 4]),\
    ])
 
print("Problem #3")
try: compileAndSimulate
except: print("The compileAndSimulate() function is not defined.")
else: check('compileAndSimulate', compileAndSimulate, [\
    (["print 123;"], [123]),\
    (["print false; print true; print 4;"], [0, 1, 4]),\
    (["print 1 + 2;"], [3]),\
    # [1] or [[1, 2, 3]], do we even need this ??
    #(["assign a := [1, 2, 3]; print a;"], [1]),\
    (["assign a := [1, 2, 3]; print @a[0]; print @ a[1]; print @ a[2];"], [1, 2, 3]),\
    (["assign a := [1+1, 2+2, 3+3]; print @a[0]; print @a[1]; print @a[2];"], [2, 4, 6]),\
    ])
 
print("Problem #4")
try: typeProgram
except: print("The typeProgram() function is not defined.")
else: check(('typeProgram(tokenizeAndParse(', '))'), lambda s: typeProgram({}, tokenizeAndParse(s)), [\
    (["print 123;"], 'Void'),\
    (["print true;"], 'Void'),\
    (["print 123; print false;"], 'Void'),\
    (["print 1 + 2;"], 'Void'),\
    (["print a;"], None),\
    (["assign a:= [1,2,3]; print @a[0]; print @a[1]; print @a[2];"], 'Void'),\
    (["assign a:= [1+1,2+2,3+3]; print @a[0]; print @a[1]; print @a[2];"], 'Void'),\
    (["assign a:= [true,2,3]; print @a[0];"], None),\
    (["assign a:= [true,2,3]; print a;"], None),\
    (["assign a:= [1,2,3]; for a { print 1; }"], 'Void'),\
    (["assign a:= [1,2,3]; for a { print 1 + 2; }"], 'Void'),\
    ])