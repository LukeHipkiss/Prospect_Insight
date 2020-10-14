# Lighthouse worker

### Description:

A sub-project containing lighthouse, google chrome, and a redis queue worker.
The worker collects jobs from redis and wire it to lighthouse in order to generate reports.
It is scalable to cope with load by simply spinning up extra instances.

### Reports:

* View reports by visiting http://localhost/reports

### Dependencies:

There are no external dependencies, but the image uses the following.

* [Python 3.8](https://www.python.org/)
* [Google lighthouse](https://github.com/GoogleChrome/lighthouse)
* [rq](http://python-rq.org/docs/workers/)
* Google Chrome