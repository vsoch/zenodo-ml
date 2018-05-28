FROM continuumio/miniconda3

RUN apt-get update && apt-get install -y vim


RUN /opt/conda/bin/conda update conda && \
    /opt/conda/bin/conda install -y pandas numpy && \
    /opt/conda/bin/pip install containertree==0.0.4

RUN mkdir -p /code /data
ADD . /code
