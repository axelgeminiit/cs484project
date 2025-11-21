from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score


def dump_model_stats(y_test: pd.Series, y_pred: pd.Series, y_prob: pd.Series):
    print("\nClassification report:\n", classification_report(y_test, y_pred, digits=3))
    print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))
    print("ROC-AUC:", roc_auc_score(y_test, y_prob))


def make_model_graph(y_pred: pd.Series):
    pd.Series(y_pred, name="pred").value_counts().sort_index().plot(
        kind="bar", title="Predicted sentiment counts"
    )
    plt.xlabel("Class")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("data/predicted_sentiment_counts.png", dpi=200, bbox_inches="tight")
    print("Saved plot: predicted_sentiment_counts.png")


def print_missclassified_test_cases(
    X_test: pd.Series, y_test: pd.Series, y_pred: pd.Series
):
    misclassified_mask = y_pred != y_test
    misclassified_indices = np.where(misclassified_mask)[0]

    total_errors = len(misclassified_indices)

    print(f"MISCLASSIFIED TEST CASES ({total_errors} errors:)")

    for i, idx in enumerate(misclassified_indices, 1):
        print(f"\n{i}. Review: {X_test.iloc[idx]}")
        print(f"   True: {y_test.iloc[idx]} | Predicted: {y_pred[idx]}")

    print("\n" + "=" * 100)
