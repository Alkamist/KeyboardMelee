def normalize(value):
    if value > 0.0:
        return 1.0
    elif value < 0.0:
        return -1.0
    else:
        return 0.0
