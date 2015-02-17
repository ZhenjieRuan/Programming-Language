module TypeCheck where

import AbstractSyntax
import Parse

class Typeable a where
  chk :: [(String, Type)] -> a -> Maybe Type
  
instance Typeable Exp where -- Implement for Problem #1, part (c).
  chk env (Value e1) = Just Bool 
  chk env (And e1 e2) =
  	if chk env e1 == Just (Bool) && chk env e2 == Just (Bool) then Just (Bool) else Nothing
  chk env (Or e1 e2) =
  	if chk env e1 == Just (Bool) && chk env e2 == Just (Bool) then Just (Bool) else Nothing
  chk env (Not e1) = 
  	if chk env e1 == Just (Bool) then Just (Bool) else Nothing
  chk env (Variable x) = 
  	lookup x env

instance Typeable Stmt where  -- Implement for Problem #1, part (c).
  chk env (Print e s) = 
  	if chk env s == Just (Void) && chk env e == Just (Bool) then Just (Void) else Nothing
  chk env (Assign x e s) =
  	let env' = env ++ [(x, unwrap (chk env e))]
  	in if chk env' s == Just (Void) then Just (Void) else Nothing
  chk env (End) = Just (Void)

-- eof