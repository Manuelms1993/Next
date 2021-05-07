import math

def calculateTemperature(n, i, center):

    if (i == 0):
        return 0.1

    # Rigth side
    if ((n - 1) / 2 < i):
        rs = 1 - center
        x = (rs) / (n - i) * math.pow(rs, (n - i) / (n)) + center
        return x

    elif ((n - 1) / 2 == i):
        return center

    # Left
    else:
        ls = center
        x = ls - ((ls) / (i+1)) * math.pow(ls, ((n)/2 - (i/2)) / ((n)/2))
        return x