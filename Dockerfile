FROM docker.io/library/python:3.7-slim-buster
# FROM docker.io/library/python:alpine

ENV WORKDIR /usr/src/app
ENV PY_HOST 0.0.0.0
ENV PY_PORT 5000
ENV FLASK_APP apiapp

WORKDIR $WORKDIR
EXPOSE $PY_PORT

ENV DEBIAN_FRONTEND=noninteractive

RUN mkdir -p /usr/share/man/man1 /usr/share/man/man2

RUN apt-get update && \
apt-get install -y --no-install-recommends \
        openjdk-11-jre

COPY ./requirements.txt $WORKDIR
RUN pip install -r requirements.txt
ADD ./$FLASK_APP $WORKDIR/$FLASK_APP
RUN /bin/echo -e "#!/bin/bash\npython -m flask run --host=$PY_HOST --port=$PY_PORT" > /exec
RUN chmod a+x /exec

USER 1000

CMD ["/exec"]


