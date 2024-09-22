from textblob import TextBlob

# Análise de sentimento
def analisar_sentimento(texto):
    blob = TextBlob(texto)
    sentimento = blob.sentiment.polarity
    if sentimento > 0:
        return "positivo"
    elif sentimento < 0:
        return "negativo"
    else:
        return "neutro"