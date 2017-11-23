from data_providers.russian_words import DataProvider

from time import time
from collections import defaultdict

import csv

from math import log, exp
from heapq import heappushpop, heappop, heappush


s = time()
ds = DataProvider(short=False)

words = ds.data
words_trie = ds.words_trie
print('Time spent creating the words trie', time() - s)

alphabet = {c for w in words for c in w}
costs = defaultdict(lambda: log(1e-8))
costs[('', '')] = log(1)
for c in alphabet:
    costs[(c, c)] = log(1)

with open('target/probs_ru.tsv') as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    for l, r, p in reader:
        costs[(l, r)] = log(float(p))


def get_children(trie, prefix):
    return trie[prefix]


def calc_lev(trie, word, k=10, threshold=-11.5):
    d = {}
    prefixes_heap = [(0, {''})]
    candidates = [(float('-inf'), '') for _ in range(k)]
    word = '•' + word.lower().replace('ё', 'е')
    while prefixes_heap and -prefixes_heap[0][0] > candidates[0][0]:
        _, prefixes = heappop(prefixes_heap)
        for prefix in prefixes:
            res = []
            for i, c in enumerate(word):
                c = c.replace('•', '')
                res.append(max(
                    (res[-1] + costs[(prefix[-1] if prefix else '', c)]) if i else float('-inf'),
                    d[prefix[:-1]][i] + costs[(prefix[-1], '')] if prefix else float('-inf'),
                    (d[prefix[:-1]][i - 1] + (costs[(prefix[-1], c)] if prefix[-1] != c else 0))
                    if prefix and i else float('-inf')
                ) if i or prefix else 0)
            d[prefix] = res
            if prefix in words:
                heappushpop(candidates, (res[-1], prefix))
            potential = max(res)
            if potential > threshold:
                heappush(prefixes_heap, (-potential, get_children(trie, prefix)))
    return [(w, exp(score)) for score, w in sorted(candidates, reverse=True)]


text = '''есть у вас оформленый и подписаный мною заказ
вот в инете откапал такую интеерсную статейку предлагаю вашему внимани
я на всю жизнь запомню свое первое купание в зимнем ледяном енисее
думаем что не ошибемся если скажем что выставка лучшие фотографии россии 2012 станет одним из самых значимых событий
в культурной жизни перми и ее жителей'''
for to_fix in text.split():
    s = time()
    candidates = calc_lev(words_trie, to_fix, k=10)
    print('{:.3f}s to do "{}"'.format(time() - s, to_fix))

    print(candidates)
    print()
