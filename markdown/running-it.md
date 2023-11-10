# PITFALL: Don't let Windows file formats thwart you.

If you use Windows,
and you edit any file that's used in the build process,
be it code (probably `.py`) or data (probably `.csv`)
or even something else,
run `dos2unix` on it.
This is needed because the Docker container,
from which everything is (typically) built,
uses Linux, not Windows -- even if you run it in Windows.

# Install dependencies

Install Git.
(For more information, see [Some software we use](Some-software-we-use.md).)

Install jq.
(For more information, see [Some software we use](Some-software-we-use.md).

Install Docker.
(For more information, see [Some software we use](Some-software-we-use.md).
Docker is not strictly necessary,
but it's a really [good idea](Why-to-use-Docker.md).

Get the latest Docker image of tax.co,
by running `docker pull ofiscal/tax.co:latest`.
(Or you could build it yourself from [the Dockerfile](../docker/Dockerfile).)
This will probably take a long time.

Each time you use that image,
Docker will create a virtual Ubuntu Linux system.
By default that system is disconnected from your native system;
actions in the Docker container cannot affect the rest of your system.
However, you can "mount" a native folder to a folder in the Docker system,
which causes them to share their contents;
you can read and write to the file from either system.
(Once Dockmer has control of a folder,
you might need to use `sudo` to modify it from outside of Docker.)

# Get `tax.co`

`tax.co` is the code that runs the microsimulation.

Get it by running this:

`git clone https://github.com/ofiscal/tax.co`.

(In the example below, I have located that folder at
`/home/username/tax.co`.
You might want to put it somewhere else;
if you do, then change those paths accordingly.)

# Get and configure `tax.co.web`

This is the code for the webpage,
but you'll need it even if you don't run the webpage.
Clone (get) it, and set up its submodules, by running:

```
git clone https://github.com/ofiscal/tax.co.web
cd tax.co.web
git submodule init
git submodule update
cd system_specific
git checkout master
```

Now customize the `base_system` paths in the file `paths.json`.
(using any text editor).
Leave the `docker` paths defined there unchanged.

Then from the root of `tax.co.web`,
run `./commands/offline/create.sh`.
That creates, and starts services in, the Docker container.

## Why system_specific is a submodule

Since the paths to `tax.co` and `tax.co.web`
can be different on different systems,
the proper configuration of `paths.json`
depends on the system it's running on.
By making `system_specific` a submodule,
one can use different branches of `system_specific`,
customized for different systems,
even while they all use the same branch of `tax.co.web`.

## PITFALL: Customizing `paths.json` and using `jq` might be hard on Windows

The two `create.sh` scripts both require `jq`,
which I've never installed on Windows.
They also require a scary-looking nested evaluation idiom
that I've never translated into Windows.

Should that prove difficult,
an alternative approach is to rewrite `create.sh`,
incorporating the paths you want to use directly into it,
and delete the lines involving `jq`.
That would involve replacing each of the following expressions:

```
  $base_system_tax_co
  $base_system_tax_co_web
  $docker_apache
  $docker_commands
  $docker_django
  $docker_paths
  $docker_system_specific
  $docker_tax_co
```

with whatever `paths.json` defines
(after having edited `paths.json` as described above).

# Set up and use `tax.co`

## Download and build the raw ENPH data

See this repo's [ENPH README](../data/enph-2017/README.md) for how.

## Configure `config.json`

You only need to do this if you won't be specifying the config file in the next step.

In `config/`, copy `config.MODEL.json` to `config.json`.
Change the subsample from `1000` to `1`
if you want to use the full data set.

Each user's email address is hashed to determine the name of the folder
where that user's data will be stored.
`tax.co` begins set up for the email address
`example_user@somewhere.net`, which corresponds to the folder
`u1e71cf39e330262a44422cc73e2e046a`.

If you want to use a different folder,
you can do so by creating it,
populating it similarly to the example folder,
and then changing the email address in `config/config.json`.
To see what folder name corresponds to another email address,
run the following from any python shell:
```
import hashlib
( "u" +
  hashlib.md5 (
    "example_user@somewhere.net" . encode () )
  . hexdigest () )
```

## Run the microsimulation

After that, enter the docker:
  `docker exec -it tax.co.web bash`

The docker container is where it runs.
(If the following commands don't work, they might be out of date.
The most up-to-date commands for running it can be found
in the header comment to `python/run-makefile.py`.)

If you don't want to specify the config file,
run this from `/mnt/tax_co`:
  `PYTHONPATH="." python3 python/run-makefile.py`

If you do (which is easier),
run this from `/mnt/tax_co`:
  `PYTHONPATH="." python3 python/run-makefile.py users/example/config/config.json`

If that path doesn't work (because Windows doesn't like symlinks?),
try this:
  `PYTHONPATH="." python3 python/run-makefile.py users/u1e71cf39e330262a44422cc73e2e046a/config/config.json`

# Once you've (maybe) gotten it to run

## To change tax rates

Edit the `users/symlinks/quien/config` folder.

## To disable testing

Go to `python/run-makefile.sh`,
and comment out the word `tests`.

## To be sure that it's running

From another window into the docker container,
run `ps -ef | grep python`

## To see if it's done

If `users/symlinks/quien/logs/make.stderr.out` is empty,
no errors happened.
(Or it might have warnings without errors; that's okay too.)

But it might still be running.
So I guess look in `users/symlinks/quien/data/`.

## To see the results

go to `users/symlinks/quien/`.
There you'll see these folders:
```
jeff@jbb-dell:quien$ ls -1
config
data
logs
logs.zip
test
```

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
with `docker exec -it tax.co.web bash`.

Stop `tax-co` with `docker stop tax.co.web`. Now it's stopped,
but it's still on your system;
you can restart it whenever you want with `docker start -ai tax.co.web`.

When the container is stopped,
you can remove it with `docker rm tax.co.web`.
You will rarely need to do that -- maybe only when upgrading the image.
It will persist even when you reboot your computer.
