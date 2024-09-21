#FUNÇÃO: Análise de Sentimento dentro do documento

from textblob import TextBlob

# Função para análise de sentimento
def analisar_sentimento(texto):
    blob = TextBlob(texto)
    sentimento = blob.sentiment.polarity
    if sentimento > 0:
        return "positivo"
    elif sentimento < 0:
        return "negativo"
    else:
        return "neutro"