FROM python:3.8.3-alpine

COPY . /insight

WORKDIR /insight

RUN pip install .

ENTRYPOINT [ "python" ]

ENV PYTHONUNBUFFERED=1
