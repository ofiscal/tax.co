# PURPOSE

To save and replace user states --
the set of user folders (`users/u*`),
`data/request*` files,
and the top-level `requests-log.txt`.

# USAGE

Run these from the root of the project.

`save.sh` takes one argument,
the name of the folder within `state/` to be saved to.
That folder does not need to exist yet.
Indeed it shouldn't -- see PITFALL below.

`clean.sh` deletes the user state data from the project,
so that it can be restored from one of the saved states here.

`restore.sh` takes one argument,
the name of the folder within `state/` to be saved to.

# PITFALL

That there is no "clean" script for these saved data,
corresponding to `clean.sh` for the project.
Instead just delete the folder.
