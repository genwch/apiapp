FROM docker.io/library/python:3.7-slim-buster

ENV PYLIB /usr/local/lib/python3.7/site-packages
ENV WORKDIR /usr/src/app
ENV PY_HOST 0.0.0.0
ENV PY_PORT 5000
ENV FLASK_APP apiapp

WORKDIR $WORKDIR
EXPOSE $PY_PORT

## install java
ENV DEBIAN_FRONTEND=noninteractive
RUN mkdir -p /usr/share/man/man1 /usr/share/man/man2
RUN apt-get update && \
apt-get install -y --no-install-recommends \
        openjdk-11-jre

## install depends python lib
COPY ./requirements.txt $WORKDIR
RUN pip install -r requirements.txt

## set hanlp
ENV HANLP_JAR_PATH $WORKDIR/pyhanlp/hanlp-1.7.8.jar
ENV HANLP_STATIC_ROOT $WORKDIR/hanlp
COPY ./hanlp.properties $WORKDIR
RUN sed -i "s|{{HANLP_STATIC_ROOT}}|${HANLP_STATIC_ROOT}|g" $WORKDIR/hanlp.properties
RUN mv $WORKDIR/hanlp.properties $PYLIB/pyhanlp/static

ADD ./$FLASK_APP $WORKDIR/$FLASK_APP
RUN /bin/echo -e "#!/bin/bash\nls $WORKDIR/hanlp\ncat $PYLIB/pyhanlp/static\npython -m flask run --host=$PY_HOST --port=$PY_PORT" > /exec
RUN chmod a+x /exec

USER 1000

CMD ["/exec"]


