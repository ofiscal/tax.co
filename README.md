A model of the Colombian tax system.


# Why to use Docker to run this code

This is written in Python using Numpy, Scipy and Pandas. The libraries used will surely expand. So far they are all included in a vanilla install of Anaconda; however, that might not always be true. If you want to work more than necessary, you could stay on top of all those new libraries yourself. However, we will be maintaining a Docker image of Anaconda with every required library already installed.


# How to run this code in Docker

Install Docker.

Get the continuumio/anaconda3 Docker image of Anaconda, by running 'docker pull continuumio/anaconda3'.

Download this Git repository, with 'git clone https://github.com/JeffreyBenjaminBrown/tax.co'.

In the example below, I have located that folder at '/home/jeff/javeriana/tax.co'. You'll want to put it somewhere else; change those paths accordingly.

Each time you run it, Docker will create a virtual Linux system. By default that system is disconnected from your native system. However, you can "mount" a native folder to a folder in the Docker system, which causes them to share their contents; you can read and write to the file from either system.

Run the Docker image, mounting your native tax.co folder to the /mnt folder in the Docker image: 'sudo docker run --name anac -itd -v /home/jeff/javeriana/tax.co:/mnt continuumio/anaconda3'. This starts a Docker container named 'anac'. (A Docker "container" is an environment running the code in a Docker "image".)

Open a Bash view into that Docker container: 'sudo docker exec -it anac bash'.

From within the Bash view, change directories to the one where the code is mounted: 'cd /mnt'.


## Next comes a choice

You can run a Python REPL in the Docker container. This gives you the advantage of a searchable command history. However, graphics cannot be viewed from within it; they must be output to a file, which can then be viewed from a (native) application.

Alternatively, you can run iPython. This lets you run and edit code in a .ipynb document, which can include graphics, from a browser (e.g. Firefox, Chrome).

I typically open two Bash views into the same Docker container, and run iPython in one and a Python REPL in the other. When I want to explore graphics I use the browser; the rest of the time I use the REPL.


## How to launch a Python REPL from within a Bash view of a Docker container

Run 'python3'. Now you're in a Python shell, which is running within the Bash shell, which is running within the Docker container.

Finally, you can execute the code: 'exec(open("vat.py").read())'.


## How to launch iPython from within a Bash view of a Docker container

Run this: 'opt/conda/bin/conda install jupyter -y --quiet && /opt/conda/bin/jupyter notebook --notebook-dir=/mnt --ip='*' --port=8888 --no-browser --allow-root'.

It will process for a little while, and then display a URL you can visit to interact with iPython.


## How to quit

Exit Python with 'exit()'. Now you're back in the Bash shell; you can futz around there and return to Python with 'python3'.

Exit the Bash shell with 'exit'. (If it's busy running the iPython server, first close that with Ctrl-C.) Now you're back in your native OS's shell. The Docker container named 'anac' is still running; you can open up a new Bash view into it with 'sudo docker exec -it anac bash'.

Quit 'anac' with 'sudo docker stop anac'. Now it's stopped, but it's still on your system; you can restart it whenever you want with 'sudo docker start -ai anac'.

When the container is stopped, you can remove it with 'sudo docker rm anac'. You don't really ever need to do that.
