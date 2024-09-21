# FUNÇÃO: Arquivo principal

from src.extract import extrair_texto_pdf
from src.classify import classificar_contexto_bert, classificar_prioridade_naive
from src.analyze_sentiment import analisar_sentimento
from src.check_dates import extrair_datas, verificar_validade
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# Dados de treino para Naive Bayes (exemplo simples)
dados = {
    'documento': [
        "O fornecedor cumpriu todos os padrões de segurança sem falhas.",
        "O contrato foi renovado e está em conformidade com as normas.",
        "A auditoria não encontrou nenhum problema nos relatórios técnicos.",
        "O documento apresenta falhas graves nos registros de segurança.",
        "O contrato está expirado e nenhuma renovação foi feita.",
        "Há pequenos atrasos na entrega de documentos, mas sem impacto na segurança.",
        "Alguns documentos estão incompletos, mas o fornecedor está corrigindo.",
        "A auditoria encontrou algumas irregularidades, porém sem riscos críticos."
    ],
    'rótulo': ['baixa', 'baixa', 'baixa', 'alta', 'alta', 'média', 'média', 'média']
}

# Vetorização e treinamento do modelo Naive Bayes
vetorizador = CountVectorizer()
X = vetorizador.fit_transform(dados['documento'])
y = dados['rótulo']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
modelo_naive = MultinomialNB()
modelo_naive.fit(X_train, y_train)

# Função para analisar um documento PDF
def analisar_documento_completo(caminho_pdf, nome_pdf):
    texto_documento = extrair_texto_pdf(caminho_pdf)
    print(f"\nAnalisando o arquivo: {nome_pdf}")
    
    # Classificação BERT (contexto)
    classificacao_bert = classificar_contexto_bert(texto_documento)
    print(f"Classificação BERT: {classificacao_bert}")
    
    # Sentimento
    sentimento_documento = analisar_sentimento(texto_documento)
    print(f"Sentimento do documento: {sentimento_documento}")
    
    # Classificação Naive Bayes
    classificacao_naive = classificar_prioridade_naive(texto_documento, vetorizador, modelo_naive)
    print(f"Classificação Naive Bayes: {classificacao_naive}")
    
    # Verificação de Data
    datas_extraidas = extrair_datas(texto_documento)
    validade = verificar_validade(datas_extraidas)
    print(f"Validade do documento: {validade}")
    
    # Combinação de classificações
    if classificacao_bert == "alta prioridade" or classificacao_naive == "alta" or sentimento_documento == "negativo":
        classificacao_final = "alta prioridade"
    elif classificacao_bert == "baixa prioridade" and classificacao_naive == "baixa" and sentimento_documento == "positivo":
        classificacao_final = "baixa prioridade"
    else:
        classificacao_final = "média prioridade"
    
    print(f"Classificação Final: {classificacao_final}")

# Executar o sistema
if __name__ == "__main__":
    caminho_pdf = "data/example.pdf"  # Certifique-se de que o caminho está correto
    nome_pdf = "example.pdf"
    analisar_documento_completo(caminho_pdf, nome_pdf)