from utils.data import download, is_done, mark_done
import os
import random


def build(datapath='downloads'):
    datapath = os.path.join(datapath, 'russian_words')

    fname = 'russian.txt'
    fname = os.path.join(datapath, fname)

    if not is_done(datapath):
        print('Downloading a list of russian words to {}'.format(fname))
        url = 'https://github.com/danakt/russian-words/raw/master/russian.txt'

        download(fname, url)

        with open(fname, encoding='cp1251') as f:
            data = f.readlines()

        with open(fname, 'w') as f:
            f.writelines(data)

        random.shuffle(data)
        with open(os.path.join(datapath, 'shortlist.txt'), 'w') as f:
            f.writelines(data[:len(data)//5])

        mark_done(datapath)

        print('Built')

    return datapath


class DataProvider(object):

    @staticmethod
    def _normalize(w):
        return w.strip().replace('ё', 'е').lower()

    def __init__(self, datapath='downloads', short=False):
        fname = os.path.join(build(datapath), 'shortlist.txt' if short else 'russian.txt')

        with open(fname) as f:
            self.data = {self._normalize(w) for w in f}
