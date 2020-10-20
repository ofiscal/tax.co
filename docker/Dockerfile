# This was originally based on
# https://hub.docker.com/r/continuumio/anaconda3/

FROM debian:latest

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

RUN echo "2020 01 05" && \
  apt update --fix-missing -y && \
  apt upgrade -y
RUN apt install -y wget bzip2 ca-certificates \
  libglib2.0-0 libxext6 libsm6 libxrender1 \
  make curl grep sed dpkg git mercurial subversion \
  texlive-latex-base texlive-fonts-recommended \
  texlive-fonts-extra texlive-latex-extra texlive-publishers

RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh -O ~/anaconda.sh && \
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
  # This brings pandas to version 0.25.1.
COPY run-jupyter.sh /root/

RUN pip install django==3.0.2

# RUN curl -sSL https://get.haskellstack.org/ | sh
# RUN stack install shake

RUN easy_install xlsx2csv

# make.py, a build tool that's better and easier than make
RUN cd /root                                     && \
    git clone https://github.com/zwegner/make.py && \
    ln -s /root/make.py/make.py /usr/bin/make.py

COPY python-from-here /usr/bin
RUN chmod +777 /usr/bin/python-from-here

RUN apt install -y csvtool

# for make2graph. (bild-essential includes cc, the clang compiler.)
RUN apt install -y build-essential graphviz               && \
  git clone https://github.com/lindenb/makefile2graph.git && \
  cd makefile2graph && make && make install

RUN pip install csv-diff
RUN pip install pydotplus graphviz
RUN pip install weightedcalcs

RUN echo "updating conda: 2020 06 26"
RUN conda update --all --yes
# RUN conda update -n base conda

RUN echo "updating django: 2020 09 25"
RUN pip install django --upgrade

RUN echo "installing apache and ufw, 2020 10 07" && \
    apt update && apt install -y ufw apache2
RUN sed -i "s/Listen 80/Listen 8000/g" /etc/apache2/ports.conf && \
    echo "service apache2 start" > /etc/apache2/start-apache.sh && \
    echo "service apache2 stop" > /etc/apache2/stop-apache.sh && \
    chmod u+x /etc/apache2/st*-apache.sh
RUN echo "installing mod_wsgi for apache, 2020 10 14" && \
    apt update && apt install -y libapache2-mod-wsgi

# I only append this, rather than copy the whole file,
# so that if the apt install of Apache changes the base apache2.conf file,
# I'll receive all those changes.
COPY apache2.conf.append /etc/apache2/
RUN cd /etc/apache2/                       && \
  cat apache2.conf.append >> apache2.conf  && \
  adduser www-data www-data                && \
  chown -R www-data:www-data /var/www      && \
  chmod -R g+rw /var/www                   && \
  find / -iname "*apache*" -exec chmod 777 -R {} \;
# PITFALL: www-data is the name of a new group and a new user,
# both created by the adduser command.

# So that the container runs without root privileges on the host.
# PITFALL: This might only work when run by a user whose uid is 1000.
# If so, the 1000 below should probably be changed to match the user's id.
RUN groupadd -g 999 appuser && \
    useradd -r -u 1000 -g appuser appuser
USER appuser

RUN PATH=/root/.local/bin:$PATH
EXPOSE 8888
CMD ["/bin/bash"]
