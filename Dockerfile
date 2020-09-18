FROM python:3.8.3-alpine

COPY ./insight_tool /insight_tool

WORKDIR /insight_tool

COPY ./requirements.txt /insight_tool/requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD ["insighter.py"]

ENV PYTHONUNBUFFERED=1
