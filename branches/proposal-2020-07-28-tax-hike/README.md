This branch depends on some variables that were removed from `python/build/`
in commit
```
2c82f5faad432aa1971bd940341adef2bf73ea02
```

The idiom at that time was to build all variables at once
and include them in the same data. Perhaps a better idiom going forward
will be to change the configuration data to evaluate alternative proposals,
and add code for comparing the output from two separate configurations.
