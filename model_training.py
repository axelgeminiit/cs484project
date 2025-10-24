import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer


def train_model(X_train: pd.Series, y_train: pd.Series):
    pipe = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    ngram_range=(1, 2),
                    min_df=5,
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
                    solver="liblinear", class_weight="balanced", max_iter=1000
                ),
            ),
        ]
    )

    # parameter variations to test
    param_grid = {"clf__penalty": ["l2"], "clf__C": [0.5, 1.0, 2.0]}

    # Cross-validation strategy : divide training data in 5 folds and cross-validate
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=None)

    # test all parameters and cross-validation combinations: 3 parameter values and 5 folds = 15 model fits
    gs = GridSearchCV(pipe, param_grid, scoring="f1", cv=cv, n_jobs=-1, verbose=0)

    # fitting on data
    gs.fit(X_train, y_train)
    print("Grid search complete.")

    # extracting the best performing model
    best = gs.best_estimator_
    print("Best params:", gs.best_params_)

    return best
