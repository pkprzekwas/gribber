FROM continuumio/miniconda:4.3.11

MAINTAINER "Patryk Przekwas"

RUN conda install -c anaconda flask=0.12.1 -y && \
    conda install -c conda-forge pygrib=2.0.2 -y && \
    conda install -c anaconda pymongo=3.3.0 -y && \
    conda install -c openmdao bson=0.3.3 && \
    conda install -c asmeurer beautiful-soup=4.3.2 && \
    conda install -c anaconda requests=2.13.0

ADD . /gribber

ENV FLASK_APP /gribber/app.py

WORKDIR /gribber
