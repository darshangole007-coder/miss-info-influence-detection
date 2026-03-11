# File: train_model.py (unchanged, but added comments for clarity)
import os
import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.calibration import CalibratedClassifierCV

def clean_text(text):
    import re
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def short_text(text, max_words=120):
    return " ".join(str(text).split()[:max_words])

DATA_DIR = "dataset"

fake_path = os.path.join(DATA_DIR, "Fake.csv")
true_path  = os.path.join(DATA_DIR, "True.csv")

if not os.path.exists(fake_path):
    print(f"Error: {fake_path} not found!")
    exit(1)

fake = pd.read_csv(fake_path)
# same for true

fake["label"] = 0
true["label"] = 1

data = pd.concat([fake, true], ignore_index=True)

data["combined"] = data["title"].fillna("") + " " + data["text"].fillna("")
data["combined"] = data["combined"].apply(short_text).apply(clean_text)

X = data["combined"]
y = data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    max_df=0.9,
    min_df=5,
    stop_words="english",
    sublinear_tf=True
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

base_model = LogisticRegression(
    max_iter=3000,
    class_weight="balanced",
    n_jobs=-1
)

model = CalibratedClassifierCV(base_model, method="sigmoid", cv=5)
model.fit(X_train_vec, y_train)

preds = model.predict(X_test_vec)
print("Accuracy:", accuracy_score(y_test, preds))

joblib.dump(model, "model/model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")