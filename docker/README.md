PITFALL: For run-jupyter to work, the native (as opposed to docker) port must be 8888.
  Running the container using one of the commands in commands.txt ensures this.
  The 8888 requirement is a consequence of the fixed port in the run-jupyter.sh script.

The docker container here is based on the one at
  https://hub.docker.com/r/continuumio/anaconda3/
