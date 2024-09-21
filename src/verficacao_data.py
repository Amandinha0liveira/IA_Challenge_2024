#FUNÇAÕ: Arquivo conterá a função de verificação de datas utilizando o dateparser e regex

import re
import dateparser
from datetime import datetime

# Função para extrair datas do texto
def extrair_datas(texto):
    padrao_data = r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b|\b(\d{1,2}\s(?:jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)\s\d{4})\b'
    datas_encontradas = re.findall(padrao_data, texto)
    datas_formatadas = [data[0] if data[0] else data[1] for data in datas_encontradas]
    return datas_formatadas

# Função para verificar validade das datas
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
            except Exception as e:
                continue
    return status_validade