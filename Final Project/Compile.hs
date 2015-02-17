module Compile where

import AbstractSyntax
import Allocation
import Machine
import TypeCheck

--statement s	::=	print e ; s   |  assign x := e ; s   |  end ;
--expression e::=	v  |  x  |  and ( e , e )  |  or ( e , e )  |  not ( e )
--variable x	::=	[a-z]+
--value v	::=	true  |  false
--type τ	::=	Bool  |  Void


class Compilable a where
  comp :: [(Var, Register)] -> a -> Instruction

instance Compilable Stmt where -- Complete missing cases for Problem #4, part (b).
  comp xrs (End         )  = STOP (Register 0)
  comp xrs (Print    e s)  = (comp xrs e) +++ (COPY (Register 0) (register (comp xrs e)) (comp xrs s))
  comp xrs (Assign x e s)  = 
  	let instExp = comp xrs e
	in instExp +++ (COPY (lookup' x xrs) (register instExp) (comp xrs s))

instance Compilable Exp where -- Complete missing cases for Problem #4, part (b).
  comp xrs (Variable x) = STOP (lookup' x xrs)
  comp xrs (Value v) = 
  	let new_reg = if xrs /= [] then maximum[r | (_,r) <- xrs] + 1 else Register 1
  	in
  		if v == True then INIT new_reg (FLIP new_reg (STOP new_reg)) else INIT new_reg (STOP new_reg) 
  comp xrs (And e1 e2) = 
  	let instExp1 = comp xrs e1
  	    new_reg  = if xrs /= [] then maximum[r | (_,r) <- xrs] + 1 else Register 1
  	    v1 = new_reg + 1
  	    v2 = v1 + 1
  	in
  		instExp1 +++ (COPY v1 (register instExp1) ((comp xrs e2)+++(COPY v2 (register (comp xrs e2))) (INIT new_reg (NAND v1 v2 new_reg (FLIP new_reg(STOP new_reg))))))
  comp xrs (Or e1 e2) = 
    let instExp1 = comp xrs e1
        instExp2 = comp xrs e2
        new_reg  = if xrs /= [] then maximum[r | (_,r) <- xrs] + 1 else Register 1
        v1 = new_reg + 1
        v2 = v1 + 1
    in
      instExp1 +++ (COPY v1 (register instExp1) (instExp2+++(COPY v2 (register instExp2)) (INIT new_reg (FLIP v1 (FLIP v2 (NAND v1 v2 new_reg (STOP new_reg)))))))
  comp xrs (Not e1) = 
    let instExp = comp xrs e1
        reg = register instExp
    in
      instExp +++ (FLIP (reg) (STOP(reg)))
 

compileMin :: Stmt -> Maybe Instruction -- Complete for Problem #4, part (c).
compileMin s = if (chk [] s) /= Nothing then
  let intf = interference s
      var = vars s
      rs = [Register (toInteger(i))|i <- [1 .. length(var)]]
      alloc = Alloc []
      minAlloc = unwrapAllocation(smallest (allocations (intf,rs) alloc var))
  in
    Just (comp minAlloc s)
  else
    Nothing



compileMax :: Integer -> Stmt -> Maybe Instruction -- Complete for Problem #4, part (d).
compileMax k s = if (chk [] s) /= Nothing then
  let intf = interference s
      var = vars s
      rs = [Register (toInteger(i))| i <- [1 .. length(var)]]
      alloc = Alloc []
      maxAlloc = unwrapAllocation(largest (allocations (intf,rs) alloc var))
  in
    Just (comp maxAlloc s)
  else
    Nothing

--help function
unwrapAllocation :: Allocation -> [(Var,Register)]
unwrapAllocation (Alloc a) = a


-- eof



























