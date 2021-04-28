These are the default config files.
A user can override any and all of them.
That is done not by modifying these files,
but by including like-named ones in the user's folder.
If a user does not override such a file,
a symlink is created in their folder,
pointing to it here.

`repl.json` is unlike the others.
It serves as a configuration file when in the Python REPL.
By contrast, when running from the shell,
Python uses a `shell.json` file from somewhere in `users/`.
`repl.json` is not overridden;
instead it should be edited in-place, here.
It should look something like `repl.MODEL.json`.
