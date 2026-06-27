import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import joblib
from sklearn.metrics import roc_curve, auc

# Create plots folder if it does not exist
os.makedirs("plots", exist_ok=True)

# Load dataset
df = pd.read_csv("data/train.csv")

# Load test data for ROC curve
X_test = pd.read_csv("data/X_test.csv")
y_test = pd.read_csv("data/y_test.csv").values.ravel()

# Load saved models
logistic = joblib.load("models/logistic_regression.pkl")
decision = joblib.load("models/decision_tree.pkl")
knn = joblib.load("models/knn.pkl")

# Set style
sns.set_style("whitegrid")

# 1. Survival Count Plot
plt.figure(figsize=(6, 4))
sns.countplot(x="Survived", data=df)
plt.title("Survival Count")
plt.xlabel("Survived (0 = No, 1 = Yes)")
plt.ylabel("Count")
plt.savefig("plots/survival_count.png", dpi=300, bbox_inches="tight")
plt.show()

# 2. Survival by Sex
plt.figure(figsize=(6, 4))
sns.countplot(x="Sex", hue="Survived", data=df)
plt.title("Survival by Sex")
plt.xlabel("Sex")
plt.ylabel("Count")
plt.savefig("plots/survival_by_sex.png", dpi=300, bbox_inches="tight")
plt.show()

# 3. Survival by Passenger Class
plt.figure(figsize=(6, 4))
sns.countplot(x="Pclass", hue="Survived", data=df)
plt.title("Survival by Passenger Class")
plt.xlabel("Passenger Class")
plt.ylabel("Count")
plt.savefig("plots/survival_by_class.png", dpi=300, bbox_inches="tight")
plt.show()

# 4. Age Distribution
plt.figure(figsize=(8, 5))
sns.histplot(df["Age"].dropna(), kde=True)
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Count")
plt.savefig("plots/age_distribution.png", dpi=300, bbox_inches="tight")
plt.show()

# 5. Fare Distribution
plt.figure(figsize=(8, 5))
sns.histplot(df["Fare"], kde=True)
plt.title("Fare Distribution")
plt.xlabel("Fare")
plt.ylabel("Count")
plt.savefig("plots/fare_distribution.png", dpi=300, bbox_inches="tight")
plt.show()

# 6. Correlation Heatmap
plt.figure(figsize=(10, 7))
numeric_df = df.select_dtypes(include=["int64", "float64"])
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.savefig("plots/correlation_heatmap.png", dpi=300, bbox_inches="tight")
plt.show()

# 7. ROC Curve Comparison
plt.figure(figsize=(9, 7))

models = [
    ("Logistic Regression", logistic),
    ("Decision Tree", decision),
    ("KNN", knn)
]

for model_name, model in models:
    y_prob = model.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)

    plt.plot(
        fpr,
        tpr,
        linewidth=2,
        label=f"{model_name} (AUC = {roc_auc:.3f})"
    )

# Random classifier line
plt.plot([0, 1], [0, 1], linestyle="--", color="black", label="Random Guess")

plt.title("ROC Curve Comparison")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend(loc="lower right")
plt.grid(True)

plt.savefig("plots/roc_curve.png", dpi=300, bbox_inches="tight")
plt.show()

print("All plots generated successfully and saved in the 'plots' folder.")
