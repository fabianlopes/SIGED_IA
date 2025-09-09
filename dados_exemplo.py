import pandas as pd
import random
from datetime import datetime, timedelta

num_docs = 50

departamentos = ['Financeiro', 'Jurídico', 'Recursos Humanos', 'TI', 'Comercial', 'Logística']
motivos = [
    "Solicitação de aprovação",
    "Revisão contratual",
    "Encaminhamento para auditoria",
    "Solicitação de compra",
    "Atualização de cadastro",
    "Relatório de progresso",
    "Notificação interna",
    "Solicitação de férias",
    "Pedido de reembolso",
    "Análise de risco"
]
referencias = [
    "REF001", "REF002", "REF003", "REF004", "REF005",
    "REF006", "REF007", "REF008", "REF009", "REF010"
]
classificacoes = ['Confidencial', 'Restrito', 'Público']
graus_acesso = ['Baixo', 'Médio', 'Alto']
procedencias = ['Interno', 'Externo']
descricoes = [
    "Documento referente a processo interno de aprovação.",
    "Relatório detalhado do andamento do processo.",
    "Solicitação enviada para departamento responsável.",
    "Atualização de dados cadastrais do cliente.",
    "Pedido formal de aquisição de materiais.",
    "Memorando para comunicação interna.",
    "Relatório financeiro do último trimestre.",
    "Solicitação de suporte técnico.",
    "Documentação relacionada à auditoria.",
    "Registro de reunião e decisões tomadas."
]

random.seed(42)


def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)


docs = []
start_data_processo = datetime(2023, 1, 1)
end_data_processo = datetime(2024, 5, 31)

for i in range(1, num_docs + 1):
    processo = f"PROC{i:05d}"
    data_do_processo = random_date(start_data_processo, end_data_processo)
    # data_de_abertura até 10 dias antes da data do processo
    data_de_abertura = data_do_processo - timedelta(days=random.randint(0, 10))

    departamento_atual = random.choice(departamentos)
    departamento_anterior_origem = random.choice(departamentos)

    motivo = random.choice(motivos)
    referencia = random.choice(referencias)
    classificacao = random.choice(classificacoes)
    grau_de_acesso = random.choice(graus_acesso)
    procedencia = random.choice(procedencias)
    anexos = random.randint(0, 5)  # número de anexos
    descricao = random.choice(descricoes)

    docs.append({
        'processo': processo,
        'data_do_processo': data_do_processo.strftime('%Y-%m-%d'),
        'data_de_abertura': data_de_abertura.strftime('%Y-%m-%d'),
        'departamento_atual': departamento_atual,
        'motivo': motivo,
        'referencia': referencia,
        'departamento_anterior_origem': departamento_anterior_origem,
        'classificacao': classificacao,
        'grau_de_acesso': grau_de_acesso,
        'procedencia': procedencia,
        'anexos': anexos,
        'descricao': descricaogit init
    })

df = pd.DataFrame(docs)
df.to_csv('documentos_exemplo_atualizados.csv', index=False)

print("Arquivo 'documentos_exemplo_atualizados.csv' criado com 50 registros de exemplo.")