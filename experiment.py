import joblib
import numpy as np
import pandas as pd

model = joblib.load("data/amazon_sentiment_lr_model.joblib")

test_cases = [
    # Sarcasm & Irony
    "Oh great, another product that broke after 2 days. Just what I needed!",
    "Sure, if you enjoy wasting money, this is perfect for you.",
    "Best purchase ever... if you love disappointment.",
    # Mixed Sentiments (Positive start, negative end)
    "The product looks beautiful and arrived quickly, but it stopped working after a week.",
    "Great customer service, but the product itself is complete garbage.",
    "I love the design and concept, however the quality is terrible and it broke immediately.",
    # Mixed Sentiments (Negative start, positive end)
    "I was skeptical at first and the setup was confusing, but once I figured it out, this is amazing!",
    "Terrible packaging and slow shipping, but the product itself exceeded my expectations.",
    "Initially disappointed with the size, but after using it I'm actually impressed.",
    # Backhanded Compliments
    "It works... barely.",
    "For the price, I guess it's okay, but don't expect much.",
    "It's not the worst thing I've bought.",
    # Context-Dependent Negatives (double negatives = positive)
    "This product is not bad.",
    "I wouldn't say I'm unhappy with it.",
    "Can't complain really.",
    # Subtle Disappointment
    "It's fine. Does what it says. Nothing special.",
    "Adequate for basic needs I suppose.",
    "Well, it arrived and it turns on.",
    # Expectation vs Reality
    "Based on the reviews I expected more, but it's just average.",
    "The pictures made it look so much better than it actually is.",
    "Five stars for the idea, one star for the execution.",
    # Conditional Positives (positive with major caveats)
    "Works great if you don't mind the noise and smell.",
    "Perfect product assuming you have the time to fix all its issues.",
    "Love it except for the fact that it doesn't do the main thing it's supposed to do.",
    # Comparative Disappointment
    "My previous model was so much better than this.",
    "The knockoff version I bought for half the price works better.",
    "Every competitor's product I've tried outperforms this.",
    # Neutral with Hidden Sentiment
    "Interesting experience with this product.",
    "Well, it certainly is a product.",
    "I have thoughts about this purchase.",
]


while 1:
    text_input = str(input(("enter a review:")))
    if text_input == "tc":
        for i, review in enumerate(test_cases, 1):
            result = model.predict([review])
            probabilities = model.predict_proba([review])[0]
            confidence = np.max(probabilities)

            print(f"\n{i}. Review: {review}")
            print(f"   Prediction: {result[0]} | Confidence: {confidence:.2%}")
            print(f"   Probabilities: {probabilities}")

    if text_input == "tf":
        vectorizer = model.named_steps["tfidf"]
        classifier = model.named_steps["clf"]

        feature_names = vectorizer.get_feature_names_out()
        coefficients = classifier.coef_[0]

        feature_weights = pd.DataFrame(
            {"feature": feature_names, "weight": coefficients}
        )

        feature_weights_sorted = feature_weights.sort_values("weight", ascending=False)

        print("\n pos features:")
        for idx, row in feature_weights_sorted.head(20).iterrows():
            print(f"{row['feature']:30s} | {row['weight']:+.4f}")

        print("\n neg features:")
        for idx, row in feature_weights_sorted.tail(20).iterrows():
            print(f"{row['feature']:30s} | {row['weight']:+.4f}")
        print()

    result = model.predict([text_input])
    probabilities = model.predict_proba([text_input])

    print(f"\nPrediction: {result[0]}")
    print(f"Confidence scores: {probabilities[0]}")
    print(f"Confidence: {np.max(probabilities[0]):.2%}")
    print("\n\n")
