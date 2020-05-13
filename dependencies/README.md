# draw Makefile dependencies

This README describes how to generate an image called `dependencies.png`
that graphically illustrates the dependencies encoded in the Makefile --
that is, which files (both code and data) depend on which.

It uses [makefile2graph](https://github.com/lindenb/makefile2graph)
(which is included in the tax.co Docker image).

## the basic syntax
Substitute something (e.g. "overview") for "target" below:
make <target> -Bnd | make2graph | dot -Tpng -o dependencies.png

That will work but it's kind of hard to read;
see the next section for a more complex process with a simpler output.

## to make it easier to read
In the Makefile, comment out (by putting a `#` in front of them)
most of the files in the definitions of `enph_files` and `overview`.
Then run this:

make overview -Bnd vat_strategy="()" | make2graph \
  | sed -r "s/([a-zA-Z0-9_\-\.\(\)]+)\.(csv|py)/\n\1.\2/g" \
  | dot -Tpng -o dependencies.png

(Be sure to change the Makefile back to how it was before running it again.)
