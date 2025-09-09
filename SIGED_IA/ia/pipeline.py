from SIGED_IA.ia import data_preprocessing as dp
from SIGED_IA.ia import feature_engineering as fe
from SIGED_IA.ia import model as m
from sklearn.model_selection import train_test_split

def run_pipeline():
    print("Iniciando pipeline...")

    # Usar nomes de arquivos simples, os módulos resolvem o caminho completo
    raw_filename = 'documentos_exemplo_atualizados.csv'
    processed_filename = 'documentos_processados.csv'
    vectorizer_filename = 'vectorizer.joblib'
    model_filename = 'model_rf.joblib'

    print("1. Carregando dados...")
    df = dp.load_data(raw_filename)

    print("2. Pré-processando dados...")
    df = dp.preprocess_dataframe(df)
    dp.save_processed(df, processed_filename)

    print("3. Criando features de texto...")
    vectorizer, X_text = fe.fit_vectorizer(df['descricao_limpo'])
    fe.save_vectorizer(vectorizer, vectorizer_filename)

    print("4. Preparando features finais...")
    X = m.prepare_features(df, X_text)
    y = df.get('erro_tramite')
    if y is None:
        raise ValueError("Coluna 'erro_tramite' não encontrada.")

    print("5. Dividindo dados em treino e teste...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("6. Treinando modelo...")
    model = m.train_model(X_train, y_train)

    print("7. Avaliando modelo...")
    m.evaluate_model(model, X_test, y_test)

    print("8. Salvando modelo...")
    m.save_model(model, model_filename)

    print("Pipeline executada com sucesso!!!")