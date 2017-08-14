import sqlite3
import multiprocessing as mp
from tqdm import tqdm


CHUNK_SIZE = 1000


def count_true(inputs):
    k, v, c = inputs
    conn = sqlite3.connect("dataset.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM train_data where key=?", (k, ))
    res = cursor.fetchone()

    if res and v == res[1]:
        # tqdm.write("TRAIN: {} {} {}".format(k, v, c))
        # tqdm.write("TEST: {} {} {}".format(res[0], res[1], res[2]))
        # tqdm.write("")
        return (c, c)

    return (c, 0)

if __name__ == '__main__':
    conn = sqlite3.connect("dataset.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM test_data")
    row_cnt, = cursor.fetchone()
    tqdm.write("Row Amount: {:,}".format(row_cnt))

    cursor.execute("SELECT * FROM test_data")
    testset = cursor.fetchall()
    # testset = cursor.fetchmany(100)

    tqdm.write("CPU Count: {:,}".format(mp.cpu_count()))
    p = mp.Pool(mp.cpu_count() * 2)

    total_count = 0
    correct_count = 0
    with tqdm(total=row_cnt) as pbar:
        for i, (t, c) in enumerate(p.imap_unordered(count_true, testset, chunksize=CHUNK_SIZE)):
            total_count += t
            correct_count += c
            pbar.update()

            if i % 100000 == 0:
                tqdm.write("Total Count: {:,}".format(total_count))
                tqdm.write("Correct Count : {:,}".format(correct_count))

    tqdm.write("Total Count: {:,}".format(total_count))
    tqdm.write("Correct Count : {:,}".format(correct_count))

