FROM python:3.10.11-slim-buster

# setup cron
RUN apt-get update && apt-get -y install cron gettext-base

ARG HOURS_TO_SYNC
ENV HOURS_TO_SYNC=${HOURS_TO_SYNC}

WORKDIR /app

ADD requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install wheel
RUN pip install -r requirements.txt

ADD . .
RUN envsubst '$HOURS_TO_SYNC' < cron-schedule > /etc/cron.d/reddit-sync
RUN chmod 0644 /etc/cron.d/reddit-sync

CMD tail -f /dev/null