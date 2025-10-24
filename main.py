import joblib
import kagglehub
from sklearn.model_selection import train_test_split
import preprocessing as pr
import model_training as mt
import model_evaluation as me

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
X, y = pr.prepareDataset(df, drop3Stars=False, subSample=5000)

# Train the model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)
model = mt.train_model(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]
me.dump_model_stats(y_test, y_pred, y_prob)
me.make_model_graph(y_pred)

# END OF PROGRAM
# persist artifacts
df.to_csv(out_csv, index=False)
print(f"Saved: {out_csv}")
joblib.dump(model, model_pkl)
print(f"Saved model: {model_pkl}")
