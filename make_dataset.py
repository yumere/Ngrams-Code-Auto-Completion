import multiprocessing as mp
import collections
import re
import os
import pickle
from tqdm import tqdm

from utils import n_grams

splitter = re.compile(r"([\s\W]{1})")
OUTPUT_NAME = "dataset.pkl"


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
    for root, dirs, files in os.walk(r"C:\Users\yumer\Downloads\js_dataset\data"):
        if files:
            files_q += [os.path.join(root, f) for f in files]

    tqdm.write("Total Files: {:,}".format(len(files_q)))
    p = mp.Pool(mp.cpu_count())
    with tqdm(total=len(files_q)) as pbar:
        for _ in p.imap_unordered(myCounter, files_q, 1):
            results.update(_)
            pbar.update()

    with open(OUTPUT_NAME, "wb") as f:
        f.write(pickle.dumps(results))
    p.close()
    p.join()


