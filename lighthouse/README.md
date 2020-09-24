# Lighthouse as a Service

### Description:

A flask server with a single endpoint which triggers google lighthouse.

### Usage:

* Spin the container up by running `docker-compose up` from the root of the project.
* Then send a post request as per below:
```bash
curl -X POST  -H 'Content-Type: application/json' -d '{"args": ["https://www.google.com", "/home/chrome/reports/test.json"]}' http://localhost:4000/lighthouse 
```
 
 Or alternatively do the same with python `requests`.
 
### Dependencies:

There are no external dependencies, but the image uses the following.

* [Python 3.8](https://www.python.org/)
    * [Click](https://click.palletsprojects.com/en/7.x/)
    * [Flask](https://flask.palletsprojects.com/en/1.1.x/)
    * [flask_shell2http](https://flask-shell2http.readthedocs.io/en/stable/Quickstart.html)
* [Google lighthouse](https://github.com/GoogleChrome/lighthouse)
* Google Chrome