FROM python:3.9-bullseye

RUN set -ex \
    apt-get update \

ENV LIBRARY_PATH=/lib:/usr/lib \
    PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

WORKDIR /code

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 8801

CMD ["/code/docker-entrypoint.sh"]
