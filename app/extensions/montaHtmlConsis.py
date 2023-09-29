import os
import shutil
from datetime import datetime
from app.extensions.configHtml import *
from ..models.Tables import *

##################################################################
# Monta o HTML de consistencia para a impressão
##################################################################
def htmlConsis(titulos, linhas):
    caminho = get_path(__name__)
    pasta = f"{caminho}/app/templates/impressoes"
    shutil.rmtree(pasta, ignore_errors=False, onerror=None)
    
    with open(f"{caminho}/app/templates/baseImpressao/baseConsistencia.html", "r+", encoding='utf-8') as html:
        htmlBase = html.read()
        html.flush()
    
    os.makedirs(pasta)
    hora = datetime.now().strftime("%H%M%S")
    
    nomeHtml = f"impressaoConsis{hora}.html"
                   
    with open(f"{caminho}/app/templates/impressoes/{nomeHtml}", "a+", encoding='utf-8') as html:
        html.write(htmlBase)
        somaValor = 0
        somaSaldo = 0
        somaTotalValor = 0
        somaTotalSaldo = 0
        for x in range(0, linhas):
            if x < linhas-1:
                if titulos[x].t_numDoc == 2769:
                    print("")
                somaValor += filtroFloat(titulos[x].t_valor)
                somaSaldo += filtroFloat(titulos[x].t_saldo)
                if titulos[x].segmento != titulos[x+1].segmento:
                    html.write(f"""<tr>
                                <td id="nota">{titulos[x].t_numDoc} / {titulos[x].t_numParcela}</td>
                                <td>{filtroData(titulos[x].t_dataLanc)}</td>
                                <td>{filtroNome(titulos[x].cliente)}</td>
                                <td>{filtroNome(titulos[x].vendedor)}</td>
                                <td>{filtroData(titulos[x].t_dataVenc)}</td>
                                <td>{titulos[x].segmento}{titulos[x].t_docRef}</td>
                                <td>{situacao(filtroFloat(titulos[x].t_valor), filtroFloat(titulos[x].t_saldo))}</td>
                                <td style='text-align: right;'>{filtroValor(titulos[x].t_valor)}</td>
                                <td id="valor" style='text-align: right;'>{filtroValor(titulos[x].t_saldo)}</td>
                                </tr>""")
                    html.write(f"""
                                <tr id="tr-total">
                                <td id="td-total" colspan="3">Total Segmento {titulos[x].decSeg}</td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td style='text-align: right;'>{filtroValor(somaValor)}</td>
                                <td style='text-align: right;'>{filtroValor(somaSaldo)}</td>
                                </tr>
                                """)
                    somaTotalValor += somaValor
                    somaTotalSaldo += somaSaldo
                    somaValor = 0
                    somaSaldo = 0
                else:
                    html.write(f"""<tr>
                                <td id="nota">{titulos[x].t_numDoc} / {titulos[x].t_numParcela}</td>
                                <td>{filtroData(titulos[x].t_dataLanc)}</td>
                                <td>{filtroNome(titulos[x].cliente)}</td>
                                <td>{filtroNome(titulos[x].vendedor)}</td>
                                <td>{filtroData(titulos[x].t_dataVenc)}</td>
                                <td>{titulos[x].segmento}{titulos[x].t_docRef}</td>
                                <td>{situacao(filtroFloat(titulos[x].t_valor), filtroFloat(titulos[x].t_saldo))}</td>
                                <td style='text-align: right;'>{filtroValor(titulos[x].t_valor)}</td>
                                <td id="valor" style='text-align: right;'>{filtroValor(titulos[x].t_saldo)}</td>  
                                </tr>""")
            if x == linhas-1:
                somaValor += filtroFloat(titulos[x].t_valor)
                somaSaldo += filtroFloat(titulos[x].t_saldo)
                html.write(f"""<tr>
                                <td id="nota">{titulos[x].t_numDoc} / {titulos[x].t_numParcela}</td>
                                <td>{filtroData(titulos[x].t_dataLanc)}</td>
                                <td>{filtroNome(titulos[x].cliente)}</td>
                                <td>{filtroNome(titulos[x].vendedor)}</td>
                                <td>{filtroData(titulos[x].t_dataVenc)}</td>
                                <td>{titulos[x].segmento}{titulos[x].t_docRef}</td>
                                <td>{situacao(filtroFloat(titulos[x].t_valor), filtroFloat(titulos[x].t_saldo))}</td>
                                <td style='text-align: right;'>{filtroValor(titulos[x].t_valor)}</td>
                                <td id="valor" style='text-align: right;'>{filtroValor(titulos[x].t_saldo)}</td>
                                </tr>""")
                html.write(f"""
                            <tr id="tr-total">
                            <td id="td-total" colspan="3">Total Segmento {titulos[x].decSeg}</td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td style='text-align: right;'>{filtroValor(somaValor)}</td>
                            <td style='text-align: right;'>{filtroValor(somaSaldo)}</td>
                            </tr>
                            """)
        somaTotalValor += somaValor
        somaTotalSaldo += somaSaldo
        somaValor = 0
        somaSaldo = 0
        html.write(f"""
                    <tr id="tr-total-geral">
                    <td id="td-total">Total Geral</td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td style='text-align: right;'>{filtroValor(somaTotalValor)}</td>
                    <td style='text-align: right;'>{filtroValor(somaTotalSaldo)}</td>
                    </tr>
                    """)

        html.write("""
            </tbody>
            </table>
            <div id="btns">
                <a class="btn btn-outline-primary btn-sm" href="javascript:window.print()">Imprimir</a>
                <a class="btn btn-outline-danger btn-sm" href="javascript:window.close()">Fechar</a>
            </div>
            </body>
            <script>
                    
                const zeroFill = n => {
                    return ('0' + n).slice(-2);
                }
                    
                const now = new Date();
            
                const data = zeroFill(now.getUTCDate()) + '/' + zeroFill((now.getMonth() + 1)) + '/' + now.getFullYear();
                const hora = zeroFill(now.getHours()) + ':' + zeroFill(now.getMinutes());
                document.getElementById('data-hora').innerHTML = `<h6>${data}</h6><h6>${hora}</h6>`;
                    
            </script>
            <div id="rodape"></div>
            </html>""")
        html.flush()
    
    return nomeHtml


def htmlConsisCli(listaCli, dataDe, dataAte):
    caminho = get_path(__name__)
    pasta = f"{caminho}/app/templates/impressoes"
    shutil.rmtree(pasta, ignore_errors=False, onerror=None)
    
    with open(f"{caminho}/app/templates/baseImpressao/baseConsistenciaCli.html", "r+", encoding='utf-8') as html:
        htmlBase = html.read()
        html.flush()
    
    os.makedirs(pasta)
    hora = datetime.now().strftime("%H:%M:%S")
    
    nomeHtml = f"impressaoConsis{hora}.html".replace(":", "")
    
    with open(f"{caminho}/app/templates/impressoes/{nomeHtml}", "a+", encoding='utf-8') as html:
        html.write(htmlBase)
        conexao = Gf3004
        conexao2 = Gf3001
        conexao3 = Gf3002
        conexao4 = Gf3003
        for idCli in listaCli:
            titulos = DB.session.query(conexao.t_numDoc, conexao.t_numParcela, conexao.t_dataLanc, conexao.t_dataVenc, conexao2.c_razaosocial.label("cliente"), conexao3.v_nome.label("vendedor"), 
            conexao4.s_abrev.label("segmento"), conexao4.s_desc.label("decSeg"), conexao.t_docRef, conexao.t_saldo, conexao.t_valor, conexao.t_status) \
            .join(conexao2, conexao2.c_id==conexao.t_idCliente) \
            .join(conexao3, conexao3.v_id==conexao.t_idVendedor) \
            .join(conexao4, conexao4.s_id==conexao.t_segmento) \
            .filter(conexao.t_dataLanc>=dataDe, conexao.t_dataLanc<=dataAte, conexao.t_idCliente==idCli[0], conexao.t_ativo==1) \
            .order_by(conexao4.s_abrev, conexao.t_dataLanc)
            
            
            linhas = DB.session.query(conexao.t_numDoc, conexao.t_numParcela, conexao.t_dataLanc, conexao.t_dataVenc, conexao2.c_razaosocial.label("cliente"), conexao3.v_nome.label("vendedor"), 
            conexao4.s_abrev.label("segmento"), conexao4.s_desc.label("decSeg"), conexao.t_docRef, conexao.t_saldo, conexao.t_valor, conexao.t_status) \
            .join(conexao2, conexao2.c_id==conexao.t_idCliente) \
            .join(conexao3, conexao3.v_id==conexao.t_idVendedor) \
            .join(conexao4, conexao4.s_id==conexao.t_segmento) \
            .filter(conexao.t_dataLanc>=dataDe, conexao.t_dataLanc<=dataAte, conexao.t_idCliente==idCli[0], conexao.t_ativo==1) \
            .order_by(conexao4.s_abrev, conexao.t_dataLanc).count()
            
            html.write(f"""
                       <div class="header-vend">
                        <h5>Cliente: {titulos[0].cliente}</h5>
                       </div>
                       """)
            
            html.write("""<table class='table' id="table">
                    <thead>
                        <tr>
                            <th style="width: 8%;">Doc.</th>
                            <th style="width: 8%;">Dt. Lanc.</th>
                            <th style="width: 8%;">Cliente</th>
                            <th style="width: 8%;">Vendedor</th>
                            <th style="width: 8%;">Vencimento</th>
                            <th style="width: 6%;">Ref.</th>
                            <th style="width: 4%;">Situacao</th>
                            <th style="width: 8%; text-align: right;">Valor Titulo</th>
                            <th style="width: 8%; text-align: right;">Saldo a Receber</th>
                        </tr>
                    </thead>
                    <tbody id="tbody">""")
            somaValor = 0
            somaSaldo = 0
            somaTotalValor = 0
            somaTotalSaldo = 0
            for x in range(0, linhas):
                if x < linhas-1:
                    somaValor += titulos[x].t_valor
                    somaSaldo += titulos[x].t_saldo
                    if titulos[x].segmento != titulos[x+1].segmento:
                        html.write(f"""<tr>
                                <td id="nota">{titulos[x].t_numDoc} / {titulos[x].t_numParcela}</td>
                                <td>{filtroData(titulos[x].t_dataLanc)}</td>
                                <td>{filtroNome(titulos[x].cliente)}</td>
                                <td>{filtroNome(titulos[x].vendedor)}</td>
                                <td>{filtroData(titulos[x].t_dataVenc)}</td>
                                <td>{titulos[x].segmento}{titulos[x].t_docRef}</td>
                                <td>{situacao(filtroFloat(titulos[x].t_valor), filtroFloat(titulos[x].t_saldo))}</td>
                                <td style='text-align: right;'>{filtroValor(titulos[x].t_valor)}</td>
                                <td id="valor" style='text-align: right;'>{filtroValor(titulos[x].t_saldo)}</td>
                                </tr>
                                   """)
                        
                        html.write(f"""
                                <tr id="tr-total">
                                <td id="td-total" colspan="3">Total Segmento {titulos[x].decSeg}</td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td style='text-align: right;'>{filtroValor(somaValor)}</td>
                                <td style='text-align: right;'>{filtroValor(somaSaldo)}</td>
                                </tr>
                                """)
                        somaTotalValor += somaValor
                        somaTotalSaldo += somaSaldo
                        somaValor = 0
                        somaSaldo = 0
                        
                    else:
                        html.write(f"""<tr>
                                    <td id="nota">{titulos[x].t_numDoc} / {titulos[x].t_numParcela}</td>
                                    <td>{filtroData(titulos[x].t_dataLanc)}</td>
                                    <td>{filtroNome(titulos[x].cliente)}</td>
                                    <td>{filtroNome(titulos[x].vendedor)}</td>
                                    <td>{filtroData(titulos[x].t_dataVenc)}</td>
                                    <td>{titulos[x].segmento}{titulos[x].t_docRef}</td>
                                    <td>{situacao(filtroFloat(titulos[x].t_valor), filtroFloat(titulos[x].t_saldo))}</td>
                                    <td style='text-align: right;'>{filtroValor(titulos[x].t_valor)}</td>
                                    <td id="valor" style='text-align: right;'>{filtroValor(titulos[x].t_saldo)}</td>  
                                    </tr>""")
                        
                if x == linhas-1:
                    somaValor += filtroFloat(titulos[x].t_valor)
                    somaSaldo += filtroFloat(titulos[x].t_saldo)
                    html.write(f"""<tr>
                                    <td id="nota">{titulos[x].t_numDoc} / {titulos[x].t_numParcela}</td>
                                    <td>{filtroData(titulos[x].t_dataLanc)}</td>
                                    <td>{filtroNome(titulos[x].cliente)}</td>
                                    <td>{filtroNome(titulos[x].vendedor)}</td>
                                    <td>{filtroData(titulos[x].t_dataVenc)}</td>
                                    <td>{titulos[x].segmento}{titulos[x].t_docRef}</td>
                                    <td>{situacao(filtroFloat(titulos[x].t_valor), filtroFloat(titulos[x].t_saldo))}</td>
                                    <td style='text-align: right;'>{filtroValor(titulos[x].t_valor)}</td>
                                    <td id="valor" style='text-align: right;'>{filtroValor(titulos[x].t_saldo)}</td>
                                    </tr>""")
                    
                    html.write(f"""
                                <tr id="tr-total">
                                <td id="td-total" colspan="3">Total Segmento {titulos[x].decSeg}</td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td style='text-align: right;'>{filtroValor(somaValor)}</td>
                                <td style='text-align: right;'>{filtroValor(somaSaldo)}</td>
                                </tr>
                                """)
                    somaTotalValor += somaValor
                    somaTotalSaldo += somaSaldo
                    somaValor = 0
                    somaSaldo = 0
        
                    html.write(f"""
                        <tr id="tr-total-geral">
                        <td id="td-total">Total Geral</td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td style='text-align: right;'>{filtroValor(somaTotalValor)}</td>
                        <td style='text-align: right;'>{filtroValor(somaTotalSaldo)}</td>
                        </tr>
                        </tbody>
                        </table>
                        """) 
                 
        html.write("""
        </tbody>
        </table>
        <div id="btns">
            <a class="btn btn-outline-primary btn-sm" href="javascript:window.print()">Imprimir</a>
            <a class="btn btn-outline-danger btn-sm" href="javascript:window.close()">Fechar</a>
        </div>
        </body>
        <script>
                
            const zeroFill = n => {
                return ('0' + n).slice(-2);
            }
                
            const now = new Date();
        
            const data = zeroFill(now.getUTCDate()) + '/' + zeroFill((now.getMonth() + 1)) + '/' + now.getFullYear();
            const hora = zeroFill(now.getHours()) + ':' + zeroFill(now.getMinutes());
            document.getElementById('data-hora').innerHTML = `<h6>${data}</h6><h6>${hora}</h6>`;
                
        </script>
        <div id="rodape"></div>
        </html>""")
            
        html.flush()
    
    return nomeHtml