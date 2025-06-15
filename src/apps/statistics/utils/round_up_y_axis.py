import math

def round_up_to_nice_number(value):
    if value >= 0 and value <= 10:
        return 100
    magnitude = 10 ** (len(str(int(value))) - 1)
    return math.ceil(value / magnitude) * magnitude
