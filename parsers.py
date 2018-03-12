days_of_month = [31, 30, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def time2val(time):
    year = time[0:4]
    month = time[5:7]
    day = time[8:10]

    # Convertion
    year = 365 * (int(year) - 2000)
    month = int(month)
    day = int(day)

    # To value
    value = 0
    month -= 1
    for i in range(0, month):
        value += days_of_month[i + 1]
    value += (day - 1) + year

    return value