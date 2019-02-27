FROM python:2.7

RUN apt-get update && apt-get install -y cron

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt
ENV PYTHONPATH /usr/src/app

COPY . /usr/src/app

WORKDIR "/usr/src/app"
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
