These are the default config files.
A user can override any and all of them.
That is done not by modifying these files,
but by including like-named ones in the user's folder.
If a user does not override such a file,
a symlink is created in their folder,
pointing to the default here.

`config.json` in this folder is unlike the others.
It serves as a configuration file when in the Python REPL --
whereas when Python is run from the shell without a REPL,
it uses a `config.json` file from somewhere in `users/`.
`config.json` here is never overridden by another file;
instead it should be edited in-place.
It should look something like `repl.MODEL.json`.
