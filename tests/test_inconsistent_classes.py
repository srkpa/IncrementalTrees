import unittest
import numpy as np
import pandas as pd
from incremental_trees.trees import StreamingRFC, StreamingEXTC


class Common:
    @classmethod
    def setUpClass(cls):
        data = pd.DataFrame({'a': (1, 2, 3, 4, 5),
                             'b': (1, 2, 3, 4, 5),
                             'c': (1, 2, 3, 4, 5),
                             'target': (1, 1, 2, 2, 3)})

        data = pd.concat((data, data),
                         axis=0).sort_values('target').reset_index(drop=True)

        cls.x = data[[c for c in data if c != 'target']]
        cls.y = data['target']

    def test_none_on_second_call(self):
        # Fit with 2 classes
        self.mod.partial_fit(self.x[0:6], self.y[0:6],
                             classes=np.array([1, 2, 3]))
        self.mod.predict(self.x[0:6])

        # Fit with 3 classes
        self.mod.partial_fit(self.x, self.y)
        self.mod.predict(self.x)

    def test_correct_on_second_call(self):
        # Fit with 2 classes
        self.mod.partial_fit(self.x[0:6], self.y[0:6],
                             classes=np.array([1, 2, 3]))
        self.mod.predict(self.x[0:6])

        # Fit with 3 classes
        self.mod.partial_fit(self.x, self.y,
                             classes=np.array([1, 2, 3]))
        self.mod.predict(self.x)

    def test_incorrect_on_second_call(self):
        """Incorrect on second call - can happen when dask passes classes."""

        # Fit with 3 classes
        self.mod.partial_fit(self.x, self.y,
                             classes=np.array([1, 2, 3]))
        self.mod.predict(self.x)

        # Fit with 2 classes
        self.mod.partial_fit(self.x[0:6], self.y[0:6],
                             classes=np.array([1, 2]))
        self.mod.predict(self.x[0:6])


class TestInconsistentClassesRFC(Common, unittest.TestCase):
    def setUp(self):
        self.mod = StreamingRFC(n_estimators_per_chunk=1,
                                max_n_estimators=np.inf)


class TestInconsistentClassesEXT(Common, unittest.TestCase):
    def setUp(self):
        self.mod = StreamingEXTC(n_estimators_per_chunk=1,
                                 max_n_estimators=np.inf)
