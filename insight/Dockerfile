FROM python:3.8.3-alpine

# Install sqlite for debugging
RUN apk update \
    && apk add --no-cache \
    sqlite \
    && rm -rf /var/cache/* \
    && mkdir /var/cache/apk

COPY . /insight

WORKDIR /insight

RUN pip install .

ENTRYPOINT [ "python" ]

ENV PYTHONUNBUFFERED=1
