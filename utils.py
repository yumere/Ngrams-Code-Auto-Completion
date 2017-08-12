def n_grams(data, n_size=3):
    d = []
    for i in range(len(data) - n_size - 1):
        d.append((tuple(data[i: i + n_size]), data[i + n_size]))
    return d
