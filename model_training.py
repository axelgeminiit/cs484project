import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer


def train_model_final(X_train: pd.Series, y_train: pd.Series):
    # parameters used are are the best performing combination from the last execution of train_model_parameters_experimentation function
    pipe = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    ngram_range=(1, 3),
                    min_df=4e-5,
                    max_df=0.9,
                    sublinear_tf=True,
                    strip_accents="unicode",
                    max_features=100_000,
                    dtype=np.float32,
                ),
            ),
            (
                "clf",
                LogisticRegression(
                    solver="liblinear",
                    class_weight="balanced",
                    max_iter=1000,
                    C=2.0,
                    penalty="l2",
                ),
            ),
        ]
    )

    # fit final model on the whole training set
    model = pipe.fit(X_train, y_train)
    print("Training on full training set complete.")

    return model


def train_model_parameters_experimentation(X_train: pd.Series, y_train: pd.Series):
    pipe = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    strip_accents="unicode",
                    dtype=np.float32,
                ),
            ),
            (
                "clf",
                LogisticRegression(
                    solver="liblinear", class_weight="balanced", max_iter=1000
                ),
            ),
        ]
    )

    # parameter variations to test
    param_grid = {
        "clf__penalty": ["l1", "l2", "elasticnet"],
        "clf__C": [0.5, 1.0, 3.0, 5.0],
        "tfidf__min_df": [1e-6, 1e-5, 1e-4, 1e-3],
        "tfidf__max_df": [0.5, 0.7, 0.9, 0.99],
        "tfidf__ngram_range": [(1, 1), (1, 2), (1, 3)],
        "tfidf__max_features": [10000, 100000, 1000000, None],
        "tfidf__sublinear_tf": [False, True],
    }

    # divide training data in 5 folds and cross-validate
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=None)

    # test all parameters and cross-validation combinations
    gs = GridSearchCV(pipe, param_grid, scoring="f1", cv=cv, n_jobs=-1, verbose=1)

    # fit on data
    gs.fit(X_train, y_train)
    print("Grid search complete.")

    # extracting the best model
    best = gs.best_estimator_
    print("Best params:", gs.best_params_)

    return best
