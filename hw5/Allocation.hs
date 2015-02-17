---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2014
-- Assignment 5 (skeleton code)
-- Allocation.hs
--

module Allocation where

type Item = Integer
type Bin = Integer
type Allocation = Alloc

data Alloc = Alloc Bin Bin deriving (Eq, Show)

data Graph =
    Branch Alloc Graph Graph 
  | Finish Alloc
  deriving (Eq, Show)

type Strategy = Graph -> Graph

graph :: Alloc -> [Item] -> Graph
graph (Alloc b1 b2) (item : rest) =
	Branch (Alloc b1 b2)
	(graph (Alloc (b1 + item) b2) rest)
	(graph (Alloc b1 (b2 + item)) rest)
graph (Alloc b1 b2) [] =
	Finish (Alloc b1 b2)

alloc :: Graph -> Alloc
alloc (Branch a1 g1 g2) = a1
alloc (Finish a1) = a1

instance Ord Alloc where
	(Alloc a1 a2) <= (Alloc b1 b2) = if abs(a1 - a2) <= abs(b1 - b2) then True else False

instance Ord Graph where
	(Branch a1 g1 g2) <= (Branch a1' g1' g2') = if a1 < a1' then True else False
	(Finish a1) <= (Finish a1') = if a1 < a1' then True else False

final :: Graph -> [Alloc]
final (Branch a1 g1 g2) = final(g1) ++ final(g2)
final (Finish a1) = [a1]

depth :: Integer -> Graph -> [Alloc]
depth n (Finish a1) = if n == 0 then [a1] else []  
depth n (Branch a1 g1 g2) = if n == 0 then [a1] else (depth (n - 1) g1) ++ (depth (n - 1) g2)

greedy :: Strategy
greedy (Branch a1 g1 g2) = if g1 < g2 then g1 else g2
greedy (Finish a1) = Finish a1

patient :: Integer -> Strategy
patient 0 g1 = g1
patient n (Branch a1 g1 g2) = greedy (Branch a1 (patient (n - 1) g1) (patient (n - 1) g2))

optimal :: Strategy
optimal (Finish a1) = Finish a1
optimal (Branch a1 g1 g2) = greedy (Branch a1 (optimal g1) (optimal g2))

metaCompose :: Strategy -> Strategy -> Strategy
(metaCompose s1 s2) g1 = s2(s1(g1))

metaRepeat :: Integer -> Strategy -> Strategy
(metaRepeat 0 s1) g1 = g1
(metaRepeat n s1) g1 = (metaRepeat (n - 1) s1) (s1(g1))

metaGreedy :: Strategy -> Strategy -> Strategy
(metaGreedy s1 s2) g1 = greedy (Branch (Alloc 0 0) (s1(g1)) (s2(g1)))

--eof