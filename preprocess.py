import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("data/train.csv")

print("Original missing values:")
print(df.isnull().sum())
print("\nOriginal shape:", df.shape)


# 1. Fill missing values


# Age: fill with median
df["Age"] = df["Age"].fillna(df["Age"].median())

# Embarked: fill with mode
df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])

# Cabin: fill missing with 'Unknown'
df["Cabin"] = df["Cabin"].fillna("Unknown")

# Fare: if any missing values exist
df["Fare"] = df["Fare"].fillna(df["Fare"].median())


# 2. Feature Engineering


# FamilySize = SibSp + Parch + 1
df["FamilySize"] = df["SibSp"] + df["Parch"] + 1

# IsAlone = 1 if passenger is alone, else 0
df["IsAlone"] = df["FamilySize"].apply(lambda x: 1 if x == 1 else 0)

# Extract Title from Name
df["Title"] = df["Name"].str.extract(" ([A-Za-z]+)\.", expand=False)

# Replace rare titles with 'Rare'
df["Title"] = df["Title"].replace([
    "Lady", "Countess", "Col", "Don", "Dr", "Major", "Rev",
    "Sir", "Jonkheer", "Dona", "Capt"
], "Rare")

# Group similar titles
df["Title"] = df["Title"].replace({
    "Mlle": "Miss",
    "Ms": "Miss",
    "Mme": "Mrs"
})

# Extract Deck from Cabin
df["Deck"] = df["Cabin"].str[0]
df["Deck"] = df["Deck"].replace("U", "Unknown")  # U means unknown


# 3. Show cleaned data

print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nNew columns added:")
print(["FamilySize", "IsAlone", "Title", "Deck"])

print("\nPreview of cleaned data:")
print(df[["Age", "Embarked", "Cabin", "FamilySize", "IsAlone", "Title", "Deck"]].head())

# Save cleaned dataset
df.to_csv("data/cleaned_train.csv", index=False)

print("\nCleaned dataset saved as data/cleaned_train.csv")