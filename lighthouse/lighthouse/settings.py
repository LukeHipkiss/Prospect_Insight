import os

PERFORMANCE_WEIGHTS = {
    "first-contentful-paint": 15,
    "speed-index": 15,
    "largest-contentful-paint": 25,
    "interactive": 15,
    "total-blocking-time": 25,
    "cumulative-layout-shift": 5,
}

REPORT_PATH = os.getenv("REPORT_PATH", "/home/chrome/reports/")
