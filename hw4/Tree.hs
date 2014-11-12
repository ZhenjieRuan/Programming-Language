---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2014
-- Assignment 4 (skeleton code)
-- Tree.hs
--
module Tree where

data Tree =
    Leaf
  | Twig
  | Branch Tree Tree Tree
   deriving (Eq,Show);

twigs :: Tree -> Integer
twigs(Twig) = 1
twigs(Leaf) = 0
twigs(Branch t1 t2 t3) = twigs(t1) + twigs(t2) + twigs(t3)

branches :: Tree -> Integer
branches(Twig) = 0
branches(Leaf) = 0
branches (Branch t1 t2 t3) = 1 + branches(t1) + branches(t2) + branches(t3)

height :: Tree -> Integer
height(Leaf) = 0
height(Twig) = 1
height(Branch t1 t2 t3) = 1 + maximum[height(t1) ,height(t2) ,height(t3)]

perfect :: Tree -> Bool
perfect(Leaf) = False
perfect(Twig) = False
perfect(Branch Leaf Leaf Leaf) = True
perfect(Branch t1 t2 t3) = perfect(t1) && perfect(t2) && perfect(t3)

degenerate :: Tree -> Bool
degenerate(Twig) = True
degenerate(Leaf) = True
degenerate(Branch t1 Leaf Leaf) = True && degenerate(t1)
degenerate(Branch t1 Twig Twig) = True && degenerate(t1)
degenerate(Branch Leaf t1 Leaf) = True && degenerate(t1)
degenerate(Branch Twig t1 Twig) = True && degenerate(t1)
degenerate(Branch Leaf Leaf t1) = True && degenerate(t1) 
degenerate(Branch Twig Twig t1) = True && degenerate(t1)
degenerate(Branch t1 Twig Leaf) = True && degenerate(t1)
degenerate(Branch t1 Leaf Twig) = True && degenerate(t1)
degenerate(Branch Twig t1 Leaf) = True && degenerate(t1)
degenerate(Branch Leaf t1 Twig) = True && degenerate(t1)
degenerate(Branch Leaf Twig t1) = True && degenerate(t1)
degenerate(Branch Twig Leaf t1) = True && degenerate(t1)
degenerate(Branch t1 t2 t3) = False


leaves :: Tree -> Integer
leaves(Twig) = 0
leaves(Leaf) = 1
leaves(Branch t1 t2 t3) = leaves(t1) + leaves(t2) + leaves(t3)

infinite :: Tree
infinite = Branch infinite infinite infinite

--eof