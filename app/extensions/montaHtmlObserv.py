import os
import shutil
from datetime import datetime
from app.extensions.configHtml import *
from ..models.Models import *

##################################################################
# Monta o HTML com os títulos que tem observação para a impressão
##################################################################
def htmlObservacao(listaId):
    caminho = get_path(__name__)
    pasta = f"{caminho}/app/templates/impressoes"
    shutil.rmtree(pasta, ignore_errors=False, onerror=None)
    
    os.makedirs(pasta)
    hora = datetime.now().strftime("%H:%M:%S")
    
    nomeHtml = f"impressaoObervacao{hora}.html".replace(":", "")
                   
    with open(f"{caminho}/app/templates/impressoes/{nomeHtml}", "a+", encoding='utf-8') as html:
        num = 2
        html.write("""<!DOCTYPE html>
                    <html lang="pt-br">
                    <head>
                        <meta charset="UTF-8">
                        <meta http-equiv="X-UA-Compatible" content="IE=edge">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Observacoes</title>

                        <link rel="stylesheet" href="{{ url_for('static', filename='plugins/bootstrap/css/bootstrap.min.css') }}">
                        <script type="text/javascript" src="{{ url_for('static', filename='plugins/bootstrap/js/bootstrap.min.js') }}"></script>
                        <script type="text/javascript" src="{{ url_for('static', filename='plugins/bootstrap/js/bootstrap.bundle.min.js') }}"></script> 

                        <style>
                            .cabec{
                                font-size:13.5px;
                            }

                            .observacao{
                                border: 1px solid #000;
                                border-radius: 5px;
                                width: 100%;
                                padding-left: 10px;
                                padding-right: 10px;
                                margin-bottom: 1rem;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                            }

                            .text{
                                width: 100%;
                                overflow-wrap: break-word;  
                                word-wrap: break-word; 
                                word-break: break-word;
                            }

                            .text p{
                                white-space: pre-line;
                                text-overflow: ellipsis;
                            }

                            #quebra{
                                page-break-before: always;
                                page-break-inside: avoid;
                            }
                            
                            #btns{
                                justify-content: space-between;
                                width: 97%;
                                margin: 1rem;
                                align-items: center;
                                display: flex;
                                position: fixed;
                                bottom: 0.2rem;
                            }
                            
                            @media print{
                                @page{
                                    size: portrait;
                                }
                                #btns{
                                    display: none;
                                }
                            }
                        </style>

                    </head>
                    <body>
                        <div class="container">""")
        for j, i in enumerate(listaId):
            conexao = Gf3006
            conexao2 = Gf3001
            
            baixas = DB.session.query(conexao.m_numDoc, conexao.m_docRef, conexao.m_parcela, conexao.m_tipoBaixa, conexao.m_observ, conexao.m_valor, conexao2.c_razaosocial.label("cliente")).join(conexao2, conexao.m_idCliente==conexao2.c_id).filter(conexao.m_id==i).first()
           
            html.write(f"""
                    <div style="width: 100%; justify-content: center; align-items: center; display: flex; margin-top: 1.5rem;">
                        <h7><strong>Observações da Baixa</strong></h7>
                    </div>
                    <p class="cabec">Número...... : {baixas.m_numDoc}</p>
                    <p class="cabec">Referência.. : {baixas.m_docRef}</p>
                    <p class="cabec">Parcela......... : {baixas.m_parcela}</p>
                    <p class="cabec">Valor............. : {filtroValor(baixas.m_valor)}  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Tipo Baixa... : {filtroTipoBaixa(baixas.m_tipoBaixa)}</p>
                    <P class="cabec">Cliente......... : {baixas.cliente}</P> 
                    <span>______________________________ OBSERVAÇÃO ______________________________</span><br>
                    <div class="observacao">
                        <div class="text">
                            <p>{baixas.m_observ}</p>
                        </div>
                    </div>""")
            
            if j == num:
                num += 3
                html.write("""
                            <div id='quebra'></div>
                            """)  
                
            else:
                pass           
            
        html.write("""
                </div>
                <div id="btns">
                    <a class="btn btn-outline-primary btn-sm" href="javascript:window.print()">Imprimir</a>
                    <a class="btn btn-outline-danger btn-sm" href="javascript:window.close()">Fechar</a>
                </div>
                """)
        
        html.flush()
    
    return nomeHtml