module Machine where

import AbstractSyntax

data Register =
    Register Integer
  deriving (Eq, Show)

instance Ord Register where
	Register a <= Register b = if a <= b then True else False
instance Num Register where
	fromInteger n = Register n
	(Register a1) + (Register a2) = Register (a1 + a2)
	(Register a1) - (Register a2) = Register (a1 - a2)	

-- Add instance declarations here for Problem #4, part (a).  


data Instruction =
    INIT Register Instruction
  | FLIP Register Instruction
  | COPY Register Register Instruction --copy to from 
  | NAND Register Register Register Instruction
  | STOP Register
  deriving (Eq, Show)

(+++) :: Instruction -> Instruction -> Instruction
(+++) (INIT r     i) j = INIT r (i +++ j)
(+++) (FLIP r     i) j = FLIP r (i +++ j)
(+++) (COPY r s   i) j = COPY r s (i +++ j)
(+++) (NAND r s t i) j = NAND r s t (i +++ j)
(+++) (STOP _      ) j = j

register :: Instruction -> Register
register (INIT _     i) = register i
register (FLIP _     i) = register i
register (COPY _ _   i) = register i
register (NAND _ _ _ i) = register i
register (STOP r    )   = r

nand :: Bool -> Bool -> Bool
nand True True = False
nand _    _    = True

step :: [(Register, Bool)] -> Instruction -> Output
step rbs (INIT r i)              = step ((r, False):rbs) i
step rbs (FLIP r i)              = step ((r, not (lookup' r rbs)):rbs) i
step rbs (COPY (Register 0) s i) = [lookup' s rbs] ++ step rbs i
step rbs (COPY r s i)            = step ((r, lookup' s rbs):rbs) i
step rbs (NAND r s t i)          = step ((t, nand (lookup' r rbs) (lookup' s rbs)):rbs) i
step rbs (STOP r)                = []

simulate :: Instruction -> Output
simulate instructions = step [] instructions

-- eof