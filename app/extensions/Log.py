from datetime import datetime
from .pastaLog import Pasta
import os

class Log(Pasta):
    """
    Classe para funções relacionadas ao gerar logs de erros e logs de interação no sistema
    @author - Fabio
    @version - 1.0
    @since - 17/10/2023
    """

    def geraLogErro(self, excecao, erro, listaErro, link) -> None:
        caminhoArq = self.verificaArquivoRecenteLogErro(self.caminhoPasta())
        with open (f"{caminhoArq}", "a+") as txt:
            txt.write(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]\nErro: {excecao} {erro}")
            for erro in listaErro:
                txt.write(f"\nArquivo: {erro[0]} - Linha: {erro[1]} '{erro[3]}'")
            txt.write(f"\nURL: {link}\n")
            txt.write(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]\n\n\n")
            

    def geraLogDiario(self, operacao, usuario, filial, referencia=False) -> None:
        caminhoArq = self.verificaArquivoRecenteLogDia(self.caminhoPasta())
        self.verificaDataLog(caminhoArq)
        with open (f"{caminhoArq}", "a+") as txt:
            if referencia:
                txt.write(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] - Usuário '{usuario}' realizou a seguinte ação: {operacao} {referencia} - FILIAL: {filial}\n")
            else: 
                txt.write(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] - Usuário '{usuario}' realizou a seguinte ação: {operacao} - FILIAL: {filial}\n")


    def logErro(self, classErro, link, erro) -> None:
        caminhoArq = self.verificaArquivoRecenteLogErro(self.caminhoPasta())
        with open (f"{caminhoArq}", "a+") as txt:
            txt.write(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] - Erro: {erro} {classErro} - URL: {link}\n\n")

    
    def verificaDataLog(self, caminhoArq) -> None:
        if not os.path.exists(caminhoArq):
            with open (f"{caminhoArq}", "a+") as txt:
                pass

        with open (f"{caminhoArq}", "r+") as txt:
            linhas = txt.readlines()
            if "\n" in linhas:
                linhas.remove("\n")
            
        linha = linhas[-1]
        dataArquivo = linha[1:11]
        dataAtual = datetime.now().strftime('%d/%m/%Y')

        if dataArquivo != dataAtual:
            with open (f"{caminhoArq}", "a+") as txt:
                txt.write(f"\n----------------------------------------------------------------------[{dataAtual}]----------------------------------------------------------------------\n\n")