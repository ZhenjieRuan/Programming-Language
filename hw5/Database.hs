---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2014
-- Assignment 5 (skeleton code)
-- Database.hs
--

module Database where

type Column = String  -- User Defined type
data User = User String deriving (Eq, Show)
data Table = Table String deriving (Eq, Show)
data Command =
    Add User
  | Create Table
  | Allow (User, Table)
  | Insert (Table, [(Column, Integer)])
  deriving (Eq, Show)

example = [
    Add (User "Alice"),
    Add (User "Bob"),
    Create (Table "Revenue"),
    Insert (Table "Revenue", [("Day", 1), ("Amount", 2400)]),
    Insert (Table "Revenue", [("Day", 2), ("Amount", 1700)]),
    Insert (Table "Revenue", [("Day", 3), ("Amount", 3100)]),
    Allow (User "Alice", Table "Revenue")
  ]


lookup' :: Column -> [(Column, Integer)] -> Integer
lookup' c' ((c,i):cvs) = if c == c' then i else lookup' c' cvs


-- Complete for Assignment 5, Problem 1, part (a).
select :: [Command] -> User -> Table -> Column -> Maybe [Integer]
select command u1 t1 c1 = 
  if 
    [()| Add u1 <- command] /= [] &&
    [()| Create t1 <- command] /= [] &&
    [()| Insert t1 _ <- command] /= []
  then
    Just([num | Insert (t1, item) <- command , num <- [lookup' (c1)(item)]])
  else
    Nothing



-- Type synonym for aggregation operators.
type Operator = Integer -> Integer -> Integer

-- Complete for Assignment 5, Problem 1, part (b).
aggregate :: [Command] -> User -> Table -> Column -> Operator -> Maybe Integer
aggregate command u1 t1 c1 operator =
  if
    elem (Add u1) command && -- check if user exists
    elem (Create t1) command && -- check if table exists
    elem (Allow (u1, t1)) command -- check if the user has permission 
  then
    Just(foldr operator 0 [num | Insert (t1, item) <- command , num <- [lookup' (c1)(item)]])
  else
    Nothing



-- Complete for Assignment 5, Problem 1, part (c).
validate :: [Command] -> Bool
validate command = check (reverse command)

check :: [Command] -> Bool
check ((Allow (u1,t1)):rest) =
  if elem (Add u1) rest && elem (Create t1) rest
  then check rest
  else
    False
check ((Insert (t1,_)):rest) =
  if elem (Create t1) rest
  then check rest
  else
    False
check _ = True



--eof