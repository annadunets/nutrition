FROM python:3.8.3-slim

WORKDIR /usr/src/my_app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2 \
    && pip install pika==1.3.1

COPY . .

CMD ["python", "./receive.py"]