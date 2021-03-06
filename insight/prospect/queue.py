from redis import Redis
from rq import Queue


q = Queue(connection=Redis(host="redis"))


def schedule_report(urls, device, tag, prospect):
    _types = ["main", "comp1", "comp2"]

    main = q.enqueue("lighthouse.worker", urls[0], tag, _types[0], prospect, device)
    comp1 = q.enqueue("lighthouse.worker", urls[1], tag, _types[1], prospect, device)
    comp2 = q.enqueue("lighthouse.worker", urls[2], tag, _types[2], prospect, device)

    return main.id, comp1.id, comp2.id
