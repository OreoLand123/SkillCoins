FROM python:3.10.7-slim

COPY . /root

WORKDIR /root

RUN pip install flask gunicorn flask-sqlalchemy psycopg2-binary