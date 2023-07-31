FROM debian:latest

RUN echo "2023 07 26"
RUN apt update --fix-missing -y && \
    apt upgrade -y

# PITFALL: These are massive. Don't reorder them
# or join them into one RUN command.
RUN apt install -y texlive
RUN apt install -y texlive-latex-extra

RUN apt install -y wget bzip2 ca-certificates \
      libglib2.0-0 libxext6 libsm6 libxrender1

RUN apt install -y \
      make curl grep sed dpkg git mercurial subversion

RUN apt install -y \
      build-essential graphviz cron jq
RUN apt install -y \
      libapache2-mod-wsgi-py3 ufw apache2
RUN apt install -y \
      haskell-platform
RUN apt install -y \
      python3-pip
RUN apt install -y \
      zip unzip

RUN pip3 install --upgrade \
  yfinance yahoofinancials
RUN pip3 install --upgrade \
  weightedcalcs csv-diff
RUN pip3 install --upgrade \
  icecream
RUN pip3 install --upgrade \
  pydotplus
RUN pip3 install --upgrade \
  graphviz
RUN pip3 install --upgrade \
  django-stubs

RUN pip3 install --upgrade ipython

RUN pip3 install --upgrade scipy

RUN pip3 install --upgrade django

ADD makefile2graph.zip make.py.zip /home/

# makefile2graph is useful for drawing the dependency hierarchy
RUN cd /home &&              \
    unzip makefile2graph &&  \
    rm makefile2graph.zip && \
    cd makefile2graph &&     \
    make && make install

# make.py is a build tool that's better and easier than make
RUN cd /home && unzip make.py && rm make.py.zip && \
    ln -s /home/make.py/make.py /usr/bin/make.py

# PITFALL: Earlier this was installed via easy_install,
# which at least used to be included in the Python `setuptools` pakage.
# If it doesn't work, try installing it that way instead.
RUN apt install xlsx2csv csvtool

RUN pip3 install --upgrade coconut mypy coconut[mypy] \
    pandas-stubs types-requests
RUN pip3 install --upgrade pandas
RUN pip3 install --upgrade matplotlib
RUN pip3 install --upgrade openpyxl
RUN pip3 install --upgrade filelock
RUN echo "coconut \$1 \$1.py -l -t 3.7 --mypy" > /usr/bin/myCoconut && \
    chmod +x                                     /usr/bin/myCoconut


#### #### #### #### #### #### #### #### #### #### #### ####
#### ####      No more installs, just config      #### ####
#### #### #### #### #### #### #### #### #### #### #### ####

# Somehow these "pam permissions" break crond in a Docker container, per
#   https://stackoverflow.com/a/21928878/916142
# Creating an empty cron.deny file overcomes that, bluntly,
# by permitting every user to use cron.
RUN sed -i '/session    required     pam_loginuid.so/c\#session    required     pam_loginuid.so' /etc/pam.d/cron && \
  touch /etc/cron.deny

COPY run-jupyter.sh /root/
COPY python-from-here /usr/bin
RUN chmod +777 /usr/bin/python-from-here

# So that the container runs without root privileges on the host.
# PITFALL: While the names "jeff" and "users" aren't important,
# the IDs are. This is designed to match my system,
# where "jeff" = 1000 and "users" = 100.
RUN groupmod -g 100 users            && \
    useradd -r -u 1000 -g users jeff && \
    mkdir /home/jeff                 && \
    chmod +777 /home/jeff            && \
    chown jeff /home/jeff

RUN cd /etc/apache2/                                && \
  adduser www-data www-data                         && \
  chown -R www-data:www-data /var/www               && \
  chmod -R g+rw /var/www                            && \
  find / -iname "*apache*" -exec chmod 777 -R {} \; && \
  sed -i "s/Listen 80/Listen 8000/g" /etc/apache2/ports.conf
# PITFALL: www-data is the name of a new group and a new user,
# both created by the adduser command.

# This prevents a weird error that recently (2021 June) started happening
# when pasting multiple lines of text into a shell.
# PITFALL: This needs to be in the home folder of both users.
# `root` (done here) and `jeff` (done below).
RUN echo "set enable-bracketed-paste off" >> /root/.inputrc
RUN echo "set enable-bracketed-paste off" >> /home/jeff/.inputrc

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV TZ="America/Bogota"
USER jeff

RUN PATH=/root/.local/bin:$PATH
EXPOSE 8888
CMD ["/bin/bash"]
