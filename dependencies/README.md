# draw Makefile dependencies

This README describes how to generate an image called `dependencies.png`
that graphically illustrates the dependencies encoded in the Makefile --
that is, which files (both code and data) depend on which.

It uses [makefile2graph](https://github.com/lindenb/makefile2graph).

## the basic syntax
Substitute something (e.g. "overview") for "target" below:
make <target> -Bnd | make2graph | dot -Tpng -o dependencies.png

## to make it easier to read
First comment out most of the definition of enph_files.
Then run this:

make overview -Bnd vat_strategy="()" | make2graph \
  | sed -r "s/([a-zA-Z0-9_\-\.\(\)]+)\.(csv|py)/\n\1.\2/g" \
  | dot -Tpng -o dependencies.png
