FROM debian:latest

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

RUN echo "Tuesday, May 28, 2019. New version of Pandas available."

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    apt-utils git mercurial subversion

RUN wget --quiet https://repo.continuum.io/archive/Anaconda3-5.1.0-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

RUN apt-get install -y curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean


# here the Dockerfile starts deviating from continuum/anaconda3
RUN apt install -y make && \
    conda update -n base conda && \
    /opt/conda/bin/conda install jupyter -y --quiet

RUN apt install -y texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra
RUN apt install -y texlive-publishers

RUN apt update && curl -sSL https://get.haskellstack.org/ | sh
RUN stack install shake
RUN apt update && apt upgrade -y
RUN conda update --prefix /opt/conda anaconda --yes
RUN apt install python3-pip -y && \
    pip3 install --upgrade pip

COPY run-jupyter.sh /root/
RUN PATH=/root/.local/bin:$PATH
EXPOSE 8888
ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD ["/bin/bash"]
