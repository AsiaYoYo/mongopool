FROM xtdockerhub.com/baseimage/python:20181109
RUN mkdir -p /XT/MONGO_POOL
ADD mongopool.tar.gz /XT/MONGO_POOL
WORKDIR /XT/MONGO_POOL
RUN tar -zxf mongopool.tar.gz
