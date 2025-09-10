import os
import shutil
import pytest
from unittest import mock
from SIGED_IA.ia import pipeline

# Caminho real do arquivo CSV original (ajuste para seu ambiente)
ORIGINAL_CSV_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'SIGED_IA', 'data', 'documentos_exemplo_atualizados.csv'))


@pytest.fixture(scope="module")
def setup_and_teardown(tmp_path_factory):
    # Criar diretório temporário para simular raiz do projeto
    tmp_dir = tmp_path_factory.mktemp("project_root")

    # Criar subpasta SIGED_IA/data e copiar CSV para lá
    tmp_sigedia_dir = tmp_dir / "SIGED_IA"
    tmp_sigedia_dir.mkdir()
    tmp_data_dir = tmp_sigedia_dir / "data"
    tmp_data_dir.mkdir()
    tmp_csv_path = tmp_data_dir / "documentos_exemplo_atualizados.csv"
    shutil.copy(ORIGINAL_CSV_PATH, tmp_csv_path)

    # Criar subpasta SIGED_IA/models vazia
    tmp_models_dir = tmp_sigedia_dir / "models"
    tmp_models_dir.mkdir()

    yield tmp_dir, tmp_sigedia_dir, tmp_data_dir, tmp_models_dir


def test_run_pipeline_creates_files(setup_and_teardown):
    tmp_dir, tmp_sigedia_dir, tmp_data_dir, tmp_models_dir = setup_and_teardown

    # Mockar get_base_dir para apontar para tmp_sigedia_dir (SIGED_IA)
    with mock.patch('SIGED_IA.ia.data_preprocessing.get_base_dir', return_value=str(tmp_sigedia_dir)), \
            mock.patch('SIGED_IA.ia.feature_engineering.get_base_dir', return_value=str(tmp_sigedia_dir)), \
            mock.patch('SIGED_IA.ia.model.get_base_dir', return_value=str(tmp_sigedia_dir)):
        pipeline.run_pipeline()

    # Verificar arquivos criados na pasta temporária SIGED_IA
    processed_csv = tmp_data_dir / 'documentos_processados.csv'
    vectorizer_file = tmp_models_dir / 'vectorizer.joblib'
    model_file = tmp_models_dir / 'model_rf.joblib'

    assert processed_csv.exists(), "Arquivo de dados processados não foi criado."
    assert vectorizer_file.exists(), "Arquivo do vectorizer não foi criado."
    assert model_file.exists(), "Arquivo do modelo não foi criado."