FROM debian:latest

RUN echo "2021 05 11"
RUN apt update --fix-missing -y &&                     \
    apt upgrade -y
RUN apt install -y wget bzip2 ca-certificates          \
      libglib2.0-0 libxext6 libsm6 libxrender1
RUN apt install -y                                     \
      make curl grep sed dpkg git mercurial subversion

# TeX takes almost 2 GB, and I haven't used it in years.
#RUN apt install -y                                     \
#      texlive-latex-base texlive-fonts-recommended     \
#      texlive-fonts-extra texlive-latex-extra texlive-publishers

RUN apt install -y                                     \
      build-essential graphviz cron jq
RUN apt install -y                                     \
      libapache2-mod-wsgi-py3 ufw apache2
RUN apt install -y                                     \
      haskell-platform
RUN apt install -y python3-pip

COPY Anaconda3-2020.11-Linux-x86_64.sh /home/anaconda.sh

RUN /bin/bash /home/anaconda.sh -b -p /opt/conda
RUN rm /home/anaconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
    /opt/conda/bin/conda clean -afy
RUN /opt/conda/bin/conda install jupyter -y --quiet
RUN /opt/conda/bin/conda update --all -y

RUN /opt/conda/bin/conda install pydotplus graphviz django

# PITFALL: If something is available via `conda install`, use that.
RUN pip3 install --upgrade \
  yfinance yahoofinancials weightedcalcs csv-diff surbtc icecream

RUN apt install -y zip unzip

ADD makefile2graph.zip make.py.zip /home/

# makefile2graph is useful for drawing the dependency hierarchy
RUN cd /home && unzip makefile2graph && rm makefile2graph.zip && \
    cd makefile2graph && make && make install

# make.py is a build tool that's better and easier than make
RUN cd /home && unzip make.py && rm make.py.zip && \
    ln -s /home/make.py/make.py /usr/bin/make.py

# PITFALL: Earlier this was installed via easy_install,
# which at least used to be included in the Python `setuptools` pakage.
# If it doesn't work, try installing it that way instead.
RUN apt install xlsx2csv

RUN apt install csvtool


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
