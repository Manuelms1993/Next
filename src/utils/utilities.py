import math


def calculateTemperature():
    n = 10
    center = 0.3
    for i in range(n):

        # Rigth side
        if ((n - i) / 2 <= i):

            rs = 1 - center
            x = (rs) / (n - i) * math.pow(rs, (n - i) / (n)) + center
            print(str(i) + " --> " + str(x))

        else:

            ls = center
            x = center - (ls) / ((n - i) * -math.pow(ls, (n - i) / (n)))
            print(str(i) + " --> " + str(x))