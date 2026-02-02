def calculate_iqr(series):
    q1 = series.quantile(0.25)
    mean = series.mean()
    q3 = series.quantile(0.75)
    
    return q1,mean,q3