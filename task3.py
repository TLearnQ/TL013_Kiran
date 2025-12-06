def classify(values):
    avg = sum(values) / len(values)
    if avg >= 80:
        return "Excellent"
    elif avg >= 60:
        return "On Track"
    elif avg >= 40:
        return "At Risk"
    else:
        return "Failing"
