from matrix import matrix
import math


def create_dataset(time_series, time_step, predict_span):
    rows = len(time_series) - time_step - 1
    cols = time_step
    x_train = matrix(rows, cols)
    y_train = matrix(rows, 1)
    x_last = matrix(1, cols)

    for i in range(rows):
        for j in range(cols):
            x_train[i, j] = time_series[i+j]
        y_train[i, 0] = sum(time_series[i+cols:i+cols+1])

    for i in range(cols):
        x_last[0, i] = time_series[i-cols]

    return x_train, y_train, x_last


def avg_filter(time_series):
    avg = 0
    cnt = 0
    for i in range(len(time_series)):
        if time_series[i] != 0:
            avg += time_series[i]
            cnt += 1
    avg /= cnt

    for i in range(len(time_series)):
        if time_series[i] > avg:
            time_series[i] = avg

    return time_series


def get_pow(time_series, n):
    for i in range(len(time_series)):
        time_series[i] = abs(time_series[i]) ** n
    return time_series
