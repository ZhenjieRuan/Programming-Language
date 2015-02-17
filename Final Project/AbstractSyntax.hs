module AbstractSyntax where

import Data.List (union, intersect, (\\), nub)

type Var = String
type Output = [Bool]

data Stmt =
    Print Exp Stmt
  | Assign Var Exp Stmt
  | End
  deriving (Eq, Show)

data Exp =
    Variable Var
  | Value Bool
  | And Exp Exp
  | Or Exp Exp
  | Not Exp
  deriving (Eq, Show)

data Type =
    Bool
  | Void
  deriving (Eq, Show)

-- Useful helper functions.
lookup' :: Eq a => a -> [(a, b)] -> b
lookup' x ((x',i) : rest) = if x == x' then i else lookup' x rest

getelem :: [[Var]] -> [Var]
getelem (x:xs) = x ++ getelem xs
getelem [] = []

strToA :: String -> [String]
strToA str = [str] 

-- Type class for a polymorphic fold function on abstract syntax trees.
--
--  * The first argument is the aggregator for combining
--    results of recursive folds.
--  * The second argument is a function that will be applied to
--    (i.e., and will replace) Variable nodes.
--  * The third argument is a constant that will replace all
--    non-Variable leaf nodes (i.e., Value nodes).
--  * The fourth argument is the abstract syntax tree that
--    will be folded.

class Foldable b where
  fold :: ([a] -> a) -> (String -> a) -> a -> b -> a

instance Foldable Exp where
  fold f var b (Variable x ) = var x
  fold f var b (Value v    ) = b
  fold f var b (And   e1 e2) = f [fold f var b e1, fold f var b e2]
  fold f var b (Or    e1 e2) = f [fold f var b e1, fold f var b e2]
  fold f var b (Not   e    ) = f [fold f var b e]

instance Foldable Stmt where
  -- Finish this definition for Problem #2, part (a).
  fold f var b (Print    e s) = f [fold f var b e, fold f var b s]
  fold f var b (Assign x e s) = f [fold f var b (Variable x), fold f var b e, fold f var b s]
  fold f var b (End)          = b

  

class HasVariables a where
  vars :: a -> [Var]


--nub is the haskell function remove duplicates in a list

instance HasVariables Stmt where
  vars stat = nub(fold getelem strToA [] stat) -- Implement for Problem #2, part (a).

instance HasVariables Exp where
  vars expr = nub(fold getelem strToA [] expr) -- Implement for Problem #2, part (a).



unbound :: Stmt -> [Var]
-- Implement for Problem #2, part (b).
unbound (End) = []
unbound (Print e s) = union (unbound s) (unboundExp e)
unbound (Assign x e s) = union ((unbound s) \\ [x]) (unboundExp e)

unboundExp :: Exp -> [Var]
unboundExp (Variable x) = [x]
unboundExp (Value v) = []
unboundExp (And e1 e2) = union (unboundExp e1) (unboundExp e2)
unboundExp (Or e1 e2) = union (unboundExp e1) (unboundExp e2)
unboundExp (Not e) = unboundExp e


type Interference = [(Var, Var)]

interference :: Stmt -> Interference
-- Implement for Problem #2, part (c).
interference (End) = []
interference (Print e s) = interference s
interference (Assign x e s) = interference s ++ [(x, y) | y <- (union (unboundExp e) (unbound s)), y /= x]


-- eof