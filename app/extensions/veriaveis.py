import os
import json as js

#Função que retorna o caminho do arquivo
def get_path_variaveis():
    ###################################################################################################
    # Função que pega a Pasta do projeto.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return f"{BASEDIR}GefIII/app/" = caso o server estiver rodando no pendrive;
    #   return f"{BASEDIR}/app/" = caso o server estiver rodando na máquina. 
    ###################################################################################################
    
    BASEDIR = os.path.dirname(os.path.realpath(__name__))
    if "G:" in BASEDIR:
        return f"{BASEDIR}GefIII/app/variaveis/"
    else:
        return f"{BASEDIR}/app/variaveis/"
    
#Função que lê Json
def leAnoTitulo():
    ###################################################################################################
    # Função que lê o Json com parametros a pega o parametro ParAnoQueryTitulo para usar na query dos
    # Títulos.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return anoQuery = Retorna o número que está no arquivo Json.
    ###################################################################################################
    
    with open(f"{get_path_variaveis()}parametros.json", "r") as json:
        objJson = js.load(json)
        anoQuery = objJson["ParAnoQueryTitulo"]
        
    return anoQuery   

#Função que lê Json
def leAnoEstorno():
    ###################################################################################################
    # Função que lê o Json com parametros a pega o parametro ParAnoQueryEstorno para usar na query dos
    # Estornos.
    
    # PARAMETROS:
    #   Não tem parametros.
    
    # RETORNOS:
    #   return anoQuery = Retorna o número que está no arquivo Json.
    ###################################################################################################
    
    with open(f"{get_path_variaveis()}parametros.json", "r") as json:
        objJson = js.load(json)
        anoQuery = objJson["ParAnoQueryEstorno"]
        
    return anoQuery
