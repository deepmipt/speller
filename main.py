from data_providers.russian_words import DataProvider

from time import time
from collections import defaultdict

import csv

from math import log, exp
from heapq import heappushpop, heappop, heappush

import nltk
nltk.download('punkt')


s = time()
ds = DataProvider(compreno=True)

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


def find_candidates(trie, word, k=10, prop_threshold=1e-4):
    threshold = log(prop_threshold)
    d = {}
    prefixes_heap = [(0, {''})]
    candidates = [(float('-inf'), '') for _ in range(k)]
    word = word.lower().replace('ё', 'е')
    word_len = len(word) + 1
    while prefixes_heap and -prefixes_heap[0][0] > candidates[0][0]:
        _, prefixes = heappop(prefixes_heap)
        for prefix in prefixes:
            res = []
            for i in range(word_len):
                c = word[i-1:i]
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


text = '''найдены также остатки мыла которое викинги делали самостоятельно
география его выступлений достегает индии англии венгрии португалии голландии финляндии
давольно милый и летом и зимой обогреваемый теплым солнушком
после моего доклада программа была паб-ресторан-паб после чего такси ловил нетвердо стоя на ногах
только вот не хочеться мне одной делать такие героическии поступки
до свидвания'''
for to_fix in nltk.tokenize.word_tokenize(text):
    s = time()
    candidates = find_candidates(words_trie, to_fix, k=5)
    print('{:.3f}s to do "{}"'.format(time() - s, to_fix))

    print(candidates)
    print()
