FROM python:3.7

WORKDIR /opt/tempsensor

#copy requirements first, so that the package installation will be cached
COPY requirements.txt .

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --assume-no --no-install-recommends jackd2

COPY docker-entrypoint.sh .


CMD "./docker-entrypoint.sh"
