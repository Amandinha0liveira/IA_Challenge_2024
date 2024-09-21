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

### 2. Modelos de IA

- **Zero-Shot Classification com BERT**: O modelo `facebook/bart-large-mnli` é utilizado para classificar o documento em três categorias: "alta prioridade", "média prioridade", ou "baixa prioridade".
- **Classificador Naive Bayes**: Um classificador **Naive Bayes** treinado em exemplos de documentos prioriza os documentos com base no conteúdo textual.
- **Análise de Sentimento com TextBlob**: Avalia o sentimento global do documento, influenciando a classificação final.

### 3. Processamento de Texto e Data

As datas encontradas no documento são analisadas e comparadas com a data atual para verificar se o documento está vencido ou ainda dentro do prazo. Isso é feito utilizando **dateparser** para interpretar diversos formatos de data.

### 4. Classificação Final

A classificação final do documento é determinada pela combinação de:

- **Classificação de contexto com BERT**,
- **Classificação Naive Bayes** (palavras-chave),
- **Análise de sentimento**,
- **Verificação de validade de datas**.

### 5. Integração

O modelo pode ser integrado a uma interface web onde os usuários podem fazer upload de PDFs, e o sistema processa automaticamente os documentos, fornecendo a classificação e análise.
