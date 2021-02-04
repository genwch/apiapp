# FROM docker.io/library/python:3.7-slim-buster
FROM docker.io/library/python:alpine

ENV WORKDIR /usr/src/app
ENV PY_HOST 0.0.0.0
ENV PY_PORT 5000
ENV FLASK_APP apiapp

WORKDIR $WORKDIR
EXPOSE $PY_PORT

### 2. Get Java via the package manager
RUN apk update \
&& apk upgrade \
&& apk add --no-cache bash \
&& apk add --no-cache --virtual=build-dependencies unzip \
&& apk add --no-cache curl \
&& apk add --no-cache openjdk8-jre
ENV JAVA_HOME="/usr/lib/jvm/java-1.8-openjdk"

COPY ./requirements.txt $WORKDIR
RUN pip install -r requirements.txt
ADD ./$FLASK_APP $WORKDIR/$FLASK_APP
RUN /bin/echo -e "#!/bin/bash\npython -m flask run --host=$PY_HOST --port=$PY_PORT" > /exec
RUN chmod a+x /exec

USER 1000

CMD ["/exec"]


