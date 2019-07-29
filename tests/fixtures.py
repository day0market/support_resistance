import os
import pickle

import pandas as pd


def get_quotes_from_fixture():
    pth = os.path.join(os.path.dirname(__file__), 'fixtures', '1H.txt')
    df = pd.read_csv(pth)

    return df


def get_levels_from_fixture():
    pth = os.path.join(os.path.dirname(__file__), 'fixtures', 'levels.pkl')
    with open(pth, 'rb') as f:
        obj = pickle.load(f)

    return obj
