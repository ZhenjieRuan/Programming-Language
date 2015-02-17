module Allocation where

import Data.List (union, intersect, (\\), nub)
import AbstractSyntax
import Machine

data Tree a =
    Branch a [Tree a]
  | Finish a
  deriving (Eq, Show)

foldTree :: ([a] -> a) -> Tree a -> a
foldTree f (Finish a) = a   -- Complete for Problem #3, part (a).
foldTree f (Branch a b) = f [foldTree f t| t <- b]

smallest :: Ord a => Tree a -> a
smallest t = foldTree minimum t -- Complete for Problem #3, part (b).

largest :: Ord a => Tree a -> a
largest t = foldTree maximum t -- Complete for Problem #3, part (b).

data Allocation =
    Alloc [(Var, Register)]
  deriving (Eq, Show)

-- Add instance declaration for Problem #3, part (c) here.
instance Ord Allocation where
	Alloc a <= Alloc b = if length (nub [a_reg | (a_var, a_reg) <- a]) <= length (nub [b_reg | (b_var, b_reg) <- b]) then True else False



allocations :: (Interference, [Register]) -> Allocation -> [Var] -> Tree Allocation
allocations (conflicts, rs) (Alloc a) [] = Finish (Alloc a)
allocations (conflicts, rs) (Alloc a) (x:xs) = 
	let rs' = unconflicted (conflicts, rs) (Alloc a) x
	in Branch (Alloc a) [allocations (conflicts, rs) (Alloc (a ++ [(x, r)])) xs | r <- rs']

-- Useful helper function.
unconflicted ::(Interference, [Register]) -> Allocation -> Var -> [Register]
unconflicted (conflicts, rs) (Alloc a) x = rs \\ [r | (y,r) <- a, (x,y) `elem` conflicts || (y,x) `elem` conflicts]

--eof