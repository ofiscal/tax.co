This describes the
[branches, in the git sense of the word](https://git-scm.com/docs/git-branch),
which the code has gone through.

Not all branches are documented here. For those that aren't:
Most branches begin with a commit message explaining their intended purpose.

Note that some branches diverge from their original scope,
including work that falls outside it.

# average-vat-spending-per-rate (complete)

In November 2019,
a reporter asked us if we could determine how much tax is collected per VAT rate.
This computes a number of variations on that.

## How it works

Compute average (across households) fraction of spending at each tax rate.
Use the max vat rate.
Ignore goods for which the VAT rate is not one of 0, 5 or 19%.

Make columns "spent @ vat x" for x in [0,5,19].
Carry those until total household spending exists.
Compute columns "fraction spent @ vat x" for x in [0,5,19].
Take their averages.
Verify that the sum of those averages is close to unity.

# csv_convert_without_python (dormant)

The initial processing of the data is all done in Python using Pandas.
It uses a lot of memory -- so much that my laptop became unable to handle it.
I had a plan to switch from Pandas to Vaex,
which processes on disk rather than in memory.

Vaex (currently) can only ingest csv-formatted data.
The aim of this branch was to convert all data to the .csv format initially,
without using Python at all. It would make Vaex feasible,
and would also simplify some other processing -- for instance,
because csvtools-processed files seem to be read more often as numbers rather than strings in Python.

# gui (unfinished, obsolete)

This branch was intended for research.
It didn't get very far.
We wanted to scrape a website that requires a lot of clicking the mouse.
It would have taken person-years by hand.
I wanted to use selenium to automate the work.
The first step was to figure out how to run Firefox in the Docker container,
which meant connecting the container to the native graphics environment.

# safe-strings (dormant)

The purpose of this branch was to assign each column name
(and in the case of categorical variables, each column value)
to a variable, and then use that variable instead of the raw string.
But once I could see what that's like, I started to doubt the value of it
-- it creates some boilerplate that could be hard to maintain,
and requires a lot of tedious definitions that can be more easily handled with regular expressions
(e.g. in build.people.main).

# qc-for-cb (???)

Stands for "quality control for the central bank".
We were about to do a presentation at the central bank,
and I wanted to be sure the model was accurate.
I don't remember what I did or what the result was --
would have to look through the history of diffs to find out.

# time-to-save-for-a-month

Finds how long it would take a household to save for a month, if in that month they had to spend what they spent during the time of the survey.

Most salient result: No matter how I sliced it, around half of households spend more than they earn, but around a fifth save more than 2/3 of their income.

# vaex

Using Pandas, tax.co can throw memory errors on an 8GB system.
(In Ubuntu it doesn't, but in NixOS it does --
at least if I install the OS with its default memory configuration.)
This branch is an incomplete attempt at using Vaex instead,
which processes on disk rather than in memory.

The memory errors are common in the early stages, through subsampling.
After that I haven't run into them. So if I were to introduce Vaex,
I might not need to propogate it any farther than the subsampling stage.
