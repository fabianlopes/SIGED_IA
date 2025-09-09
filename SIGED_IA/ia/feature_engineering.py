from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os

def get_base_dir():
    current_file = os.path.abspath(__file__)
    return os.path.abspath(os.path.join(current_file, '..', '..', '..'))

def get_models_path(filename):
    base_dir = get_base_dir()
    return os.path.join(base_dir, 'models', filename)

def fit_vectorizer(texts, max_features=5000):
    vectorizer = TfidfVectorizer(max_features=max_features)
    X_text = vectorizer.fit_transform(texts)
    return vectorizer, X_text

def transform_text(vectorizer, texts):
    return vectorizer.transform(texts)

def save_vectorizer(vectorizer, filename='vectorizer.joblib'):
    path = get_models_path(filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(vectorizer, path)

def load_vectorizer(filename='vectorizer.joblib'):
    path = get_models_path(filename)
    return joblib.load(path)