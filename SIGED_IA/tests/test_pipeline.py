import os
import shutil
import pytest

from SIGED_IA.ia.pipeline import run_pipeline

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    """Fixture para limpar arquivos antigos antes e depois dos testes."""
    # Remove arquivos gerados antes do teste (se existirem)
    processed_csv = os.path.join(DATA_DIR, 'documentos_processados.csv')
    vectorizer_file = os.path.join(MODELS_DIR, 'vectorizer.joblib')
    model_file = os.path.join(MODELS_DIR, 'model_rf.joblib')

    for f in [processed_csv, vectorizer_file, model_file]:
        if os.path.exists(f):
            os.remove(f)

    yield  # Executa o teste

    # Remove arquivos gerados após o teste para limpeza
    for f in [processed_csv, vectorizer_file, model_file]:
        if os.path.exists(f):
            os.remove(f)

def test_run_pipeline_creates_files():
    # Executa a pipeline
    run_pipeline()

    # Verifica se os arquivos esperados foram criados
    processed_csv = os.path.join(DATA_DIR, 'documentos_processados.csv')
    vectorizer_file = os.path.join(MODELS_DIR, 'vectorizer.joblib')
    model_file = os.path.join(MODELS_DIR, 'model_rf.joblib')

    assert os.path.exists(processed_csv), "Arquivo de dados processados não foi criado."
    assert os.path.exists(vectorizer_file), "Arquivo do vectorizer não foi criado."
    assert os.path.exists(model_file), "Arquivo do modelo não foi criado."