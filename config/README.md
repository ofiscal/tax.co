These are the default config files.
A user can override any and all of them.
That is done not by modifying these files,
but by including like-named ones in the user's folder.
If a user does not override such a file,
a symlink is created in their folder,
pointing to the default here.

`config.json` in this folder serves as a configuration file
when in the Python REPL.
It is also the default configuration file used by
`python/run-makefile.py` when none is specified.
Output in that case will still go to some subfolder of the `users/` folder --
specifically, a subfolder named
'u' + the hash of the user_email specified in `config.json`.

When the simulation is called from the webapp,
`user_email` determines where those results are sent.
