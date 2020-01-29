# Some folders have a "main.py" program

If so, and if there is no README.md file for that folder,
the header comment in "main.py"
probably describes what the entire folder is for.

# Pay attention to PITFALL comments

They document likely points of confusion.

# For an overview

For an overview of how these processes depend on each other and the input data, see the `dependencies/` folder.

# _defs.py and _test.py files

If you see a file called "name.py" (where "name" could be anything), you might find another file in the same folder called "name_defs.py". If you do, "name_defs.py" defines things that are only used by "name.py".

Similarly, "name_test.py" defines some ways to test "name.py".x
