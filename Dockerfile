FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install libpq-dev -y