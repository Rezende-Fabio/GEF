import os
import shutil
from datetime import datetime
from app.extensions.configHtml import *
from ..models.Models import *
from sqlalchemy import func

##################################################################
# Monta o HTML de acordo com os número de documentos passados 
# para a impressão
##################################################################
def htmlPlanilha(listaDoc):
    caminho = get_path(__name__)
    pasta = f"{caminho}/app/templates/impressoes"
    shutil.rmtree(pasta, ignore_errors=False, onerror=None)
    
    os.makedirs(pasta)
    hora = datetime.now().strftime("%H:%M:%S")
    
    nomeHtml = f"impressaoPlanilha{hora}.html".replace(":", "")
                   
    with open(f"{caminho}/app/templates/impressoes/{nomeHtml}", "a+", encoding='utf-8') as html:
        html.write("""
                       <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta http-equiv="X-UA-Compatible" content="IE=edge">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Planilha de Titulos</title>

                            <link rel="stylesheet" href="{{ url_for('static', filename='plugins/bootstrap/css/bootstrap.min.css') }}">
                            <script type="text/javascript" src="{{ url_for('static', filename='plugins/bootstrap/js/bootstrap.min.js') }}"></script>
                            <script type="text/javascript" src="{{ url_for('static', filename='plugins/bootstrap/js/bootstrap.bundle.min.js') }}"></script>

                            <style>
                                .cabec{
                                    font-size:13.5px;
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
                                    body{
                                        margin: 1cm;
                                        top: 2cm;
                                    }
                                    
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
                       """)
        for j, i in enumerate(listaDoc):
            conexao = Gf3004
            conexao2 = Gf3001
            conexao3 = Gf3002
            conexao4 = Gf3003
            baixas = DB.session.query(conexao.t_numDoc, conexao.t_numParcela, conexao.t_docRef, conexao.t_dataLanc,
                                          conexao.t_dataVenc, conexao2.c_razaosocial.label("cliente"), conexao2.c_id.label("idCli"), conexao.t_valor,
                                          conexao3.v_nome.label("vendedor"), conexao3.v_id.label("idVend"), conexao.t_saldo, conexao4.s_abrev.label("segmento")).join(conexao2, conexao.t_idCliente==conexao2.c_id).join(conexao3, conexao.t_idVendedor==conexao3.v_id).join(conexao4, conexao.t_segmento==conexao4.s_id).filter(conexao.t_ativo==1, conexao.t_status==1, conexao.t_numDoc==i).order_by(conexao.t_dataVenc, conexao.t_numDoc, conexao.t_numParcela)
                
            html.write(f"""
                       <div class="container">
                        <div style="width: 100%; justify-content: center; align-items: center; display: flex; margin-top: 0;">
                            <h7 style="margin-top: 2rem;"><strong>Planilha de Titulos a Receber</strong></h7>
                        </div>
                        <p class="cabec">Número...... : {i}</p>
                        <P class="cabec">Cliente......... : {baixas[0].cliente} - {baixas[0].idCli}</P> 
                        <p class="cabec">Vendedor... : {baixas[0].vendedor} - {baixas[0].idVend}</p>
                        <span>__________________________________________ Parcelamento __________________________________________</span><br>
                        <table class='table' id="table">
                            <thead style="font-size: 12px;">
                                <tr>
                                    <th style="width: 8%;">Doc.</th>
                                    <th style="width: 4%;">Lanc.</th>
                                    <th style="width: 4%;">Venc.</th>
                                    <th style="width: 5%;">Ref.</th>
                                    <th style="width: 11%; text-align: right;">Vlr Princ.</th>
                                    <th style="width: 7%; text-align: right;">Juros</th>
                                    <th style="width: 7%; text-align: right;">Descont.</th>
                                    <th style="width: 11%; text-align: right;">Sald. Receb.</th>
                                </tr>
                            </thead>
                            <tbody id="tbody" style="font-size: 11px;">
                       """)
            
            somaValor = 0
            somaSaldo = 0
            for x in range(0, 4):
                try:
                    conexao5 = Gf3006
                    desconto = DB.session.query(func.sum(conexao5.m_deconto)).filter(conexao5.m_numDoc==baixas[x].t_numDoc, conexao5.m_parcela==baixas[x].t_numParcela).first()
                    juros = DB.session.query(func.sum(conexao5.m_juros)).filter(conexao5.m_numDoc==baixas[x].t_numDoc, conexao5.m_parcela==baixas[x].t_numParcela).first()
                    
                    somaValor += filtroFloat(baixas[x].t_valor)
                    somaSaldo += filtroFloat(baixas[x].t_saldo)
                    html.write(f"""
                            <tr>
                                <td>{baixas[x].t_numDoc} / {baixas[x].t_numParcela}</td>
                                <td>{filtroData(baixas[x].t_dataLanc)}</td>
                                <td>{filtroData(baixas[x].t_dataVenc)}</td>
                                <td>{baixas[x].segmento}{baixas[x].t_docRef}</td>
                                <td style="text-align: right;">{filtroValor(filtroFloat(baixas[x].t_valor))}</td>
                                <td style="text-align: right;">{filtroValor(filtroFloat(juros[0]))}</td>
                                <td style="text-align: right;">{filtroValor(filtroFloat(desconto[0]))}</td>
                                <td style="text-align: right;">{filtroValor(filtroFloat(baixas[x].t_saldo))}</td>
                            </tr>
                            """)
                except IndexError:
                    html.write(f"""
                            <tr>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                            </tr>
                            """)
            html.write(f"""
                            <tr>
                                <td>Total</td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td style="text-align: right;">{filtroValor(filtroFloat(somaValor))}</td>
                                <td></td>
                                <td></td>
                                <td style="text-align: right;">{filtroValor(filtroFloat(somaSaldo))}</td>
                            </tr>
                            """)
               
            if j%2:
                html.write("""
                        </tbody>
                            </table>
                            <span>Observ.:______________________________________________________________________________________________</span><br>   
                            <span>_______________________________________________________________________________________________________</span><br>
                            <span>_______________________________________________________________________________________________________</span><br>
                            <span>_______________________________________________________________________________________________________</span><br><br>
                            <div id='quebra'></div>
                        </div>""")
                
            else: 
                html.write("""
                        </tbody>
                            </table>
                            <span>Observ.:______________________________________________________________________________________________</span><br>   
                            <span>_______________________________________________________________________________________________________</span><br>
                            <span>_______________________________________________________________________________________________________</span><br>
                            <span>_______________________________________________________________________________________________________</span><br><br>
                            <i class="fa-solid fa-scissors"></i>
                            <span>-----------------------------------------------------------------------------------------------------------</span><br><br>
                        </div>""")
                
        html.write("""
                </div>
                <div id="btns">
                    <a class="btn btn-outline-primary btn-sm" href="javascript:window.print()">Imprimir</a>
                    <a class="btn btn-outline-danger btn-sm" href="javascript:window.close()">Fechar</a>
                </div>""")
                       
        html.flush()
    
    return nomeHtml