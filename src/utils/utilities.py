import math

def calculateTemperature():
    n = 20
    center = 0.7
    for i in range(n):

        if (i == 0):
            print(0.1)
            continue

        # Rigth side
        if ((n - 1) / 2 <= i):
            rs = 1 - center
            x = (rs) / (n - i) * math.pow(rs, (n - i) / (n)) + center
            print(str(i) + " --> " + str(x))

        else:
            ls = center
            x = ls - ((ls) / i) * math.pow(ls, (n/2 - i) / (n/2))
            print(str(i) + " --> " + str(x))