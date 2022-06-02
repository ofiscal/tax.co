
# Hack the code
## The three ways to run the code from the Docker container

(1) You can use the `Makefile`. If you intend to run the entire model,
this is the way to do it. `make` is a utility which reads a `Makefile`
and determines what to run, in what order. The `Makefile`
describes the inputs and outputs of each program.
(It does not distinguish between code and data -- they're all just files.)
If something has already been built recently,
and nothing it depends on has changed, it won't be built again.
To do what the Makefile does yourself, you'd need to enter a lot of commands,
and keep track of a lot of dependencies; it would be hard and boring.

(2) For interactive coding, you can run a Python REPL in the Docker container.
This gives you the advantage of a searchable command history.
However, graphics cannot be viewed from within it;
they must be output to a file,
which can then be viewed from a (native) application.

(3) Alternatively, for interactive coding, you can run iPython.
This lets you run and edit code in a .ipynb document,
which can include graphics, from a browser (e.g. Firefox, Chrome).

I typically open two Bash views into the same Docker container,
and run iPython from one and a Python REPL from the other.
When I want to explore graphics I use the browser;
the rest of the time I use the REPL.
You don't really need both (2) and (3).
(If I had to choose, I'd stick to (2).)


## (1) Running the Makefile

The easiest way to use the Makefile is through the `make-all-models.sh` script described above.
To change other parameters besides the sample size,
edit `make-all-models.sh`.

You can also call the Makefile yourself.
Read `make-all-models.sh` for an example of how to do that.


## (2) Running code in Bash in Docker

From within the Bash view,
change directories to the one where the code is mounted: `cd /mnt`.

Run `python3`. Now you're in a Python shell,
which is running within the Bash shell,
which is running within the Docker container.

Now you can type individual commands.
If you'd like to run an entire program,
there's a command for that:
`exec(open("python/path/blablabla/file_to_run.py").read())`.


## (3) launching iPython from Bash in Docker

Run this: `opt/conda/bin/conda install jupyter -y --quiet && /opt/conda/bin/jupyter notebook --notebook-dir=/mnt --ip='*' --port=8888 --no-browser --allow-root`.

It will process for a little while,
and then display a URL you can visit to interact with iPython.
