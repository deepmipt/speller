import csv
from typing import Dict, Tuple

import os

from data_providers.kartaslov import DataProvider
from error_models.dame_lev import DameLevErrorModel
from collections import Counter


def save(probs: Dict[Tuple[str, str], float]):
    fname = 'target/probs_ru.tsv'
    os.makedirs(os.path.dirname(fname), exist_ok=True)
    with open(fname, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        for (w, s), p in probs.items():
            writer.writerow([w, s, p])


def main():
    dp = DataProvider(seed=15)
    changes = []
    entries = []
    n = len(dp.train)
    for i, (correct, error, weight) in enumerate(dp.train):
        d, ops = DameLevErrorModel.distance_edits(correct, error)
        # print(correct, error)
        # print(d, ops)
        if d <= 2:
            entries += [op[0] for op in ops]
            changes += [op for op in ops if op[0] != op[1]]

        if i % 1500 == 0:
            print('{} out of {}'.format(i, n))
        # if d > 2:
        #     print(correct, error, d)
    e_count = Counter(entries)
    c_count = Counter(changes)
    probs = {(w, s): c/e_count[w] for (w, s), c in c_count.items()}
    save(probs)


if __name__ == '__main__':
    main()
