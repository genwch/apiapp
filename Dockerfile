FROM docker.io/library/python:3.7-slim-buster

ENV WORKDIR /usr/src/app
# ENV PYVENV .apivenv
ENV PY_HOST 0.0.0.0
ENV PY_PORT 5000
ENV FLASK_APP apiapp
ENV FLASK_ENV development

WORKDIR $WORKDIR
EXPOSE $PY_PORT

COPY ./requirements.txt $WORKDIR
RUN pip install -r requirements.txt
ADD ./$FLASK_APP $WORKDIR/$FLASK_APP
RUN /bin/echo -e "#!/bin/bash\nls $WORKDIR/$FLASK_APP\npython -m flask run --host=$PY_HOST --port=$PY_PORT" > /exec
RUN chmod a+x /exec

USER 1000

#CMD ["ls", "$WORKDIR", "&&", "python", "-m", "flask", "run", "--host=$PY_HOST", "--port=$PY_PORT"]
CMD ["/exec"]


