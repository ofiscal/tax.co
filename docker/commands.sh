# PITFALL: This is not a script.
# It is a collection of one-liners,
# each to be run from the command line individually as needed.

# A trick to quickly edit a Docker-locked file from the host system:
# https://stackoverflow.com/a/26915343

# Start a docker container based on the latest image.
docker run --name tax -it             \
  -v /home/jeff/of/tax.co/master:/mnt \
  -p 8888:8888 -d -h 127.0.0.1        \
  ofiscal/tax.co:2020-10-16.apache-access

# Start a docker container and run jupyter from within it.
docker run --name tax -it             \
  --entrypoint=/root/run-jupyter.sh   \
  -v /home/jeff/of/tax.co/master:/mnt \
  -p 8888:8888 -d -h 127.0.0.1	      \
  ofiscal/tax.co:2020-10-16.apache-access

# Start a shell within a running container.
# (Once inside, go to the `/mnt` folder to do useful stuff,
# like running `python` or the Makefile.)
docker exec      -it tax bash
docker exec -u 0 -it tax bash # as root

# Build a new image. Do this after making changes to the Dockerfile
# or any of its dependencies.
docker build -f Dockerfile -t \
  ofiscal/tax.co:new .        \
  | tee logs/"build-log.`date`.txt"

# Change the name of the new image.
docker tag ofiscal/tax.co:new     \
  ofiscal/tax.co:latest
docker tag ofiscal/tax.co:new     \
  ofiscal/tax.co:2020-10-16.apache-access
docker rmi ofiscal/tax.co:new

# Upload to DockerHub.
docker push ofiscal/tax.co:latest
docker push ofiscal/tax.co:2020-10-16.apache-access

