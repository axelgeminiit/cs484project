import streamlit as st
import joblib
import pandas as pd
from pathlib import Path
import preprocessing as pr


st.set_page_config(
    page_title="Amazon Review Sentiment Analyzer",
    page_icon="⭐",
    layout="wide"
)


st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF9900;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .prediction-box {
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    .positive {
        background-color: #d4edda;
        color: #155724;
        border: 2px solid #c3e6cb;
    }
    .negative {
        background-color: #f8d7da;
        color: #721c24;
        border: 2px solid #f5c6cb;
    }
    </style>
""", unsafe_allow_html=True)

#model
@st.cache_resource
def load_model():
    model_path = Path("data/amazon_sentiment_lr_model.joblib")
    if not model_path.exists():
        return None
    return joblib.load(model_path)

# Main app
def main():
    # Header
    st.markdown('<div class="main-header">⭐ Amazon Review Sentiment Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Sentiment Analysis for Product Reviews</div>', unsafe_allow_html=True)

    model = load_model()

    if model is None:
        st.error("⚠️ Model not found! Please train the model first by running `python main.py`")
        st.info("After training, the model will be saved to `data/amazon_sentiment_lr_model.joblib`")
        return

    # Sidebar with info
    with st.sidebar:
        st.header("📊 About the Project")
        st.write("""
        This sentiment analyzer uses **Logistic Regression** with **TF-IDF** features to classify Amazon Fine Food Reviews.

        **Model Details:**
        - Dataset: Amazon Fine Food Reviews
        - Algorithm: Logistic Regression
        - Features: TF-IDF (1-2 grams)
        - Classes: Positive (≥4 stars) / Negative (≤2 stars)
        """)

        st.header("🎯 How to Use")
        st.write("""
        1. Enter a product review in the text box
        2. Click 'Analyze Sentiment'
        3. View the prediction and confidence score
        """)

        st.header("💡 Example Reviews")
        if st.button("Try Positive Example"):
            st.session_state['example_text'] = "This product is absolutely amazing! Best purchase ever. The quality is outstanding and it exceeded all my expectations. Highly recommend!"

        if st.button("Try Negative Example"):
            st.session_state['example_text'] = "Terrible product. Complete waste of money. It broke after one use and the quality is awful. Very disappointed with this purchase."

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📝 Enter a Product Review")

        # Text input
        default_text = st.session_state.get('example_text', '')
        review_text = st.text_area(
            "Type or paste a review here:",
            value=default_text,
            height=150,
            placeholder="Example: This product is amazing! Best purchase I've made..."
        )

        # Clear example after use
        if 'example_text' in st.session_state and review_text == st.session_state['example_text']:
            del st.session_state['example_text']

        analyze_button = st.button("🔍 Analyze Sentiment", type="primary", use_container_width=True)

        if analyze_button and review_text.strip():
            # Preprocess 
            cleaned_text = pr.cleanText(review_text)

            # prediction
            prediction = model.predict([cleaned_text])[0]
            probability = model.predict_proba([cleaned_text])[0]

            # Display results
            st.subheader("🎯 Analysis Results")

            if prediction == 1:
                sentiment = "POSITIVE"
                confidence = probability[1] * 100
                emoji = "😊"
                css_class = "positive"
                stars = "⭐⭐⭐⭐⭐"
            else:
                sentiment = "NEGATIVE"
                confidence = probability[0] * 100
                emoji = "😞"
                css_class = "negative"
                stars = "⭐"

            st.markdown(
                f'<div class="prediction-box {css_class}">{emoji} {sentiment} {emoji}<br>{stars}</div>',
                unsafe_allow_html=True
            )

            # Confidence meter
            st.write("### Confidence Score")
            st.progress(confidence / 100)
            st.write(f"**{confidence:.1f}%** confident in this prediction")

            # Show cleaned text in expander
            with st.expander("🔧 View Preprocessed Text"):
                st.write("**Original Text:**")
                st.write(review_text)
                st.write("**Cleaned Text (used for prediction):**")
                st.write(cleaned_text if cleaned_text else "_[empty after cleaning]_")

        elif analyze_button:
            st.warning("⚠️ Please enter a review text to analyze!")

    with col2:
        st.subheader("📈 Quick Stats")

        # Display model info boxes
        st.metric("Model Type", "Logistic Regression")
        st.metric("Feature Method", "TF-IDF")
        st.metric("N-gram Range", "(1, 2)")

        # Check if evaluation graph exists
        graph_path = Path("data/predicted_sentiment_counts.png")
        if graph_path.exists():
            st.subheader("📊 Model Performance")
            st.image(str(graph_path), use_container_width=True)

if __name__ == "__main__":
    main()
