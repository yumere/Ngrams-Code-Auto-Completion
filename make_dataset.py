import multiprocessing as mp
import collections
import re
import os
import pickle
import gc
from tqdm import tqdm

from utils import n_grams

splitter = re.compile(r"([\s\W]{1})")
WORKER_SIZE = None or mp.cpu_count()
CHUNK_SIZE = 500
SAVE_INTERVAL = 5000
OUTPUT_NAME = "dataset.pkl"

DATA_URL = "/home/yumere/Downloads/data"


def myCounter(filename):
    splitted = []
    try:
        with open(filename, "rt", encoding="utf-8") as f:
            try:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if line:
                        splitted += [i.strip() for i in splitter.split(line) if i.strip()]

                r = n_grams(splitted)
                r = collections.Counter(r)
                return r
            except Exception as e:
                pass
    except FileNotFoundError as e:
        pass

if __name__ == '__main__':
    files_q = []
    results = collections.Counter()
    for root, dirs, files in os.walk(DATA_URL):
        if files:
            files_q += [os.path.join(root, f) for f in files]

    tqdm.write("Total Files: {:,}".format(len(files_q)))
    tqdm.write("Chunk Size: {}".format(CHUNK_SIZE))
    tqdm.write("CPU Count: {:,}".format(mp.cpu_count()))

    p = mp.Pool(mp.cpu_count())
    with tqdm(total=len(files_q)) as pbar:
        for i, _ in enumerate(p.imap_unordered(myCounter, files_q, CHUNK_SIZE)):
            results.update(_)
            pbar.update()

            if i is not 0 and i % SAVE_INTERVAL == 0:
                with open("results/3gram/{}_{}".format(i, OUTPUT_NAME), "wb") as f:
                    f.write(pickle.dumps(results))

                results = collections.Counter()
                gc.collect()

    with open("results/3gram/" + OUTPUT_NAME, "wb") as f:
        f.write(pickle.dumps(results))
    p.close()
    p.join()


