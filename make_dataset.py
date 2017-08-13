from tqdm import tqdm, trange
import os
import re
import pickle

from collections import Counter
from multiprocessing import Process, Queue

from utils import n_grams

OUTPUT_NAME = "dataset.pkl"
WORKER_SIZE = 16

splitter = re.compile(r"([\s\W]{1})")

files_q = []
data_q = Queue()
dataset = Counter()


class Error(object):
    DONE = False

    def __init__(self, done):
        self.DONE = done


def process(q, file_list):
    for file_name in file_list:
        splitted = []
        with open(file_name, "rt", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line:
                    splitted += [i.strip() for i in splitter.split(line) if i.strip()]

        q.put(n_grams(splitted))

    q.put(Error(done=True))


if __name__ == '__main__':
    for root, dirs, files in os.walk("C:\\Users\\yumere\\Downloads\\js_dataset\\data"):
        if files:
            files_q += [os.path.join(root, f) for f in files]

    print("Total Files: {:,}".format(len(files_q)))

    workers = []
    for i in range(0, len(files_q), int(len(files_q) / WORKER_SIZE)+1):
        workers.append(Process(target=process, args=(data_q, files_q[i: i+int(len(files_q) / WORKER_SIZE)], )))

    for worker in workers:
        worker.start()

    done_cnt = 0
    pbar = tqdm(total=len(files_q))
    while True:
        try:
            d = data_q.get(block=True)
            if type(d) == Error:
                if d.DONE:
                    done_cnt += 1
                    if done_cnt == WORKER_SIZE:
                        break
            else:
                dataset.update(d)
                pbar.update()

        except Exception as e:
            print(e)

    for worker in workers:
        worker.join()

    if OUTPUT_NAME:
        with open(OUTPUT_NAME, "wb") as f:
            f.write(pickle.dumps(dataset))
