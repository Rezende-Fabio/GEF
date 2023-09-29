from datetime import datetime
from .pastaLog import Pasta

class Logger():
    def log(operacao, usuario, filial, documento=False):
        diaAtual = datetime.now().strftime("%d")
        pasta = Pasta()
        caminho = pasta.get_path()
        with open (f"{caminho}/Log_Diario.txt", "a+") as txt:
            dataAtual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            if documento:
                txt.write(f"[{dataAtual}] - {usuario} executou {operacao} no {documento} - FILIAL: {filial}\n")
            else: 
                txt.write(f"[{dataAtual}] - {usuario} executou {operacao} - FILIAL: {filial}\n")
    
    def logErro(classErro, link, erro):
        diaAtual = datetime.now().strftime("%d")
        pasta = Pasta()
        caminho = pasta.get_path()
        with open (f"{caminho}/Log_Erro.txt", "a+") as txt:
            txt.write(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] - Erro: {erro} {classErro} - URL: {link}\n\n")