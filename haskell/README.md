# Execution

## Execution with compilation

```
./Main ../python/csv_dynamic/r2019/most
```

This will generate `../python/csv_dynamic/r2019/most.py`
from `../python/csv_dynamic/r2019/most.csv`,
assuming the latter exists.

## Execution without compilation

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

# Compile Main.hs

```
ghc -o Main Main.hs
```

This creates an executable called `Main` from `Main.hs`.
