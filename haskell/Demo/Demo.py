# This is to test whether / demonstrate how a haskell program can be called
# from somewhere other than the root of the haskell source tree.
# From /mnt, try running this as
#   PYTHONPATH="." python3 haskell/Demo.py
# and see if it runs haskell/Demo.hs (note the different file extensions).
import os

os.chdir ( "haskell/" )
os.system( "runhaskell Demo.hs a b" )
