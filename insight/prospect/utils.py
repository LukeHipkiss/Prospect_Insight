PERFORMANCE_WEIGHTS = {
    "first-contentful-paint": 15,
    "speed-index": 15,
    "largest-contentful-paint": 25,
    "interactive": 15,
    "total-blocking-time": 25,
    "cumulative-layout-shift": 5,
}


def tribe_score(score: int) -> str:
    """A Tribe defined standard for web performance.
    Expects values between 0 to 100
    low = 0 to 49
    medium = 50 to 90
    high = 90 to 100
    """
    assert 0 <= score <= 100

    if score > 90:
        return "success"
    elif score > 49:
        return "warning"

    return "danger"
