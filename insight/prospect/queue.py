from redis import Redis
from rq import Queue


q = Queue(connection=Redis(host="redis"))


def schedule_report(urls, tag, name):
    _types = ["main", "comp1", "comp2"]
    for url, _type in zip(urls, _types):
        q.enqueue("lighthouse.worker", url, tag, f"{name}_{_type}")
