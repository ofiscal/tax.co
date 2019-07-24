FROM debian:latest

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

RUN echo "2019 07 23" && \
  apt update --fix-missing -y && \
  apt upgrade -y
RUN apt install -y wget bzip2 ca-certificates \
  libglib2.0-0 libxext6 libsm6 libxrender1 \
  make curl grep sed dpkg git mercurial subversion \
  texlive-latex-base texlive-fonts-recommended \
  texlive-fonts-extra texlive-latex-extra texlive-publishers

RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
    /opt/conda/bin/conda clean -afy
RUN /opt/conda/bin/conda install jupyter -y --quiet
COPY run-jupyter.sh /root/

RUN curl -sSL https://get.haskellstack.org/ | sh
RUN stack install shake

RUN easy_install xlsx2csv

# RUN conda update --all --yes
# RUN conda update -n base conda

RUN PATH=/root/.local/bin:$PATH
EXPOSE 8888
CMD ["/bin/bash"]
