#FUNÇÃO: Arquivo será onde você implementa os modelos de classificação, como o BERT e o Naive Bayes       

from transformers import pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Função para classificar com BERT
def classificar_contexto_bert(texto):
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    classes = ["baixa prioridade", "média prioridade", "alta prioridade"]
    resultado = classifier(texto, classes)
    return resultado['labels'][0]  # Classe com maior pontuação

# Função para classificar com Naive Bayes
def classificar_prioridade_naive(texto, vetorizador, modelo):
    vetor_texto = vetorizador.transform([texto])
    return modelo.predict(vetor_texto)[0]
