This describes the branches the code has gone through, in the [git sense of the word](https://git-scm.com/docs/git-branch).

Not all branches are documented here. For those that aren't:
Most branches begin with a commit message explaining its intended purpose.

Note that some branches diverge,
including work that falls outside their original scope.

# average-vat-spending-per-rate (complete)

In November 2019,
a reporter asked us if we could determine how much tax is collected per VAT rate.
This computes a number of variations on that.

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
