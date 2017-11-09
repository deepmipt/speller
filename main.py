from data_providers.kartaslov import DataProvider
from error_models.dame_lev import DameLevErrorModel


def main():
    dp = DataProvider(seed=15)
    for correct, error, weight in dp.train:
        print(correct, error)
        d, ops = DameLevErrorModel.distance_edits(correct, error)
        print(d, ops)
        # if d > 2:
        #     print(correct, error, d)
        print()


if __name__ == '__main__':
    main()
