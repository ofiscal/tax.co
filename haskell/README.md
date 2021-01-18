# Run tests from command line

From the command line (in the Docker container),
from this folder (such that Demo/Demo.hs is found), run
```
runhaskell Demo/Demo.hs a b
```

# Load into GHCI

From here (in the Docker container):
```
cabal repl   # after this you'll be in GHCI
:s .ghci     -- loads the libraries listed in the file ".ghci"
runTests     -- do this regularly
```
