# Set up some software

Install Git.
(For more information, see [Some software we use](Some-software-we-use.md).)

Download this Git repository,
with `git clone https://github.com/ofiscal/tax.co`.
(In the example below, I have located that folder at `/home/username/tax.co`. You'll want to put it somewhere else; change those paths accordingly.)

Install Docker.
(For more information, see [Some software we use](Some-software-we-use.md).
Docker is not strictly necessary,
but it's a really [good idea](Why-to-use-Docker.md).

Get the latest Docker image of tax.co,
by running `docker pull ofiscal/tax.co:latest`.
(Or you could build it yourself from [the Dockerfile](../docker/Dockerfile).)

Each time you use that image,
Docker will create a virtual Ubuntu Linux system.
By default that system is disconnected from your native system;
actions in the Docker container cannot affect the rest of your system.
However, you can "mount" a native folder to a folder in the Docker system,
which causes them to share their contents;
you can read and write to the file from either system.
(Once Dockmer has control of a folder,
you might need to use `sudo` to modify it from outside of Docker.)

Run the Docker image, mounting your native tax.co folder to the
`/mnt` folder in the Docker image.
For instance, if earlier you cloned the `tax.co` repository to a folder called `/home/username/tax.co/`, you would run this:
```
docker run --name tax-co -p 8888:8888 -itd -v /home/username/tax.co:/mnt ofiscal/tax.co
```
This starts a Docker container named `tax-co`.
(A Docker "container" is an environment running the code in a Docker "image".)

Open a Bash view into that Docker container:
`docker exec -it tax-co bash`.

# Download and build the raw ENPH data

See this repo's [ENPH README](../data/enph-2017/README.md) for how.

# Run the code

From the project's root folder (`tax.co/`),
run `bash/make-all-models 100`.
Doing so runs `bash/make-all-models.sh`
for the 1/100 subsample.
It will build a lot of data products,
writing them to the `output/` folder.
If you'd like to run the project the full sample,
provide the argument `1` instead of `100`.
(`10` and `1000` also work.)

If your computer's resources are like mine,
you might have to kill your web browser when building the subsamples.
(`make` echoes each command it's about to run to the screen,
so you know what it's doing; for instance, when it says
`PYTHONPATH='.' python3 python/subsample.py`,
it's building the subsamples.)


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


# To quit Docker

If you're in the REPL, exit Python with `exit()` (or `Ctrl-C`).
Now you're back in the Bash shell;
you can futz around there and return to Python with `python3`.

If you're running Jupyter, kill it with `Ctrl-C`.

Now you're in the Bash shell that was hosting Jupyter or the REPL.
Kill it with `exit` (or `Ctrl-D`)
(If it's busy running the iPython server, first close that with Ctrl-C.)
Now you're back in your native OS shell.
The Docker container you were in, `tax-co`, is still running,
but you're no longer looking around inside it.
You can open up a new Bash view into `tax-co`
with `docker exec -it anac bash`.

Stop `tax-co` with `docker stop anac`. Now it's stopped,
but it's still on your system;
you can restart it whenever you want with `docker start -ai anac`.

When the container is stopped,
you can remove it with `docker rm anac`.
You will rarely need to do that -- maybe only when upgrading the image.
It will persist even when you reboot your computer.
