import pandas as pd
import joblib
import os

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report
)


# Load data

X_train = pd.read_csv("data/X_train.csv")
X_test = pd.read_csv("data/X_test.csv")
y_train = pd.read_csv("data/y_train.csv").values.ravel()
y_test = pd.read_csv("data/y_test.csv").values.ravel()

print("Data loaded successfully")
print("Training data shape:", X_train.shape)
print("Testing data shape:", X_test.shape)

# Create folders if they do not exist
os.makedirs("models", exist_ok=True)

results = []
best_f1 = 0
best_model_name = ""
best_model = None


# Function to evaluate model

def evaluate_model(model, model_name):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc = roc_auc_score(y_test, y_prob)

    print(f"\n{model_name} Results:")
    print("Accuracy :", acc)
    print("Precision :", prec)
    print("Recall    :", rec)
    print("F1 Score  :", f1)
    print("ROC-AUC   :", roc)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    return acc, prec, rec, f1, roc


# Models

models = [
    (
        "Logistic Regression",
        Pipeline([
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(max_iter=1000))
        ])
    ),
    (
        "Decision Tree",
        DecisionTreeClassifier(random_state=42)
    ),
    (
        "KNN",
        Pipeline([
            ("scaler", StandardScaler()),
            ("model", KNeighborsClassifier(n_neighbors=5))
        ])
    )
]


# Train, evaluate, compare

saved_models = {}

for model_name, model in models:
    print(f"\nTraining {model_name}...")
    model.fit(X_train, y_train)

    acc, prec, rec, f1, roc = evaluate_model(model, model_name)

    results.append([model_name, acc, prec, rec, f1, roc])

    # Save each trained model separately
    file_name = model_name.lower().replace(" ", "_").replace("-", "_")
    model_path = f"models/{file_name}.pkl"
    joblib.dump(model, model_path)
    saved_models[model_name] = model_path
    print(f"{model_name} saved to {model_path}")

    # Track best model by F1 score
    if f1 > best_f1:
        best_f1 = f1
        best_model_name = model_name
        best_model = model


# Save results table

results_df = pd.DataFrame(
    results,
    columns=["Model", "Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"]
)

print("\nModel Comparison:")
print(results_df)

results_df.to_csv("data/model_results.csv", index=False)
print("\nResults saved to data/model_results.csv")


# Save best model

joblib.dump(best_model, "models/best_model.pkl")
print(f"\nBest model saved: {best_model_name} -> models/best_model.pkl")
