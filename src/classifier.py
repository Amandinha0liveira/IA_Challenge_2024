from transformers import pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

#Modelo BERT para classificar o texto no contexto
def classificar_contexto_bert(texto):
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    classes = ["baixa prioridade", "média prioridade", "alta prioridade"]
    resultado = classifier(texto, classes)
    return resultado['labels'][0]

#Dados de treino para Naive Bayes
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

#Classificar prioridade com Naive Bayes
def classificar_prioridade_naive(texto, vetorizador, modelo):
    vetor_texto = vetorizador.transform([texto])
    return modelo.predict(vetor_texto)[0]

#Treinamento do modelo Naive Bayes
def treinar_naive_bayes(dados):
    vetorizador = CountVectorizer()
    X = vetorizador.fit_transform(dados['documento'])
    y = dados['rótulo']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo_naive = MultinomialNB()
    modelo_naive.fit(X_train, y_train)

    return modelo_naive, vetorizador

#Teste das classificações
def teste_classificacoes():
    texto_exemplo = "O contrato foi renovado e está em conformidade com as normas."

    # Classificação BERT
    classificacao_bert = classificar_contexto_bert(texto_exemplo)
    print(f"Classificação BERT: {classificacao_bert}")

    # Treinar Naive Bayes
    modelo_naive, vetorizador = treinar_naive_bayes(dados)

    # Classificação Naive Bayes
    classificacao_naive = classificar_prioridade_naive(texto_exemplo, vetorizador, modelo_naive)
    print(f"Classificação Naive Bayes: {classificacao_naive}")

#Executar os testes de classificação
if __name__ == "__main__":
    teste_classificacoes()