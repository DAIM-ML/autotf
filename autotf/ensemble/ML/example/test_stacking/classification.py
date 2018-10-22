from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, log_loss
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from ensemble import Stacking
import time
import warnings
warnings.filterwarnings(module='sklearn*', action='ignore', category=DeprecationWarning)

digits = load_digits()
X, y = digits.data, digits.target

# Make train/test split
# As usual in machine learning task we have X_train, y_train, and X_test
X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, test_size=0.2, random_state=0)

models = [
    ExtraTreesClassifier(random_state=0, n_jobs=-1,
                         n_estimators=100, max_depth=3),

    RandomForestClassifier(random_state=0, n_jobs=-1,
                           n_estimators=100, max_depth=3),

    XGBClassifier(random_state=0, n_jobs=-1, learning_rate=0.1,
                  n_estimators=100, max_depth=3)
]

meta_model = XGBClassifier(random_state=0, n_jobs=1, learning_rate=0.1,
                           n_estimators=100, max_depth=3)
start_time = time.time()
ensemble = Stacking(X_train, y_train, X_test, regression=False, bagged_pred=True,
                    needs_proba=False, save_dir=None, metric=accuracy_score,
                    n_folds=4, stratified=True, shuffle=True,
                    random_state=0, verbose=1)

start_time = time.time()
ensemble.add(models, propagate_features=[0, 1, 2, 3])
print ('process(add) took %fs!' % (time.time() - start_time))

start_time = time.time()
y_pred = ensemble.add_meta(meta_model)
print ('process(add_meta) took %fs!' % (time.time() - start_time))

print('Final prediction score: [%.8f]' % accuracy_score(y_test, y_pred))



# '''Compare with the randomforest'''
#
# print("randomforest")
# model = RandomForestClassifier(random_state=0, n_jobs=-1,
#                            n_estimators=200, max_depth=3)
# model.fit(X_train,y_train)
# y_pred = model.predict(X_test)
# print('Final prediction score: [%.8f]' % accuracy_score(y_test, y_pred))