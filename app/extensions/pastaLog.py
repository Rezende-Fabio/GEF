import os

class Pasta:
    """
    Classe para funções relacionadas ao gerenciamento de arquivos de log
    @author - Fabio
    @version - 1.0
    @since - 17/10/2023
    """

    def __init__(self) -> None:
        self.caminhoArqErr = ""
        self.caminhoArqDia = ""


    def caminhoPasta(self) -> str:
        caminho = os.path.dirname(os.path.realpath(__name__))
        caminho = f"{caminho}\\app\\log\\"
        return caminho
    
    
    def caminhoArquivoErro(self, numlog) -> None:
        self.caminhoArqErr = f"{self.caminhoPasta()}logErro_{numlog}.log"

    
    def caminhoArquivoDia(self, numlog) -> None:
        self.caminhoArqDia = f"{self.caminhoPasta()}LogDiario_{numlog}.log"


    def verificaTamanhoArq(self, caminho: str, arquivo: str) -> None:
        try:
            tamanhoBytes = os.path.getsize(f"{caminho}\\{arquivo}")
            tamanhoMegaBytes = tamanhoBytes / (1024 * 1024)
            posicao1 = arquivo.find("_")
            posicao2 = arquivo.find(".")
            if tamanhoMegaBytes >= 5:
                numLog = int(arquivo[posicao1+1:posicao2])
                numLog += 1
                if "erro" in arquivo.lower():
                    self.caminhoArquivoErro(numLog)
                else:
                    self.caminhoArquivoDia(numLog)
            else:
                if "erro" in arquivo.lower():
                    self.caminhoArquivoErro(int(arquivo[posicao1+1:posicao2]))
                else:
                    self.caminhoArquivoDia(int(arquivo[posicao1+1:posicao2]))
            
        except FileNotFoundError:
            if "erro" in arquivo.lower():
                self.caminhoArquivoErro(0)
            else:
                self.caminhoArquivoDia(0)


    def verificaArquivoRecenteLogErro(self, caminho: str) -> None:
        arquivos = os.listdir(caminho)
        arquivos = [arquivo for arquivo in arquivos if 'erro' in arquivo.lower()] #Pegando apenas os arquivos de log erro
        arquivoMaisRecente = ""
        dataModificacaoRecente = 0.0
        if len(arquivos) != 0:
            for arquivo in arquivos:
                caminho_completo = os.path.join(caminho, arquivo)
                if os.path.isfile(caminho_completo):  # Verifica se é um arquivo (ignora pastas)
                    dataModificacao = os.path.getmtime(caminho_completo)
                    if dataModificacao > dataModificacaoRecente:
                        dataModificacaoRecente = dataModificacao
                        arquivoMaisRecente = arquivo
        else:
            arquivoMaisRecente = "LogErro_0.log"

        self.verificaTamanhoArq(caminho, arquivoMaisRecente)

        return self.caminhoArqErr


    def verificaArquivoRecenteLogDia(self, caminho: str) -> None:
        arquivos = os.listdir(caminho)
        arquivos = [arquivo for arquivo in arquivos if 'erro' not in arquivo.lower()] #Pegando apenas os arquivos de log diario
        arquivoMaisRecente = ""
        dataModificacaoRecente = 0.0
        if len(arquivos) != 0:
            for arquivo in arquivos:
                caminho_completo = os.path.join(caminho, arquivo)
                if os.path.isfile(caminho_completo):  # Verifica se é um arquivo (ignora pastas)
                    dataModificacao = os.path.getmtime(caminho_completo)
                    if dataModificacao > dataModificacaoRecente:
                        dataModificacaoRecente = dataModificacao
                        arquivoMaisRecente = arquivo
        else:
            arquivoMaisRecente = "LogDiario_0.log"

        self.verificaTamanhoArq(caminho, arquivoMaisRecente)

        return self.caminhoArqDia
        