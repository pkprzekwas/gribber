FROM continuumio/miniconda:4.3.11

MAINTAINER "Patryk Przekwas"

RUN conda install -c anaconda flask=0.12.1 -y && \
    conda install -c conda-forge pygrib=2.0.2 -y && \
    conda install -c anaconda pymongo=3.3.0 -y

ADD . /gribber

ENV FLASK_APP /gribber/app.py

WORKDIR /gribber
