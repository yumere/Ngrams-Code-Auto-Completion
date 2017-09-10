def n_grams(data, n_size=3):
    d = []
    for i in range(len(data) - n_size - 2):
        d.append((tuple(data[i: i + n_size - 1]), data[i + n_size - 1]))
    return d
