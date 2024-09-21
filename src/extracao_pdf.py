#FUNÇÃO: Arquivo será responsável pela extração de texto dos PDFs 

import pdfplumber

# Função para extrair texto de PDFs
def extrair_texto_pdf(caminho_arquivo):
    with pdfplumber.open(caminho_arquivo) as pdf:
        texto = ''
        for pagina in pdf.pages:
            texto += pagina.extract_text()
    return texto