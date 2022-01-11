# This folder is not for human manipulation.

The Makefile writes empty files here to know when to rebuild things.
The only information such files convey are their names and timestamps.
The names correspond to source files.
Timestamps are maxima for the last time a file or anything it depends on was modified.

# More detail

For any sourcefile `x` there might be a corresponding empty file `.no_younger_than/x`.
If so, and the timestamp on `.no_younger_than/x` is T,
then neither `x` nor any source file it imports was not modified any later than time T.

If the Makefile finds that an output `o` depends on `x`,
and the timestamp on `.no_younger_than/x` is more recent than the one on `o`,
then it must rerun the recipe for `o`.
