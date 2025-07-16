def calculate_iqr(series):
    """Calculates mean and interquantile range"""
    q1 = series.quantile(0.25)
    mean = series.mean()
    q3 = series.quantile(0.75)

    q1 = round(q1, 1)
    mean = round(mean, 1)
    q3 = round(q3, 1)

    return q1, mean, q3
