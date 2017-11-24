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