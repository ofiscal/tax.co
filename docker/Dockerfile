# This was originally based on
# https://hub.docker.com/r/continuumio/anaconda3/

FROM debian:latest

RUN echo "2020 01 05" && \
  apt update --fix-missing -y && \
  apt upgrade -y
RUN apt install -y wget bzip2 ca-certificates \
  libglib2.0-0 libxext6 libsm6 libxrender1 \
  make curl grep sed dpkg git mercurial subversion \
  texlive-latex-base texlive-fonts-recommended \
  texlive-fonts-extra texlive-latex-extra texlive-publishers
RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
    /opt/conda/bin/conda clean -afy
RUN /opt/conda/bin/conda install jupyter -y --quiet
RUN conda update --all -y
COPY run-jupyter.sh /root/

RUN pip install django==3.0.2

RUN easy_install xlsx2csv

# make.py, a build tool that's better and easier than make
RUN cd /root                                     && \
    git clone https://github.com/zwegner/make.py && \
    ln -s /root/make.py/make.py /usr/bin/make.py

RUN apt install -y csvtool

RUN apt update && apt upgrade -y && apt install --fix-missing -y           \
  build-essential graphviz cron jq  libapache2-mod-wsgi-py3 ufw apache2 && \
  git clone https://github.com/lindenb/makefile2graph.git               && \
  cd makefile2graph && make && make install

RUN pip install --upgrade                                            \
  csv-diff pydotplus graphviz weightedcalcs yfinance yahoofinancials \
  surbtc django

RUN conda update --all --yes
# RUN conda update -n base conda

RUN apt update -y            && \
    apt install -y haskell-platform

RUN pip install icecream  # a print library, nice for debugging


#### #### #### #### #### #### #### #### #### #### #### ####
#### ####      No more installs, just config      #### ####
#### #### #### #### #### #### #### #### #### #### #### ####

# Somehow these "pam permissions" break crond in a Docker container, per
#   https://stackoverflow.com/a/21928878/916142
# Creating an empty cron.deny file overcomes that, bluntly,
# by permitting every user to use cron.
RUN sed -i '/session    required     pam_loginuid.so/c\#session    required     pam_loginuid.so' /etc/pam.d/cron && \
  touch /etc/cron.deny

COPY python-from-here /usr/bin
RUN chmod +777 /usr/bin/python-from-here

RUN cd /etc/apache2/                                && \
  adduser www-data www-data                         && \
  chown -R www-data:www-data /var/www               && \
  chmod -R g+rw /var/www                            && \
  find / -iname "*apache*" -exec chmod 777 -R {} \; && \
  mkdir /home/appuser /usr/local/apache2            && \
  chmod +777 /home/appuser                          && \
  sed -i "s/Listen 80/Listen 8000/g" /etc/apache2/ports.conf
# PITFALL: www-data is the name of a new group and a new user,
# both created by the adduser command.

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

# So that the container runs without root privileges on the host.
# PITFALL: This might only work when run by a user whose uid is 1000.
# If so, the 1000 below should probably be changed to match the user's id.
RUN groupadd -g 999 appuser               && \
    useradd -r -u 1000 -g appuser appuser && \
    chown appuser /home/appuser
USER appuser

ENV TZ="America/Bogota"

RUN PATH=/root/.local/bin:$PATH
EXPOSE 8888
CMD ["/bin/bash"]
