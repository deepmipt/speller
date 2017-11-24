from data_providers.russian_words import DataProvider

from time import time
from collections import defaultdict

import csv

from math import log
from error_models.candidates import find_candidates

from data_providers.kartaslov import DataProvider as kartaslov

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


# text = '''найдены также остатки мыла которое викинги делали самостоятельно
# география его выступлений достегает индии англии венгрии португалии голландии финляндии
# давольно милый и летом и зимой обогреваемый теплым солнушком
# после моего доклада программа была паб-ресторан-паб после чего такси ловил нетвердо стоя на ногах
# только вот не хочеться мне одной делать такие героическии поступки
# до свидвания'''
# for to_fix in nltk.tokenize.word_tokenize(text):
#     s = time()
#     candidates = find_candidates(words_trie, words, costs, to_fix, k=5)
#     print('{:.3f}s to do "{}"'.format(time() - s, to_fix))
#
#     print(candidates)
#     print()

errors = kartaslov(seed=15)
test = errors.test
times = []
examples = len(test)
seen = 0
one = 0
two = 0
three = 0

for i, (correct, incorrect, _) in enumerate(test):
    s = time()
    candidates = [x[0] for x in find_candidates(words_trie, words, costs, incorrect, k=3)]
    times.append(time() - s)
    seen += 1
    if correct in candidates[:3]:
        three += 1
        if correct in candidates[:2]:
            two += 1
            one += correct in candidates[:1]
    # else:
    #     print(incorrect, candidates, correct)

    if i % 50 == 0:
        print('{} out of {}'.format(i+1, examples))
        print('avg time: {:.3}; 1-best: {:06.2f}%; 2-best: {:06.2f}%; 3-best {:06.2f}%'.format(
            sum(times)/len(times), 100*one/seen, 100*two/seen, 100*three/seen
        ))

print('avg time: {:.3}; 1-best: {:06.2f}%; 2-best: {:06.2f}%; 3-best {:06.2f}%'.format(
    sum(times)/len(times), 100*one/examples, 100*two/examples, 100*three/examples
))
