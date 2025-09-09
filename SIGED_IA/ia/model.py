import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import os
import numpy as np

def get_base_dir():
    current_file = os.path.abspath(__file__)
    return os.path.abspath(os.path.join(current_file, '..', '..', '..'))

def get_models_path(filename):
    base_dir = get_base_dir()
    return os.path.join(base_dir, 'models', filename)

def prepare_features(df, X_text):
    num_cols = ['anexos']
    if all(col in df.columns for col in num_cols):
        X_num = df[num_cols].values
    else:
        X_num = np.empty((X_text.shape[0], 0))
    X_combined = np.hstack([X_num, X_text.toarray()])
    return X_combined

def train_model(X, y):
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    return clf

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

def save_model(model, filename='model_rf.joblib'):
    path = get_models_path(filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)

def load_model(filename='model_rf.joblib'):
    path = get_models_path(filename)
    return joblib.load(path)