def tribe_score(score: int) -> str:
    """A Tribe defined standard for web performance.
    Expects values between 0 to 100
    low = 0 to 49
    medium = 50 to 90
    high = 90 to 100
    """

    if score > 90:
        return "high"
    elif score > 49:
        return "medium"

    return "low"
