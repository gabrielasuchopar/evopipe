import numpy as np
import warnings
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
from sklearn.metrics import make_scorer


class TrainTestEvaluator:

    def __init__(self, preproc, classif):
        self.pr = np.array(preproc)
        self.cl = np.array(classif)
        self.tr_x = None
        self.tr_y = None
        self.te_x = None
        self.te_y = None

    def fit(self, train_X, train_Y):
        self.tr_x = train_X
        self.tr_y = train_Y

    def score(self, individual, n_prepro, test_X, test_Y):
        prep = self.pr[individual[:n_prepro]]
        clf = self.cl[individual[n_prepro:]]
        pipe = make_pipeline(*prep, *clf)
        try:
            pipe.fit(self.tr_x, self.tr_y)
            return (pipe.score(test_X, test_Y),)
        # todo better error handling
        except:
            return 0.0,


class DefaultEvaluator:
    def fit(self, train_X, train_Y):
        self._trX = train_X
        self._trY = train_Y
        self._teX = None
        self._teY = None

    def score(self, pipe, scorer=None):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')

                # scoring=None is the default value for the parameter
                scores = cross_val_score(pipe, self._trX, self._trY, cv=10, scoring=scorer)
                return np.mean(scores), np.var(scores)
        # todo better error handling
        except:
            return None

    def fit_test(self, test_X, test_Y):
        self._teX = test_X
        self._teY = test_Y

    def train_test_score(self, pipe, scorer=None):
        if self._teX is None or self._teY is None:
            return None

        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')

                pipe.fit(self._trX, self._trY)

                if scorer is not None:
                    scorer(pipe, self._teX, self._teY)
                return pipe.score(self._teX, self._teY)

        # todo better error handling
        except:
            return None

