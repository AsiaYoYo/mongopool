FROM xtdockerhub.com/baseimage/python:20181109
ADD target/mongopool.tar.gz /XT
RUN tar zxf /XT/mongopool.tar.gz \
    && mv /XT/mongopool -d /XT/MONGO_POOL

#CMD ["/XT/MONGO_POOL/xt-mongopool", "start"; "tail -f /XT/vmlogs/xt-mongopool.log"]
