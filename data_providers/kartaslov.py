from collections import defaultdict

from utils.data import download, is_done, mark_done
import os
import csv

import random

def build(datapath='downloads'):
    datapath = os.path.join(datapath, 'kartaslov')

    fname = 'orfo_and_typos.L1_5.csv'
    fname = os.path.join(datapath, fname)

    if not is_done(datapath):
        print('Downloading orfo_and_typos dataset from kartaslov to {}'.format(fname))
        url = 'https://raw.githubusercontent.com/dkulagin/kartaslov/master/dataset/orfo_and_typos/orfo_and_typos.L1_5.csv'

        download(fname, url)

        mark_done(datapath)

        print('Built')

    return fname


class DataProvider(object):

    @staticmethod
    def _normalize(str):
        return str.replace('ё', 'е')

    def __init__(self, datapath='downloads', seed=None):
        fname = build(datapath)
        self.uniques = defaultdict(list)
        with open(fname, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            next(reader)
            for correct, mistake, weight in reader:
                self.uniques[self._normalize(correct)].append((self._normalize(mistake), weight))

        if seed is None:
            seed = random.randrange(1500000)

        rs = random.getstate()
        random.seed(seed)
        data = list(self.uniques.items())
        random.shuffle(data)
        split = int(len(data) * 0.85)
        self.train = [(c, e, w) for c, errors in data[:split] for e, w in errors]
        random.shuffle(self.train)
        self.test = [(c, e, w) for c, errors in data[split:] for e, w in errors]
        random.shuffle(self.test)
        random.setstate(rs)
