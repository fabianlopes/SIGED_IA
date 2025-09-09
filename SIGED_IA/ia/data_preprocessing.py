import pandas as pd
import spacy
import os


# Carregar modelo spaCy em português (instale com: python -m spacy download pt_core_news_sm)
nlp = spacy.load("pt_core_news_sm")


def get_base_dir():
    # Caminho da raiz do projeto SIGED (onde está manage.py)
    current_file = os.path.abspath(__file__)
    # sobe 3 níveis: ia/ (1), SIGED_IA/ (2), SIGED/ (3)
    return os.path.abspath(os.path.join(current_file, '..', '..', '..'))


def get_data_path(filename):
    base_dir = get_base_dir()
    return os.path.join(base_dir, 'data', filename)


def load_data(filename='documentos_exemplo_atualizados.csv') -> pd.DataFrame:
    path = get_data_path(filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    return pd.read_csv(path)


def clean_text(text: str) -> str:
    if pd.isna(text):
        return ""
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(tokens)


def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if 'descricao' not in df.columns:
        raise ValueError("Coluna 'descricao' não encontrada no DataFrame")
    df['descricao_limpo'] = df['descricao'].apply(clean_text)

    for col in ['anexos']:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    return df


def save_processed(df: pd.DataFrame, filename='documentos_processados.csv'):
    base_dir = get_base_dir()
    save_path = os.path.join(base_dir, 'data', filename)
    df.to_csv(save_path, index=False)