import pandas as pd
import pytest
from SIGED_IA.ia import data_preprocessing as dp

def test_clean_text_removes_stopwords():
    texto = "Este é um texto de teste simples."
    resultado = dp.clean_text(texto)
    # "este" e "é" são stopwords e devem ser removidos
    assert 'texto' in resultado
    assert 'teste' in resultado
    assert 'simples' in resultado
    assert 'este' not in resultado
    assert 'é' not in resultado

def test_preprocess_dataframe_adds_column():
    df = pd.DataFrame({'descricao': ["Teste de processamento"]})
    df_proc = dp.preprocess_dataframe(df)
    assert 'descricao_limpo' in df_proc.columns
    assert isinstance(df_proc.loc[0, 'descricao_limpo'], str)

def test_load_and_save(tmp_path):
    df = pd.DataFrame({'descricao': ["Teste"]})
    file_path = tmp_path / "test.csv"
    df.to_csv(file_path, index=False)
    df_loaded = dp.load_data(str(file_path))
    assert 'descricao' in df_loaded.columns
    dp.save_processed(df_loaded, str(file_path))
    assert file_path.exists()