module Test where

import Parse
import AbstractSyntax
import TypeCheck
import Interpret
import Allocation
import Machine
--import Compile

allTests = [
  p1Tests, 
  p2Tests,
  p3Tests,
  p4Tests
  ]

p1Tests = [
	show (failed parseExpTests),
  show (failed parseStmtTests),
  show (failed interpretTests)
	]

p2Tests = [
	show (failed varsExpTests),
  show (failed varsStmtTests),
  show (failed unboundTests),
  show (failed interferenceTests)
	]

p3Tests = [
	show (failed foldTreeTests),
  show (failed smallestTests),
  show (failed largestTests),
  show (failed orderAllocTests)
	]

p4Tests = [
	show (failed registerTests)
	]

-- To get the failures for an individual test, query that
-- test using "failed", e.g.:
-- 
-- *> failed parseExpTests

failed :: Eq a => [(Integer, a, a)] -> [(Integer, a, a)]
failed tests = [(n, x, y) | (n, x, y) <- tests, x /= y]

parseExp  e = fst $ (\(Just x)->x) $ parse (tokenize (e)) :: Exp
parseStmt s = fst $ (\(Just x)->x) $ parse (tokenize (s)) :: Stmt

e0 = ["true",
	    "false",
			"var",
			"and(true,false)",
			"or(vara,varb)",
			"not(false)"
			]

parseExpTests = [
  (0, parseExp (e0!!0), (Value True)),
  (1, parseExp (e0!!1), (Value False)),
  (2, parseExp (e0!!2), (Variable "var")),
  (3, parseExp (e0!!3), (And (Value True) (Value False))),
  (4, parseExp (e0!!4), (Or (Variable "vara") (Variable "varb"))),
  (5, parseExp (e0!!5), (Not (Value False)))
	]

s0 = ["end;",
 		  "print not (true); end;",
 		  "assign x := true; end;",
 		 	"print and(var,true); assign y := false; end;",
 		 	"assign z := or(true, true); print false; end;",
 		 	"assign x := not(and(true, false)); print x; assign a := not(and(x, x)); print a; end;"
 		 	]

parseStmtTests = [
	(0, parseStmt (s0!!0), (End)),
	(1, parseStmt (s0!!1), (Print (Not (Value True)) End)),
	(2, parseStmt (s0!!2), (Assign "x" (Value True) End)),
	(3, parseStmt (s0!!3), (Print (And (Variable "var") (Value True)) (Assign "y" (Value False) End))),
	(4, parseStmt (s0!!4), (Assign "z" (Or (Value True) (Value True)) (Print (Value False) End))),
	(5, parseStmt (s0!!5), (Assign "x" (Not (And (Value True) (Value False))) (Print (Variable "x") (Assign "a" (Not (And (Variable "x") (Variable "x"))) (Print (Variable "a") End)))))
	]

interpretTests = [
	(0, interpret example, Just [True, False])
	]

e1 = ["true",
			"false",
			"var",
			"and(true,false)",
			"or(vara,varb)",
			"or(vara,vara)",
			"not(false)"
			]

varsExpTests = [
	(0, vars (parseExp (e1!!0)), []),
	(1, vars (parseExp (e1!!1)), []),
	(2, vars (parseExp (e1!!2)), ["var"]),
	(3, vars (parseExp (e1!!3)), []),
	(4, vars (parseExp (e1!!4)), ["vara", "varb"]),
	(5, vars (parseExp (e1!!5)), ["vara"]),
	(6, vars (parseExp (e1!!6)), [])
	]

s1 = ["end;",
 		  "print x; end;",
 		  "assign x := y; end;",
 		 	"print and(x,x); assign y := false; end;",
 		 	"assign z := or(true, true); print x; end;",
 		 	"assign x := not(and(true, false)); print x; assign a := not(and(x, x)); print a; end;"
 		 	]

varsStmtTests = [
	(0, vars (parseStmt (s1!!0)), []),
	(1, vars (parseStmt (s1!!1)), ["x"]),
	(2, vars (parseStmt (s1!!2)), ["x", "y"]),
	(3, vars (parseStmt (s1!!3)), ["x", "y"]),
	(4, vars (parseStmt (s1!!4)), ["z", "x"]),
	(5, vars (parseStmt (s1!!5)), ["x", "a"])
	]

s2 = ["end;",
 		  "print x; end;",
 		  "assign x := y; end;",
 		 	"print and(x,x); print y; end;",
 		 	"assign x := or(true, y); print x; print y; end;",
 		 	"assign x := not(and(true, false)); print x; assign a := not(and(x, x)); print a; end;"
 		 	]

unboundTests = [
	(0, unbound (parseStmt (s2!!0)), []),
	(1, unbound (parseStmt (s2!!1)), ["x"]),
	(2, unbound (parseStmt (s2!!2)), ["y"]),
	(3, unbound (parseStmt (s2!!3)), ["x", "y"]),
	(4, unbound (parseStmt (s2!!4)), ["y"]),
	(5, unbound (parseStmt (s2!!5)), [])
	]

s3 = ["end;",
 		  "print x; end;",
 		  "print x; print y; end;",
 		  "assign x := y; end;",
 		  "assign x := x; end;",
 		  "assign x := x; assign y := x; end;",
 		  "assign x := not(and(true, false)); print x; assign a := not(and(x, x)); print a; end;"
 		 	]

interferenceTests = [
	(0, interference (parseStmt (s3!!0)), []),
	(1, interference (parseStmt (s3!!1)), []),
	(2, interference (parseStmt (s3!!2)), []),
	(3, interference (parseStmt (s3!!3)), [("x","y")]),
	(4, interference (parseStmt (s3!!4)), []),
	(5, interference (parseStmt (s3!!5)), [("y", "x")]),
	(6, interference (parseStmt (s3!!6)), [("a","x")])
	]

t0 = [Finish 1,
			Branch 1 [(Finish 2), (Finish 3)],
			Branch 1 [(Branch 2 [Finish 3]), (Finish 4)],
			Branch 1 [(Finish 4), (Branch 2 [Finish 3])],
			Branch 1 [(Branch 2 [Finish 3]), (Branch 4 [Finish 5])],
			Branch 7 [(Branch 6 [Finish 5]), (Branch 4 [Finish 3]), (Branch 2 [Finish 1])]
			]

foldTreeTests = [
	(0, foldTree maximum (t0!!0), 1),
	(1, foldTree maximum (t0!!1), 3),
	(2, foldTree maximum (t0!!2), 4),
	(3, foldTree maximum (t0!!3), 4),
	(4, foldTree maximum (t0!!4), 5),
	(5, foldTree maximum (t0!!5), 7),
	(0, foldTree sum (t0!!0), 1),
	(1, foldTree sum (t0!!1), 6),
	(2, foldTree sum (t0!!2), 10),
	(3, foldTree sum (t0!!3), 10),
	(4, foldTree sum (t0!!4), 15),
	(5, foldTree sum (t0!!5), 28)
	]

smallestTests = [
	(0, smallest (t0!!0), 1),
	(1, smallest (t0!!1), 2),
	(2, smallest (t0!!2), 3),
	(3, smallest (t0!!3), 3),
	(4, smallest (t0!!4), 3),
	(5, smallest (t0!!5), 1)
	]

largestTests = [
	(0, largest (t0!!0), 1),
	(1, largest (t0!!1), 3),
	(2, largest (t0!!2), 4),
	(3, largest (t0!!3), 4),
	(4, largest (t0!!4), 5),
	(5, largest (t0!!5), 5)
	]

a0 = [Alloc [],
			Alloc [("x", Register 0)],
			Alloc [("x", Register 0), ("y", Register 0)],
			Alloc [("x", Register 0), ("y", Register 1)]
			]

orderAllocTests = [
	(0,  (a0!!0) <  (a0!!0), False),
	(1,  (a0!!0) <= (a0!!0), True ),
	(2,  (a0!!1) <  (a0!!1), False),
	(3,  (a0!!1) <= (a0!!1), True ),
	(4,  (a0!!2) <  (a0!!2), False),
	(5,  (a0!!2) <= (a0!!2), True ),
	(6,  (a0!!3) <  (a0!!3), False),
	(7,  (a0!!3) <= (a0!!3), True ),
	(8,  (a0!!0) <  (a0!!1), True ),
	(9,  (a0!!0) <= (a0!!1), True ),
	(10, (a0!!1) <  (a0!!2), False),
	(11, (a0!!1) <= (a0!!2), True ),
	(12, (a0!!2) <  (a0!!3), True ),
	(13, (a0!!2) <= (a0!!3), True ),
	(14, (a0!!1) <  (a0!!3), True ),
	(15, (a0!!1) <= (a0!!3), True )
	]

getFinish :: Tree a -> [a]
getFinish (Finish x  ) = [x]
getFinish (Branch x t) = concat [getFinish subtree | subtree <- t]

allocationsTests = do
	getFinish (allocations ([("z", "y"), ("x","y"), ("x", "z")],[Register 1, Register 2, Register 3]) (Alloc []) ["x","y","z"])
	getFinish (allocations ([("z", "y"), ("x","y"), ("x", "z")],[Register 1, Register 2, Register 3, Register 4]) (Alloc []) ["x","y","z"])
	getFinish (allocations ([("z", "y"), ("x","y")],[Register 1, Register 2, Register 3]) (Alloc []) ["x","y","z"])

registerTests = [
	(0, (Register 4) + 1, 																	Register 5),
	(1, (Register 4) - 1, 																	Register 3),
	(2, (maximum [Register 1, Register 4, Register 3]) + 1, Register 5)
	]

