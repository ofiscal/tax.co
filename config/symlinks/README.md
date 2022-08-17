# These are not important.

Thesee links are convenient for development,
but not used in production.
If they point to files that don't exist,
it won't matter.

# PURPOSE | How to use them

To redefine the default config, do this:
```
cd config
rm config.json
ln -s symlinks/baseline config.json
```

instead of this:
```
cd config
rm config.json
ln -s symlinks/baseline ../users/symlinks/baseline/config/config.json
```
