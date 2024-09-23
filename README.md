# Visão Geral

Este projeto demonstra um protótipo funcional de uma solução baseada em **Inteligência Artificial** que extrai, analisa e classifica documentos PDF. Ele utiliza modelos de aprendizado de máquina, como **BERT**, para classificação contextual, **Naive Bayes** para análise de conteúdo, e a biblioteca **TextBlob** para análise de sentimento.

## Funcionalidades

O sistema executa as seguintes operações:

- **Extração de Texto**: Utilizando a biblioteca **pdfplumber**, o texto é extraído automaticamente de documentos PDF.
- **Classificação de Contexto com BERT**: Um modelo BERT (`facebook/bart-large-mnli`) classifica o contexto do documento em três categorias: "alta", "média" ou "baixa" prioridade.
- **Análise de Sentimento**: Usando a biblioteca **TextBlob**, o sistema avalia o sentimento do documento para classificá-lo como "positivo", "neutro" ou "negativo".
- **Classificação com Naive Bayes**: O sistema faz uma análise de prioridade usando **Naive Bayes**, com base no conteúdo textual e em palavras-chave.
- **Verificação de Datas**: O sistema identifica datas no documento e verifica se ele está "dentro do prazo", "vencido" ou "sem data", utilizando **dateparser** ou **regex** para interpretação de diferentes formatos de data.
- **Combinação de Resultados**: A classificação final do documento é uma combinação das classificações de **BERT**, **Naive Bayes**, análise de sentimento e a verificação de validade de datas.

## Arquitetura de IA

### 1. Entrada de Dados

- **Origem**: PDFs enviados pelo usuário.
- **Aquisição**: O texto dos PDFs é extraído utilizando **pdfplumber**.

#### Implementação:

```python
def extrair_texto_pdf(caminho_arquivo):
    with pdfplumber.open(caminho_arquivo) as pdf:
        texto = ''
        for pagina in pdf.pages:
            texto += pagina.extract_text()
    return texto
```

### 2. Pré-processamento de Dados

Após extrair o texto dos PDFs, é necessário pré-processar os dados para que possam ser usados nos classificadores (BERT e Naive Bayes) e na análise de sentimento.

#### Componentes:

- **Pré-processamento de Texto**: O texto extraído dos PDFs não requer muita transformação, mas pode precisar de algumas etapas dependendo do formato dos documentos.
- **Extração de Datas**: A biblioteca `re` é usada para identificar padrões de datas no texto, e o `dateparser` converte esses padrões para formatos de datas.

#### Implementação:

```python
def extrair_datas(texto):
    padrao_data = r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b|\b(\d{1,2}\s(?:jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)\s\d{4})\b'
    datas_encontradas = re.findall(padrao_data, texto)
    datas_formatadas = [data[0] if data[0] else data[1] for data in datas_encontradas]
    return datas_formatadas
```

### 3. Modelo de Aprendizado: Classificação de Texto

Seu projeto usa dois tipos principais de modelos para classificar os documentos extraídos dos PDFs:

- **BERT (transformer)**: Um modelo de linguagem poderoso que faz a classificação de texto com base em aprendizado não supervisionado.
- **Naive Bayes**: Um modelo de aprendizado supervisionado usado para classificar o texto com base em palavras-chave (usando vetorização).

#### Implementação:

##### BERT:

```python
from transformers import pipeline

def classificar_contexto_bert(texto):
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    classes = ["baixa prioridade", "média prioridade", "alta prioridade"]
    resultado = classifier(texto, classes)
    return resultado['labels'][0]
```

##### Naive Bayes:

```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

# Dados de treino
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

# Vetorização e treinamento
vetorizador = CountVectorizer()
X = vetorizador.fit_transform(dados['documento'])
y = dados['rótulo']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

modelo_naive = MultinomialNB()
modelo_naive.fit(X_train, y_train)

def classificar_prioridade_naive(texto, vetorizador, modelo_naive):
    vetor_texto = vetorizador.transform([texto])
    return modelo_naive.predict(vetor_texto)[0]
```

### 4. Análise de Sentimento

A biblioteca **TextBlob** é usada para realizar a análise de sentimento dos textos extraídos dos PDFs. Esta análise é importante para ajudar a complementar as classificações de prioridade, já que um documento com sentimento negativo pode ser classificado com uma prioridade mais alta.

#### Implementação:

```python
from textblob import TextBlob

def analisar_sentimento(texto):
    blob = TextBlob(texto)
    sentimento = blob.sentiment.polarity
    if sentimento > 0:
        return "positivo"
    elif sentimento < 0:
        return "negativo"
    else:
        return "neutro"
```
### 5. Inferência e Teste

Depois que o modelo de IA classifica os textos e realiza a análise de sentimento, os resultados são apresentados ao usuário. A lógica de inferência inclui a combinação de resultados de múltiplos classificadores (**BERT**, **Naive Bayes** e **análise de sentimento**) para determinar a prioridade final do documento.

#### Implementação:

```python
def analisar_documento_completo(caminho_pdf, nome_pdf):
    texto_documento = extrair_texto_pdf(caminho_pdf)

    # Classificação BERT
    classificacao_bert = classificar_contexto_bert(texto_documento)
    print(f"Classificação BERT: {classificacao_bert}")

    # Análise de Sentimento
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
```
#### Exemplo de Saída:

```python
Analisando o arquivo: relatorio_fornecedor_8.pdf

Classificação BERT: baixa prioridade
Sentimento do documento: neutro
Classificação Naive Bayes: baixa
Validade do documento: sem data
Classificação Final: média prioridade
```