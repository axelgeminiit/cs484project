import kagglehub
import pandas as pd
import re
from pathlib import Path

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


from textblob import TextBlob
import matplotlib.pyplot as plt


def polarity(s: str) -> float:
    return TextBlob(s).sentiment.polarity


# thresholds: neutral band reduces false positives on short texts
def to_label(p: float) -> str:
    if p > 0.05:
        return "Positive"
    if p < -0.05:
        return "Negative"
    return "Neutral"


df["polarity"] = df["cleaned_text"].apply(polarity)
df["sentiment"] = df["polarity"].apply(to_label)

df.to_csv(out_csv, index=False)
print(f"Saved: {out_csv}")

ax = (
    df["sentiment"]
    .value_counts()
    .reindex(["Negative", "Neutral", "Positive"])
    .plot(kind="bar", title="Sentiment Distribution")
)
ax.set_xlabel("Sentiment")
ax.set_ylabel("Number of comments")
plt.tight_layout()
plt.savefig("unsupervised_sentiment_counts.png", dpi=200, bbox_inches="tight")
print("Saved plot: unsupervised_sentiment_counts.png")
