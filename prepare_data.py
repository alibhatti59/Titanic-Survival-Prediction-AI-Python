import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load the cleaned dataset
df = pd.read_csv("data/cleaned_train.csv")

print("Dataset loaded:")
print(df.head())

# Step 1: Select useful features

# We will not use columns like Name, Ticket, PassengerId, Cabin
# because they are not directly useful for first model training.

features = [
    "Pclass",
    "Sex",
    "Age",
    "SibSp",
    "Parch",
    "Fare",
    "Embarked",
    "FamilySize",
    "IsAlone",
    "Title",
    "Deck"
]

target = "Survived"

df_model = df[features + [target]].copy()

print("\nSelected columns:")
print(df_model.columns)


# Step 2: Encode text columns

# Convert text to numbers using one-hot encoding

df_model = pd.get_dummies(
    df_model,
    columns=["Sex", "Embarked", "Title", "Deck"],
    drop_first=True
)

print("\nColumns after encoding:")
print(df_model.columns)


# Step 3: Separate features and target

X = df_model.drop("Survived", axis=1)
y = df_model["Survived"]

print("\nShape of X:", X.shape)
print("Shape of y:", y.shape)


# Step 4: Split data

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining set shape:", X_train.shape)
print("Testing set shape:", X_test.shape)


# Step 5: Save prepared data

X_train.to_csv("data/X_train.csv", index=False)
X_test.to_csv("data/X_test.csv", index=False)
y_train.to_csv("data/y_train.csv", index=False)
y_test.to_csv("data/y_test.csv", index=False)

print("\nPrepared data saved successfully.")