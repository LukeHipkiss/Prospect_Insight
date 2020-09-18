# Prospect Insight

Prospect Insight is a Django application for running lighthouse audits against three target URLs, and then providing a comparison of strictly just the performance scores and the Lab Results data.

## Installation

### Prior to project being dockerised

Install the lighthouse CLI tool through npm.

```bash
npm install -g lighthouse
```

### Post dockerisation
TBC

## Test Usage

The `prospect_insighter.py` script allows the easier method of interaction for backend interaction.

```python
report = LighthouseRunner("https://www.google.com").report

print(report.overall_performance_score)
print(report.data)
print(report.url)
print(report.metric_keys)
print(report.timing("first-contentful-paint"))
```

### Report Object Breakdown

- `report.data` returns the final dictionary. Example below:

```python
EXPECTED_DATA = {
    'URL': 'https://shop.polymer-project.org/',
    'fetch_time': '2020-09-16T13:03:29.810Z',
    'performance_score': 38.0,
    'performance_class': 'red',
    'metrics': {
        'first-contentful-paint': {
            'score': 0.65,
            'timing': 1357.0, 
            'perf_class': 'orange'
        },
        'speed-index': {...},
        'largest-contentful-paint': {...},
        'interactive': {...},
        'total-blocking-time': {...},
        'cumulative-layout-shift': {...}
    }
}
```

- `report.url` - Returns the final url of the lighthouse audit. This is not necessarily the originally provided URL, as any redirects during the lighthouse auditing result in the final URL changing.
- `report.metrics` - Returns the sub metric dictionary.
- `report.overall_performance_score` - Returns the overall audit performance score, derived from the individual weighting and timing of each metric.
- `report.score(METRIC_NAME)` - Returns the performance score of an individual metric.
- `report.timing(METRIC_NAME)` - Returns the metric timing recorded in milliseconds.

## Lighthouse Metrics Captured
The metrics stored alongside their individual score weighting used to find the overall performance score.

- **First Contenful Paint** - 15%
- **Speed Index** - 15%
- **Largest Contentful Paint** - 25%
- **Time to Interactive** - 15%
- **Total Blocking Time** - 25%
- **Cumulative Blocking Time** - 5%

## Dependencies
- Python 3.7
- Django 3.1.1

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
