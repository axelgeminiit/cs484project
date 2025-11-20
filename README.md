# Amazon Review Sentiment Analyzer

A machine learning project that analyzes sentiment in Amazon Fine Food Reviews using Logistic Regression with TF-IDF features.

## Project Overview

This project classifies product reviews as either **positive** (≥4 stars) or **negative** (≤2 stars) using natural language processing and machine learning techniques.

### Key Features
- **Dataset**: Amazon Fine Food Reviews from Kaggle
- **Algorithm**: Logistic Regression with L2 regularization
- **Features**: TF-IDF vectorization with 1-2 grams
- **Interactive Demo**: Streamlit web application

## Installation

1. Clone the repository
```bash
git clone <your-repo-url>
cd cs484project
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Train the Model

Run the training script to download the dataset, preprocess it, and train the model:

```bash
python main.py
```

This will:
- Download the Amazon Fine Food Reviews dataset
- Preprocess and clean the text data
- Train a Logistic Regression model
- Save the trained model to `data/amazon_sentiment_lr_model.joblib`
- Generate evaluation metrics and graphs

**Note**: Training may take several minutes depending on the sample size (default: 50,000 reviews).

### Step 2: Run the Demo

Launch the interactive Streamlit web application:

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## Using the Demo

1. **Enter a review**: Type or paste a product review in the text box
2. **Analyze**: Click the "Analyze Sentiment" button
3. **View results**: See the predicted sentiment (positive/negative) with confidence score

### Example Reviews to Try

**Positive:**
> "This product is absolutely amazing! Best purchase ever. The quality is outstanding and it exceeded all my expectations. Highly recommend!"

**Negative:**
> "Terrible product. Complete waste of money. It broke after one use and the quality is awful. Very disappointed with this purchase."

## Project Structure

```
cs484project/
├── main.py                    # Main training pipeline
├── preprocessing.py           # Data loading and preprocessing
├── model_training.py          # Model training functions
├── model_evaluation.py        # Model evaluation and metrics
├── app.py                     # Streamlit demo application
├── requirements.txt           # Python dependencies
├── data/                      # Data and model files
│   ├── amazon_sentiment_lr_model.joblib  # Trained model
│   └── predicted_sentiment_counts.png     # Performance graph
└── README.md                  # This file
```

## Model Details

### Preprocessing
- Text cleaning (URLs, mentions, special characters)
- Lowercasing
- Optional removal of neutral 3-star reviews

### Feature Engineering
- TF-IDF vectorization
- N-gram range: (1, 2)
- Max features: 100,000
- Min/Max document frequency filtering

### Model Architecture
- Algorithm: Logistic Regression
- Solver: liblinear
- Regularization: L2 (C=2.0)
- Class weighting: balanced

## Configuration

You can modify the following parameters in `main.py`:

- `SUBSAMPLE`: Number of reviews to use for training (default: 50,000)
- `DROP3STARS`: Whether to remove neutral 3-star reviews (default: True)

## Requirements

- Python 3.8+
- See `requirements.txt` for package dependencies

## Demo for Professor

To demonstrate this project:

1. Ensure the model is trained (run `python main.py` if needed)
2. Launch the Streamlit app: `streamlit run app.py`
3. Show the interactive interface and try different reviews
4. Explain the model architecture and preprocessing steps
5. Show the performance metrics in the sidebar

## Authors

CS484 Machine Learning Project

## License

This project is for educational purposes.
