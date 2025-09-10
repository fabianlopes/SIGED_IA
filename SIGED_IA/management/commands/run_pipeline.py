from django.core.management.base import BaseCommand
import os
from SIGED_IA.ia import data_preprocessing as dp
from SIGED_IA.ia import feature_engineering as fe
from SIGED_IA.ia import model as m
from sklearn.model_selection import train_test_split

class Command(BaseCommand):
    help = 'Executa a pipeline automatizada de treinamento e avaliação do modelo IA'

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando pipeline...")

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        data_raw_path = os.path.join(base_dir, 'data', 'documentos_exemplo_atualizados.csv')
        data_processed_path = os.path.join(base_dir, 'data', 'processed', 'documentos_processados.csv')
        vectorizer_path = os.path.join(base_dir, 'models', 'vectorizer.joblib')
        model_path = os.path.join(base_dir, 'models', 'model_rf.joblib')

        self.stdout.write("1. Carregando dados...")
        print(f"Diretorio base em: {base_dir}")
        print(f"Buscando arquivo em: {data_raw_path}")
        print(f"Arquivo existe? {os.path.exists(data_raw_path)}")
        df = dp.load_data(data_raw_path)

        self.stdout.write("2. Pré-processando dados...")
        df = dp.preprocess_dataframe(df)
        dp.save_processed(df, data_processed_path)

        self.stdout.write("3. Criando features de texto...")
        vectorizer, X_text = fe.fit_vectorizer(df['descricao_limpo'])
        fe.save_vectorizer(vectorizer, vectorizer_path)

        self.stdout.write("4. Preparando features finais...")
        X = m.prepare_features(df, X_text)
        y = df.get('erro_tramite', None)
        if y is None:
            self.stderr.write("Erro: coluna 'erro_tramite' não encontrada.")
            return

        self.stdout.write("5. Dividindo dados em treino e teste...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.stdout.write("6. Treinando modelo...")
        model = m.train_model(X_train, y_train)

        self.stdout.write("7. Avaliando modelo...")
        m.evaluate_model(model, X_test, y_test)

        self.stdout.write("8. Salvando modelo...")
        m.save_model(model, model_path)

        self.stdout.write(self.style.SUCCESS('Pipeline executada com sucesso!'))