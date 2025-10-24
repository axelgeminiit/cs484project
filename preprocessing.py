### PREPROCESSING FILE

from pathlib import Path
import pandas as pd
import re


def loadData(path: Path) -> pd.DataFrame:
    reviews_csv = Path(path) / "Reviews.csv"
    assert reviews_csv.exists(), f"Reviews.csv not found in {path}"
    file_path = str(reviews_csv)

    # Load CSV
    df = pd.read_csv(file_path)

    # ERROR HANDLING
    # ensuring required columns exist
    required = {"Text", "Score"}
    missing = required - set(df.columns)
    assert not missing, f"Missing columns: {missing}"

    return df


def createSavePaths(path: Path):
    out_original_csv = Path("data/input_amazon_reviews.csv")
    out_csv = Path("data/processed_amazon_reviews.csv")
    model_pkl = Path("data/amazon_sentiment_lr_model.joblib")

    return out_original_csv, out_csv, model_pkl


def cleanText(s: str) -> str:
    # TODO: cleaning seems to not be working for now, at least for links...
    # Clean
    _url = re.compile(r"http\S+|www\.\S+")
    _mention_hashtag = re.compile(r"[@#]\w+")
    _nonletters = re.compile(r"[^a-zA-Z\s']")

    s = _url.sub("", s)
    s = _mention_hashtag.sub("", s)
    s = _nonletters.sub(" ", s)
    s = re.sub(r"\s{2,}", " ", s)
    s = s.strip()
    s = s.lower()
    return s


def prepareDataset(
    df: pd.DataFrame, drop3Stars: bool = False, subSample: int = None
) -> tuple[pd.Series, pd.Series]:
    ## CLEANING
    # keep only the needed columns and clean basic types
    df = df[["Text", "Score"]].dropna()
    df["Score"] = pd.to_numeric(df["Score"], errors="coerce")
    df = df.dropna(subset=["Score"])
    df["Score"] = df["Score"].astype(int)

    # optional denoising: drop neutral 3-star reviews to make labels crisper
    if drop3Stars:
        df = df[df["Score"] != 3]

    # binary label: 1 = positive (>=4 stars), 0 = negative (<=2 stars) (or 3 if no denoising)
    df["sentiment_label"] = (df["Score"] >= 4).astype(int)

    # Optional speed-up: subsample large dataset
    if subSample is not None:
        if len(df) > subSample:
            df = df.sample(subSample).reset_index(drop=True)
        print(f"Training rows: {len(df):,}")

    text_col = "Text"
    assert text_col in df.columns, f"Missing column: {text_col}"
    df[text_col] = df[text_col].fillna("")

    df["cleaned_text"] = df[text_col].apply(cleanText)

    X = df["cleaned_text"]
    y = df["sentiment_label"].astype(int)

    return X, y
