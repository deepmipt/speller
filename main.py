from data_providers.russian_words import DataProvider

from time import time
from collections import defaultdict

import csv

from math import log, exp


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

candidates = {}


def calc_lev(d, prefixes, w):
    w = '•' + w.lower().replace('ё', 'е')
    while prefixes:
        new_prefixes = set()
        for prefix in prefixes:
            res = []
            for i, c in enumerate(w):
                c = c.replace('•', '')
                res.append(max(
                    (res[-1] + costs[(prefix[-1] if prefix else '', c)]) if i else float('-inf'),
                    d[prefix[:-1]][i] + costs[(prefix[-1], '')] if prefix else float('-inf'),
                    (d[prefix[:-1]][i - 1] + (costs[(prefix[-1], c)] if prefix[-1] != c else 0))
                    if prefix and i else float('-inf')
                ) if i or prefix else 0)
            d[prefix] = res
            if prefix in words_trie:
                candidates[prefix] = exp(res[-1])
            if max(res) > -6.91:  # log(0.001)
                new_prefixes.update({x[:len(prefix) + 1] for x in words_trie.keys(prefix) if len(x) > len(prefix)})
        prefixes = new_prefixes


to_fix = 'кндидатская'
s = time()
distances = {}
calc_lev(distances, {''}, to_fix)
print('Time to do everything else', time() - s)

candidates_short = sorted(candidates.items(), key=lambda x: x[1], reverse=True)[:5]

print(to_fix)
print(candidates_short)
