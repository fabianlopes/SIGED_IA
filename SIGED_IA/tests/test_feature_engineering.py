import pytest
from SIGED_IA.ia import feature_engineering as fe

def test_fit_and_transform_vectorizer():
    texts = ["teste de texto", "outro texto de exemplo"]
    vectorizer, X = fe.fit_vectorizer(texts, max_features=10)
    X_transformed = fe.transform_text(vectorizer, ["teste novo"])
    assert X.shape[0] == 2
    assert X_transformed.shape[0] == 1
    assert X.shape[1] <= 10

def test_save_and_load_vectorizer(tmp_path):
    texts = ["teste"]
    vectorizer, _ = fe.fit_vectorizer(texts)
    path = tmp_path / "vectorizer.joblib"
    fe.save_vectorizer(vectorizer, str(path))
    vectorizer_loaded = fe.load_vectorizer(str(path))
    assert vectorizer_loaded is not None