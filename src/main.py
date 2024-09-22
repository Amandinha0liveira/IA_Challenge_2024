import os
from src.utils import extrair_texto_pdf, extrair_datas, verificar_validade
from src.classifier import classificar_contexto_bert, classificar_prioridade_naive, modelo_naive, vetorizador
from src.sentiment import analisar_sentimento

# Define o caminho da pasta onde estão os arquivos PDF
PASTA_PDFS = "pdf_teste"  # Supondo que os PDFs estão na pasta 'data'

def analisar_documento_completo(caminho_pdf, nome_pdf):
    texto_documento = extrair_texto_pdf(caminho_pdf)

    # Mostrar o nome do arquivo PDF
    print(f"\nAnalisando o arquivo: {nome_pdf}")

    # BERT (contexto)
    classificacao_bert = classificar_contexto_bert(texto_documento)
    print(f"Classificação BERT: {classificacao_bert}")

    # Sentimento
    sentimento_documento = analisar_sentimento(texto_documento)
    print(f"Sentimento do documento: {sentimento_documento}")

    # Naive Bayes (palavras)
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

# Iterar sobre todos os PDFs na pasta
def analisar_pdfs_na_pasta(pasta):
    for nome_arquivo in os.listdir(pasta):
        if nome_arquivo.endswith(".pdf"):
            caminho_pdf = os.path.join(pasta, nome_arquivo)
            analisar_documento_completo(caminho_pdf, nome_arquivo)

if __name__ == "__main__":
    analisar_pdfs_na_pasta(PASTA_PDFS)
