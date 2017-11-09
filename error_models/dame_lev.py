def dameraulevenshtein(seq1, seq2):
    """Calculate the Damerau-Levenshtein distance between sequences.

    This distance is the number of additions, deletions, substitutions,
    and transpositions needed to transform the first sequence into the
    second. Although generally used with strings, any sequences of
    comparable objects will work.

    Transpositions are exchanges of *consecutive* characters; all other
    operations are self-explanatory.

    This implementation is O(N*M) time and O(M) space, for N and M the
    lengths of the two sequences.

    >>> dameraulevenshtein('ba', 'abc')
    2
    >>> dameraulevenshtein('fee', 'deed')
    2

    It works with arbitrary sequences too:
    >>> dameraulevenshtein('abcd', ['b', 'a', 'c', 'd', 'e'])
    2
    """
    # codesnippet:D0DE4716-B6E6-4161-9219-2903BF8F547F
    # Conceptually, this is based on a len(seq1) + 1 * len(seq2) + 1 matrix.
    # However, only the current and two previous rows are needed at once,
    # so we only store those.
    oneago = None
    thisrow = list(range(1, len(seq2) + 1)) + [0]
    for x in range(len(seq1)):
        # Python lists wrap around for negative indices, so put the
        # leftmost column at the *end* of the list. This matches with
        # the zero-indexed strings and saves extra calculation.
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
        for y in range(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
            # This block deals with transpositions
            if (x > 0 and y > 0 and seq1[x] == seq2[y - 1]
                and seq1[x-1] == seq2[y] and seq1[x] != seq2[y]):
                thisrow[y] = min(thisrow[y], twoago[y - 2] + 1)
    return thisrow[len(seq2) - 1]


class DameLevErrorModel(object):
    @staticmethod
    def distance_edits(seq1, seq2):
        l1, l2 = len(seq1), len(seq2)
        d = [[(i, ()) for i in range(l2 + 1)]]
        d += [[(i, ())] + [(0, ())]*l2 for i in range(1, l1 + 1)]

        for i in range(1, l1 + 1):
            for j in range(1, l2 + 1):
                edits = [
                    (d[i-1][j][0] + 1, d[i-1][j][1] + ('{}|'.format(seq1[i-1]),)),
                    (d[i][j-1][0] + 1, d[i][j-1][1] + ('|{}'.format(seq2[j-1]),)),
                    (d[i-1][j-1][0] + (seq1[i-1] != seq2[j-1]), d[i-1][j-1][1] + ('{}|{}'.format(seq1[i-1], seq2[j-1]),))
                ]
                if i > 1 and j > 1 and seq1[i-1] == seq2[j-2] and seq1[i-2] == seq2[j-1]:
                    edits.append((d[i-2][j-2][0] + (seq1[i-1] != seq2[j-1]), d[i-2][j-2][1] + ('{}|{}'.format(seq1[i-2:i], seq2[j-2:j]),)))
                d[i][j] = min(edits, key=lambda x: x[0])

        return d[-1][-1]

    def load(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError

    def buid(self, train):
        raise NotImplementedError
