FROM docker.io/library/python:3.7-slim-buster
# FROM docker.io/library/python:alpine

ENV WORKDIR /usr/src/app
ENV PY_HOST 0.0.0.0
ENV PY_PORT 5000
ENV FLASK_APP apiapp

WORKDIR $WORKDIR
EXPOSE $PY_PORT

RUN apt-get update && \
apt-get install -y --no-install-recommends \
        openjdk-8-jre

COPY ./requirements.txt $WORKDIR
RUN pip install -r requirements.txt
ADD ./$FLASK_APP $WORKDIR/$FLASK_APP
RUN /bin/echo -e "#!/bin/bash\npython -m flask run --host=$PY_HOST --port=$PY_PORT" > /exec
RUN chmod a+x /exec

USER 1000

CMD ["/exec"]


