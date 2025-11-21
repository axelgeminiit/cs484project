import kagglehub
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.model_selection import train_test_split
from transformers import pipeline
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import joblib
import preprocessing as pr

SUBSAMPLE = 50000
DROP3STARS = True


# our custom TF-IDF model
custom_model = joblib.load("data/amazon_sentiment_lr_model.joblib")

# BERT-based model
bert_model = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    device=-1,  # Use CPU; change to 0 for GPU
)

# VADER rule-based sentiment analysis, specialy tuned on social media
vader = SentimentIntensityAnalyzer()


def predict_custom(texts):
    predictions = custom_model.predict(texts)
    return predictions


def predict_bert(texts):
    results = bert_model(list(texts), truncation=True, max_length=512)
    predictions = [1 if r["label"] == "POSITIVE" else 0 for r in results]
    return np.array(predictions)


def predict_vader(texts):
    predictions = []
    for text in texts:
        score = vader.polarity_scores(str(text))
        predictions.append(1 if score["compound"] > 0.05 else 0)
    return np.array(predictions)


def predict_textblob(texts):
    predictions = []
    for text in texts:
        blob = TextBlob(str(text))
        # polarity: > 0 is positive, <= 0 is negative
        predictions.append(1 if blob.sentiment.polarity > 0 else 0)
    return np.array(predictions)


def compare_all(X_test: pd.Series, y_test: pd.Series):
    print("=" * 40)
    print("COMPARING ALL MODELS")
    print("=" * 40)

    models = {
        "our model": predict_custom,
        "BERT (DistilBERT)": predict_bert,
        "VADER": predict_vader,
        "TextBlob": predict_textblob,
    }

    results = {}

    ## custom model
    predictions = predict_custom(X_test)
    accuracy = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)

    results["custom"] = {
        "accuracy": accuracy,
        "f1_score": f1,
        "predictions": predictions,
    }

    ## BERT model
    predictions = predict_bert(X_test)
    accuracy = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)

    results["BERT"] = {
        "accuracy": accuracy,
        "f1_score": f1,
        "predictions": predictions,
    }

    ## vader model
    predictions = predict_vader(X_test)
    accuracy = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)

    results["VADER"] = {
        "accuracy": accuracy,
        "f1_score": f1,
        "predictions": predictions,
    }

    ## textblob model
    predictions = predict_textblob(X_test)
    accuracy = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)

    results["textblob"] = {
        "accuracy": accuracy,
        "f1_score": f1,
        "predictions": predictions,
    }

    # print results
    print("\n" + "=" * 40)
    print("SUMMARY")
    print("=" * 40)
    print(f"{'Model':<40} {'Accuracy':>12} {'F1 Score':>12}")
    print("-" * 40)

    for model_name, result in results.items():
        print(
            f"{model_name:<40} {result['accuracy']:>12.4f} {result['f1_score']:>12.4f}"
        )

    return results


def main():
    # Download dataset
    path = kagglehub.dataset_download("snap/amazon-fine-food-reviews")
    print("Path to dataset files:", path)

    # Load dataset
    df = pr.loadData(path)
    out_original_csv, out_csv, model_pkl = pr.createSavePaths(path)

    # Save input data into a dedicated csv file for comparison
    df.to_csv(out_original_csv, index=False)
    print(f"Saved: {out_csv}")

    # Preprocess the dataset
    X, y = pr.prepareDataset(df, drop3Stars=DROP3STARS, subSample=SUBSAMPLE)

    # Train the model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

    compare_all(X_test, y_test)


main()
