import os
import pdfplumber
import re
import dateparser
from datetime import datetime

#Extrair texto de PDFs
def extrair_texto_pdf(caminho_arquivo):
    with pdfplumber.open(caminho_arquivo) as pdf:
        texto = ''
        for pagina in pdf.pages:
            texto += pagina.extract_text()
    return texto

#Função para extrair datas do texto
def extrair_datas(texto):
    padrao_data = r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b|\b(\d{1,2}\s(?:jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)\s\d{4})\b'
    datas_encontradas = re.findall(padrao_data, texto)
    datas_formatadas = [data[0] if data[0] else data[1] for data in datas_encontradas]
    return datas_formatadas

#Verificação das validade das datas
def verificar_validade(datas):
    if not datas:
        return "sem data"
    
    data_atual = datetime.now()
    status_validade = "dentro do prazo"
    
    for data in datas:
        if isinstance(data, str):
            try:
                data_formatada = dateparser.parse(data)
                if data_formatada and data_formatada < data_atual:
                    return "vencido"
            except Exception:
                continue

    return status_validade

#Função para analisar um PDF (individual)
def analisar_pdf(caminho_pdf):
    texto_documento = extrair_texto_pdf(caminho_pdf)
    print(f"Texto extraído do PDF:\n{texto_documento[:500]}...")  # Exibindo os primeiros 500 caracteres

    datas_extraidas = extrair_datas(texto_documento)
    print(f"Datas extraídas: {datas_extraidas}")

    validade = verificar_validade(datas_extraidas)
    print(f"Validade do documento: {validade}")

# Função para processar múltiplos PDFs na pasta (varios)
def processar_pdfs_na_pasta(pasta_pdf):
    for nome_arquivo in os.listdir(pasta_pdf):
        if nome_arquivo.endswith(".pdf"):
            caminho_pdf = os.path.join(pasta_pdf, nome_arquivo)
            print(f"\nAnalisando arquivo: {nome_arquivo}")
            analisar_pdf(caminho_pdf)

# Defina o caminho da pasta onde os PDFs estão localizados
PASTA_PDFS = "pdf_teste" 

# Execução principal
if __name__ == "__main__":
    processar_pdfs_na_pasta(PASTA_PDFS)