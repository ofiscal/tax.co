# How to read these Makefile dependencies

Look at `dependencies.png`.
If that doesn't exist, see the next section,
"How to draw these Makefile dependencies".

It looks hard to read,
but that's because it draws all the code that's depended on.
The easy way to read it is to ignore all those `.py` files,
none of which depend on anything themselves,
and consider instead just the `.csv` files.
Roughly, that means looking at the red ovals,
and not the green ones.

# How to draw these Makefile dependencies

This README describes how to generate an image called `dependencies.png`
that graphically illustrates the dependencies encoded in the Makefile --
that is, which files (both code and data) depend on which.

It uses [makefile2graph](https://github.com/lindenb/makefile2graph),
which is included in the tax.co Docker image.

## Optional: First make the graph easier to read

In the Makefile, comment out (by putting a `#` in front of them)
most of the files in the definitions of `enph_files` and `overview`.
(As of 2021 July 08, `simplify.diff` shows what those changes look like.)

## Next, run this

```
make overview -Bnd                                         \
  config_file=config/config.json                           \
  subsample=1                                              \
  strategy=detail                                          \
  regime_year=2019                                         \
  user=u59b2b1ba567d0dec94345c66793e9122                   \
  | make2graph                                             \
  | sed -r "s/([a-zA-Z0-9_\-\.\(\)]+)\.(csv|py)/\n\1.\2/g" \
  | dot -Tpng -o dependencies.png
```

Be sure to change the Makefile back to how it was before running it again.
