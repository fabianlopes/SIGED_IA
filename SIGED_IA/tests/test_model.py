import numpy as np
import pandas as pd
from SIGED_IA.ia import model as m

def test_prepare_features_combines_text_and_numeric():
    df = pd.DataFrame({'anexos': [1, 2, 3]})
    X_text = np.array([[0, 1], [1, 0], [0, 0]])
    X_combined = m.prepare_features(df, X_text)
    assert X_combined.shape[0] == 3
    assert X_combined.shape[1] == X_text.shape[1] + 1  # anexos + texto

def test_train_evaluate_save_load_model(tmp_path):
    X = np.array([[1, 0], [0, 1]])
    y = np.array([0, 1])
    model = m.train_model(X, y)
    assert model is not None

    from sklearn.metrics import accuracy_score
    y_pred = model.predict(X)
    acc = accuracy_score(y, y_pred)
    assert acc >= 0.5

    path = tmp_path / "model.joblib"
    m.save_model(model, str(path))
    loaded_model = m.load_model(str(path))
    y_pred_loaded = loaded_model.predict(X)
    assert (y_pred == y_pred_loaded).all()