module Interpret where

import AbstractSyntax
import Parse
import TypeCheck

eval :: [(String, Bool)] -> Exp -> Bool
eval env (And e1 e2) = eval env e1 && eval env e2
eval env (Or e1 e2) = eval env e1 || eval env e2
eval env (Not e1) = not (eval env e1)
eval env (Value e1) = e1
eval env (Variable e1) = 
	lookup' e1 env -- Implement for Problem #1, part (b).

exec :: [(String, Bool)] -> Stmt -> ([(String, Bool)], Output)
exec env (Print    e s) =
  let (env', o) = exec env s
  in (env', [eval env e] ++ o)
exec env (Assign x e s) =
  let env' = env ++ [(x,eval env e)]
  in(env',  snd(exec env' s))
exec env (End) = (env,[]) -- Implement the Assign and End cases for Problem #1, part (b).

interpret :: Stmt -> Maybe Output
interpret  statment= -- Implement for Problem #1, part (d).
  if chk [] statment /= Nothing then Just (snd(exec [] statment)) else Nothing


-- eof