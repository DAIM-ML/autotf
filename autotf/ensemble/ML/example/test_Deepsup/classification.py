from sklearn.ensemble.forest import ExtraTreesClassifier as ExtremeRandomizedTrees
from sklearn.neighbors import KNeighborsClassifier as kNearestNeighbors
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble.forest import RandomForestClassifier

from xgboost.sklearn import XGBClassifier
import numpy as np
from sklearn import datasets
from ensemble.Deep_super_learner import DeepSuperLearner
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_digits
import warnings
warnings.filterwarnings(module='sklearn*', action='ignore', category=DeprecationWarning)

# Prepare data
digits = load_digits()
X, y = digits.data, digits.target
X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, test_size=0.2, random_state=0)

if __name__ == '__main__':
    ERT_learner = ExtremeRandomizedTrees(n_estimators=200, max_depth=None, max_features=1)
    kNN_learner = kNearestNeighbors(n_neighbors=11)
    LR_learner = LogisticRegression()
    RFC_learner = RandomForestClassifier(n_estimators=200, max_depth=None)
    XGB_learner = XGBClassifier(n_estimators=200, max_depth=3, learning_rate=1.)
    Base_learners = {'ExtremeRandomizedTrees': ERT_learner, 'kNearestNeighbors': kNN_learner,
                     'LogisticRegression': LR_learner,
                     'RandomForestClassifier': RFC_learner, 'XGBClassifier': XGB_learner}

    # np.random.seed(100)
    # X, y = datasets.make_classification(n_samples=1000, n_features=12,
    #                                     n_informative=2, n_redundant=6)
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    DSL_learner = DeepSuperLearner(Base_learners)
    DSL_learner.fit(X_train, y_train, max_iterations=20, sample_weight=None)
    DSL_learner.get_precision_recall(X_test, y_test, show_graphs=True)