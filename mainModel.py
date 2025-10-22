import kagglehub
import pandas as pd
import re
from pathlib import Path
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import joblib
import matplotlib.pyplot as plt
import numpy as np

path = kagglehub.dataset_download("snap/amazon-fine-food-reviews")

print("Path to dataset files:", path)

# I/O
# pointing to reviews imported

reviews_csv = Path(path) / "Reviews.csv"
assert reviews_csv.exists(), f"Reviews.csv not found in {path}"
file_path = str(reviews_csv)

out_csv = Path("processed_amazon_reviews.csv")
model_pkl = Path("amazon_sentiment_lr_model.joblib")

# Load CSV
df = pd.read_csv(file_path)

# ERROR HANDLING
# ensuring required columns exist
required = {"Text", "Score"}
missing = required - set(df.columns)
assert not missing, f"Missing columns: {missing}"


## CLEANING
# keep only the needed columns and clean basic types
df = df[["Text", "Score"]].dropna()
df["Score"] = pd.to_numeric(df["Score"], errors="coerce")
df = df.dropna(subset=["Score"])
df["Score"] = df["Score"].astype(int)


##### EXPERIMENT
# optional denoising: drop neutral 3-star reviews to make labels crisper
# df = df[df["Score"] != 3]

# binary label: 1 = positive (>=4 stars), 0 = negative (<=2 stars) (or 3 if no denoising)
df["sentiment_label"] = (df["Score"] >= 4).astype(int)

# Optional speed-up: subsample large dataset
#####EXPERIMENT
N = 50_000
if len(df) > N:
    df = df.sample(N).reset_index(drop=True)
print(f"Training rows: {len(df):,}")

text_col = "Text"
assert text_col in df.columns, f"Missing column: {text_col}"
df[text_col] = df[text_col].fillna("")

# Clean

_url = re.compile(r"http\S+|www\.\S+")
_mention_hashtag = re.compile(r"[@#]\w+")
_nonletters = re.compile(r"[^a-zA-Z\s']")


# TODO: cleaning seems to not be working rn, at least for links...
def clean_text(s: str) -> str:
    s = _url.sub("", s)
    s = _mention_hashtag.sub("", s)
    s = _nonletters.sub(" ", s)
    s = re.sub(r"\s{2,}", " ", s).strip().lower()
    return s


print("Cleaning text...")
df["cleaned_text"] = df[text_col].apply(clean_text)
print("Finished cleaning.")


X = df["cleaned_text"]
y = df["sentiment_label"].astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

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

param_grid = {"clf__penalty": ["l2"], "clf__C": [0.5, 1.0, 2.0]}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
gs = GridSearchCV(pipe, param_grid, scoring="f1", cv=cv, n_jobs=-1, verbose=0)
print("Vectorizing + GridSearchCV...")
gs.fit(X_train, y_train)
print("Grid search complete.")

best = gs.best_estimator_
y_pred = best.predict(X_test)
y_prob = best.predict_proba(X_test)[:, 1]

print("Best params:", gs.best_params_)
print("\nClassification report:\n", classification_report(y_test, y_pred, digits=3))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))
try:
    print("ROC-AUC:", roc_auc_score(y_test, y_prob))
except Exception:
    pass

# persist artifacts
df.to_csv(out_csv, index=False)
joblib.dump(best, model_pkl)
print(f"Saved: {out_csv}")
print(f"Saved model: {model_pkl}")

# quick bar chart
pd.Series(y_pred, name="pred").value_counts().sort_index().plot(
    kind="bar", title="Predicted sentiment counts"
)
plt.xlabel("Class")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("predicted_sentiment_counts.png", dpi=200, bbox_inches="tight")
print("Saved plot: predicted_sentiment_counts.png")
