from collections import defaultdict
from math import log, exp
from heapq import heappop, heappush, heappushpop


def get_children(trie, prefix):
    return trie[prefix]


def find_candidates(trie, words, costs, word, k=10, prop_threshold=1e-4):
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
                    (res[-1] + costs[('', c)]) if i else float('-inf'),
                    d[prefix[:-1]][i] + costs[(prefix[-1], '')] if prefix else float('-inf'),
                    (d[prefix[:-1]][i - 1] + (costs[(prefix[-1], c)]))
                    if prefix and i else float('-inf')
                ) if i or prefix else 0)
            d[prefix] = res
            if prefix in words:
                heappushpop(candidates, (res[-1], prefix))
            potential = max(res)
            if potential > threshold:
                heappush(prefixes_heap, (-potential, get_children(trie, prefix)))
    return [(w, exp(score)) for score, w in sorted(candidates, reverse=True)]


def find_candidates_v2(trie, words, costs, word, k=10, prop_threshold=1e-4, window=1):
    threshold = log(prop_threshold)
    word = '⟬{}⟭'.format(word.lower().replace('ё', 'е'))
    word_len = len(word) + 1
    inf = float('-inf')
    d = defaultdict(list)
    d[''] = [0.] + [inf] * (word_len - 1)
    prefixes_heap = [(0, get_children(trie, ''))]
    candidates = [(inf, '')] * k
    while prefixes_heap and -prefixes_heap[0][0] > candidates[0][0]:
        _, prefixes = heappop(prefixes_heap)
        for prefix in prefixes:
            prefix_len = len(prefix)
            res = d[prefix]
            res.append(inf)
            for i in range(1, word_len):
                c_res = [inf]
                for li in range(1, min(prefix_len + 1, window + 2)):
                    for ri in range(1, min(i+1, window + 2)):
                        c_res.append(d[prefix[:prefix_len - li]][i-ri] +
                                     costs[(prefix[prefix_len-li:prefix_len], word[i-ri:i])])
                res.append(max(c_res))
            if prefix in words:
                heappushpop(candidates, (res[-1], prefix))
            potential = max([e for i in range(window+2) for e in d[prefix[:prefix_len-i]]])
            if potential > threshold:
                heappush(prefixes_heap, (-potential, get_children(trie, prefix)))
    return [(w.strip('⟬⟭'), exp(score)) for score, w in sorted(candidates, reverse=True)]
