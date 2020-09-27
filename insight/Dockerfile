FROM python:3.8.3-alpine

COPY . /insight

WORKDIR /insight

RUN pip install .

ENTRYPOINT [ "python" ]

CMD ["manage.py", "runserver", "0.0.0.0:80"]

ENV PYTHONUNBUFFERED=1
