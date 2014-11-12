---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2014
-- Assignment 4 (skeleton code)
-- Term.hs
--
module Term where

data Term =
    Number Integer
  | Abs Term
  | Plus Term Term
  | Mult Term Term

evaluate :: Term -> Integer
evaluate (Number n1) = n1
evaluate (Abs t1) = abs(evaluate(t1))
evaluate (Plus t1 t2) = evaluate(t1) + evaluate(t2)
evaluate (Mult t1 t2) = evaluate(t1) * evaluate(t2)

--eof