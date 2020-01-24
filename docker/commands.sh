# PITFALL: This is not a script.
# It is a collection of one-liners,
# each to be run from the command line individually as needed.

# A trick to quickly edit a Docker-locked file from the host system:
# https://stackoverflow.com/a/26915343

# Build a new image. Do this after making changes to the Dockerfile
# or any of its dependencies.
docker build -f Dockerfile -t           \
  jeffreybbrown/tax.co:new .            \
  | tee logs/"build-log.`date`.txt"

# Change the name of the new image.
docker tag jeffreybbrown/tax.co:new     \
  jeffreybbrown/tax.co:<PUT A BETTER NAME HERE>

# The rest of this script assumes the latest version of the image is
# 2020-01-05.django

docker tag jeffreybbrown/tax.co:new     \
  jeffreybbrown/tax.co:2020-01-05.django

# Upload the new image to DockerHub.
docker push jeffreybbrown/tax.co:2020-01-05.django

# Start a docker container based on the latest image.
docker run --name tax -it		\
  -v /home/jeff/of/tax.co/master:/mnt	\
  -p 8888:8888 -d -h 127.0.0.1		\
  jeffreybbrown/tax.co:2020-01-05.django

# Start a docker container and run jupyter from within it.
docker run --name tax -it		\
  --entrypoint=/root/run-jupyter.sh	\
  -v /home/jeff/of/tax.co:/mnt		\
  -p 8888:8888 -d -h 127.0.0.1		\
  jeffreybbrown/tax.co:2020-01-05.django

# Start a shell within a running container.
# (Once inside, go to the `/mnt` folder to do useful stuff,
# like running `python` or the Makefile.)

