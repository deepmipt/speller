import csv
from typing import Dict, Tuple

import os

from data_providers.kartaslov import DataProvider
from error_models.dame_lev import DameLevErrorModel
from collections import Counter


def save(probs: Dict[Tuple[str, str], Tuple[float, float]], incorrect_prior=1, correct_prior=19):
    fname = 'target/probs_ru.tsv'
    os.makedirs(os.path.dirname(fname), exist_ok=True)
    with open(fname, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        for (w, s), (c, e) in probs.items():
            c = c + (incorrect_prior if w != s else correct_prior)
            e = e + incorrect_prior + correct_prior
            p = c / e
            writer.writerow([w, s, p, c, e])


def main():
    dp = DataProvider(seed=15)
    changes = []
    entries = []
    n = len(dp.train)
    window = 2
    for i, (correct, error, weight) in enumerate(dp.train):
        correct = '⟬{}⟭'.format(correct)
        error = '⟬{}⟭'.format(error)
        d, ops = DameLevErrorModel.distance_edits(correct, error)
        # print(correct, error)
        # print(d, ops)
        if d <= 2:
            w_ops = set()
            for pos in range(len(ops)):
                # if ops[i][0] == ops[i][1]:
                #     continue
                left, right = list(zip(*ops))
                for l in range(pos, max(0, pos - window) - 1, -1):
                    for r in range(pos + 1, min(len(ops), l + 2 + window)):
                        w_ops.add(((''.join(left[l:r]), ''.join(right[l:r])), l, r))
            ops = [x[0] for x in w_ops]

            entries += [op[0] for op in ops]
            changes += [op for op in ops]

        if i % 1500 == 0:
            print('{} out of {}'.format(i, n))
        # if d > 2:
        #     print(correct, error, d)
    e_count = Counter(entries)
    c_count = Counter(changes)
    probs = {(w, s): (c, e_count[w]) for (w, s), c in c_count.items()}
    save(probs)


if __name__ == '__main__':
    main()
