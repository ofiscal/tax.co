# Setup

The makefile will try to build the executable.
If that fails it should be in the logs.
If it succeeds, the default symlink here might not work,
because it depends on your version of ghc.

If it's broken, you'll know because the link
`haskell/Main` will point to a nonexistent file.
To fix it, go to the `haskell/` folder and run
```
find  . -name "Main" -type f
```
delete the old symlink, and make a new one
pointing to the file that `find` discovered.

Now the Makefile will be able to run the executable
by referring to it as `haskell/Main`.

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
