import os
import shutil
from datetime import datetime
from app.extensions.configHtml import *

##################################################################
#Monta o HTML quando o opção escolhida foi por Segmento
##################################################################
def htmlReceberSegmento(baixas, linhas, seg):
    caminho = get_path(__name__)
    pasta = f"{caminho}/app/templates/impressoes"
    shutil.rmtree(pasta, ignore_errors=False, onerror=None)
    
    with open(f"{caminho}/app/templates/baseImpressao/baseReceberSeg.html", "r+", encoding='utf-8') as html:
        htmlBase = html.read()
        html.flush()
    
    os.makedirs(pasta)
    hora = datetime.now().strftime("%H:%M:%S")
    
    nomeHtml = f"impressaoReceber{hora}.html".replace(":", "")
    
    with open(f"{caminho}/app/templates/impressoes/{nomeHtml}", "a+", encoding='utf-8') as html:
        html.write(htmlBase)
        somaSaldo = 0
        somaTotalSaldo = 0
        for x in range(0, linhas):
            if x < linhas-1:
                somaSaldo += filtroFloat(baixas[x].t_saldo)
                if baixas[x].segmento != baixas[x+1].segmento:
                    html.write(f"""<tr>
                            <td id="nota">{filtroData(baixas[x].t_dataVenc)}</td>
                            <td>{baixas[x].t_numDoc} / {baixas[x].t_numParcela}</td>
                            <td>{baixas[x].segmento}{baixas[x].t_docRef}</td>
                            <td>{filtroNome(baixas[x].cliente)}</td>
                            <td>{filtroNome(baixas[x].vendedor)}</td>
                            <td>{calculaDias(baixas[x].t_dataVenc)}</td>
                            <td style='text-align: right;'>{filtroValor(baixas[x].t_saldo)}</td>
                            </tr>""")
                    html.write(f"""
                                <tr id="tr-total">
                                <td id="td-total" colspan="3">Total Segmento {baixas[x].descSeg}</td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td style='text-align: right;'>{filtroValor(somaSaldo)}</td>
                                </tr>
                                """)
                    somaTotalSaldo += somaSaldo
                    somaSaldo = 0
                else:
                    html.write(f"""<tr>
                            <td id="nota">{filtroData(baixas[x].t_dataVenc)}</td>
                            <td>{baixas[x].t_numDoc} / {baixas[x].t_numParcela}</td>
                            <td>{baixas[x].segmento}{baixas[x].t_docRef}</td>
                            <td>{filtroNome(baixas[x].cliente)}</td>
                            <td>{filtroNome(baixas[x].vendedor)}</td>
                            <td>{calculaDias(baixas[x].t_dataVenc)}</td>
                            <td style='text-align: right;'>{filtroValor(baixas[x].t_saldo)}</td>
                            </tr>""")
            if x == linhas-1:
                somaSaldo += filtroFloat(baixas[x].t_saldo)
                html.write(f"""<tr>
                            <td id="nota">{filtroData(baixas[x].t_dataVenc)}</td>
                            <td>{baixas[x].t_numDoc} / {baixas[x].t_numParcela}</td>
                            <td>{baixas[x].segmento}{baixas[x].t_docRef}</td>
                            <td>{filtroNome(baixas[x].cliente)}</td>
                            <td>{filtroNome(baixas[x].vendedor)}</td>
                            <td>{calculaDias(baixas[x].t_dataVenc)}</td>
                            <td style='text-align: right;'>{filtroValor(baixas[x].t_saldo)}</td>
                            </tr>""")
                if seg == True:
                    html.write(f"""
                                <tr id="tr-total">
                                <td id="td-total" colspan="3">Total Segmento {baixas[x].descSeg}</td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td style='text-align: right;'>{filtroValor(somaSaldo)}</td>
                                </tr>
                                    """)
        somaTotalSaldo += somaSaldo
        somaSaldo = 0
        html.write(f"""
                        <tr id="tr-total-geral">
                        <td id="td-total">Total Geral</td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td style='text-align: right;'>{filtroValor(somaTotalSaldo)}</td>
                        </tr>
                        """)
        
        html.write("""
            </tbody>
            </table>
            </div>
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
            

##################################################################
#Monta o HTML quando o opção escolhida foi por periodo
##################################################################
def htmlReceberPeriodo(baixas, linhas):
    caminho = get_path(__name__)
    pasta = f"{caminho}/app/templates/impressoes"
    shutil.rmtree(pasta, ignore_errors=False, onerror=None)
    
    with open(f"{caminho}/app/templates/baseImpressao/baseReceber.html", "r+", encoding='utf-8') as html:
        htmlBase = html.read()
        html.flush()
    
    os.makedirs(pasta)
    hora = datetime.now().strftime("%H:%M:%S")
    
    nomeHtml = f"impressaoReceber{hora}.html".replace(":", "")
    
    with open(f"{caminho}/app/templates/impressoes/{nomeHtml}", "a+", encoding='utf-8') as html:
        html.write(htmlBase)
        somaSaldo = 0
        somaTotalSaldo = 0
        for x in range(0, linhas):
            if x < linhas-1:
                somaSaldo += filtroFloat(baixas[x].t_saldo)
                if baixas[x].t_dataVenc != baixas[x+1].t_dataVenc:
                    html.write(f"""<tr>
                                    <td id="nota">{filtroData(baixas[x].t_dataVenc)}</td>
                                    <td>{baixas[x].t_numDoc} / {baixas[x].t_numParcela}</td>
                                    <td>{baixas[x].segmento}{baixas[x].t_docRef}</td>
                                    <td>{filtroNome(baixas[x].cliente)}</td>
                                    <td>{filtroNome(baixas[x].vendedor)}</td>
                                    <td>{calculaDias(baixas[x].t_dataVenc)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].t_saldo)}</td>
                                    </tr>""")
                    html.write(f"""
                                <tr id="tr-total">
                                <td id="td-total">Total Dia</td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td style='text-align: right;'>{filtroValor(somaSaldo)}</td>
                                </tr>
                                """)
                    somaTotalSaldo += somaSaldo
                    somaSaldo = 0
                else:
                    html.write(f"""<tr>
                                    <td id="nota">{filtroData(baixas[x].t_dataVenc)}</td>
                                    <td>{baixas[x].t_numDoc} / {baixas[x].t_numParcela}</td>
                                    <td>{baixas[x].segmento}{baixas[x].t_docRef}</td>
                                    <td>{filtroNome(baixas[x].cliente)}</td>
                                    <td>{filtroNome(baixas[x].vendedor)}</td>
                                    <td>{calculaDias(baixas[x].t_dataVenc)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].t_saldo)}</td>
                                    </tr>""")
            if x == linhas-1:
                somaSaldo += filtroFloat(baixas[x].t_saldo)
                html.write(f"""<tr>
                            <td id="nota">{filtroData(baixas[x].t_dataVenc)}</td>
                            <td>{baixas[x].t_numDoc} / {baixas[x].t_numParcela}</td>
                            <td>{baixas[x].segmento}{baixas[x].t_docRef}</td>
                            <td>{filtroNome(baixas[x].cliente)}</td>
                            <td>{filtroNome(baixas[x].vendedor)}</td>
                            <td>{calculaDias(baixas[x].t_dataVenc)}</td>
                            <td style='text-align: right;'>{filtroValor(baixas[x].t_saldo)}</td>
                            </tr>""")
                html.write(f"""
                        <tr id="tr-total">
                        <td id="td-total">Total Dia</td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td style='text-align: right;'>{filtroValor(somaSaldo)}</td>
                        </tr>
                        """)
                
        somaTotalSaldo += somaSaldo
        somaSaldo = 0
        html.write(f"""
                <tr id="tr-total-geral">
                <td id="td-total">Total Geral</td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td style='text-align: right;'>{filtroValor(somaTotalSaldo)}</td>
                </tr>
                """)
        
        html.write("""
            </tbody>
            </table>
            </div>
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
            
                     
##################################################################
#Monta o HTML quando o opção escolhida foi por Vendedor
##################################################################            
def htmlReceberbVend(baixas, linhas):
    caminho = get_path(__name__)
    pasta = f"{caminho}/app/templates/impressoes"
    shutil.rmtree(pasta, ignore_errors=False, onerror=None)
    
    with open(f"{caminho}/app/templates/baseImpressao/baseReceberCliVend.html", "r+", encoding='utf-8') as html:
        htmlBase = html.read()
        html.flush()
    
    os.makedirs(pasta)
    hora = datetime.now().strftime("%H:%M:%S")
    
    nomeHtml = f"impressaoReceber{hora}.html".replace(":", "")

    with open(f"{caminho}/app/templates/impressoes/{nomeHtml}", "a+", encoding='utf-8') as html:
        html.write(htmlBase)
        somaSaldo = 0
        somaTotalSaldo = 0
        for x in range(0, linhas):
            if x < linhas-1:
                somaSaldo += filtroFloat(baixas[x].t_saldo)
                if baixas[x].t_dataVenc != baixas[x+1].t_dataVenc:
                    html.write(f"""<tr>
                                    <td id="nota">{filtroData(baixas[x].t_dataVenc)}</td>
                                    <td>{baixas[x].t_numDoc} / {baixas[x].t_numParcela}</td>
                                    <td>{baixas[x].segmento}{baixas[x].t_docRef}</td>
                                    <td>{filtroNome(baixas[x].cliente)}</td>
                                    <td>{calculaDias(baixas[x].t_dataVenc)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].t_saldo)}</td>
                                    </tr>""")
                    html.write(f"""
                                <tr id="tr-total">
                        <td id="td-total">Total Dia</td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td style='text-align: right;'>{filtroValor(somaSaldo)}</td>
                        </tr>
                                """)
                    somaTotalSaldo += somaSaldo
                    somaSaldo = 0
                else:
                    html.write(f"""<tr>
                                    <td id="nota">{filtroData(baixas[x].t_dataVenc)}</td>
                                    <td>{baixas[x].t_numDoc} / {baixas[x].t_numParcela}</td>
                                    <td>{baixas[x].segmento}{baixas[x].t_docRef}</td>
                                    <td>{filtroNome(baixas[x].cliente)}</td>
                                    <td>{calculaDias(baixas[x].t_dataVenc)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].t_saldo)}</td>
                                    </tr>""")
            if x == linhas-1:
                somaSaldo += filtroFloat(baixas[x].t_saldo)
                html.write(f"""<tr>
                                    <td id="nota">{filtroData(baixas[x].t_dataVenc)}</td>
                                    <td>{baixas[x].t_numDoc} / {baixas[x].t_numParcela}</td>
                                    <td>{baixas[x].segmento}{baixas[x].t_docRef}</td>
                                    <td>{filtroNome(baixas[x].cliente)}</td>
                                    <td>{calculaDias(baixas[x].t_dataVenc)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].t_saldo)}</td>
                                    </tr>""")
                html.write(f"""
                                <tr id="tr-total">
                        <td id="td-total">Total Dia</td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td style='text-align: right;'>{filtroValor(somaSaldo)}</td>
                        </tr>
                                """)
        somaTotalSaldo += somaSaldo
        somaSaldo = 0
        html.write(f"""
                            <tr id="tr-total-geral">
                <td id="td-total">Total Geral</td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td style='text-align: right;'>{filtroValor(somaTotalSaldo)}</td>
                </tr>
                            """)
        
        html.write("""
            </tbody>
            </table>
            </div>
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
                   

##################################################################
#Monta o HTML quando o opção escolhida foi por Cliente
##################################################################            
def htmlReceberbCli(baixas, linhas):
    caminho = get_path(__name__)
    pasta = f"{caminho}/app/templates/impressoes"
    shutil.rmtree(pasta, ignore_errors=False, onerror=None)
    
    with open(f"{caminho}/app/templates/baseImpressao/baseReceberCliVend.html", "r+", encoding='utf-8') as html:
        htmlBase = html.read()
        html.flush()
        
    os.makedirs(pasta)
    hora = datetime.now().strftime("%H:%M:%S")
    
    nomeHtml = f"impressaoReceber{hora}.html".replace(":", "")
    
    with open(f"{caminho}/app/templates/impressoes/{nomeHtml}", "a+", encoding='utf-8') as html:
        html.write(htmlBase)
        somaSaldo = 0
        somaTotalSaldo = 0
        for x in range(0, linhas):
            if x < linhas-1:
                somaSaldo += filtroFloat(baixas[x].t_saldo)
                if baixas[x].t_dataVenc != baixas[x+1].t_dataVenc:
                    html.write(f"""<tr>
                                    <td id="nota">{filtroData(baixas[x].t_dataVenc)}</td>
                                    <td>{baixas[x].t_numDoc} / {baixas[x].t_numParcela}</td>
                                    <td>{baixas[x].segmento}{baixas[x].t_docRef}</td>
                                    <td>{filtroNome(baixas[x].vendedor)}</td>
                                    <td>{calculaDias(baixas[x].t_dataVenc)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].t_saldo)}</td>
                                    </tr>""")
                    html.write(f"""
                                <tr id="tr-total">
                        <td id="td-total">Total Dia</td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td style='text-align: right;'>{filtroValor(somaSaldo)}</td>
                        </tr>
                                """)
                    somaTotalSaldo += somaSaldo
                    somaSaldo = 0
                else:
                    html.write(f"""<tr>
                                    <td id="nota">{filtroData(baixas[x].t_dataVenc)}</td>
                                    <td>{baixas[x].t_numDoc} / {baixas[x].t_numParcela}</td>
                                    <td>{baixas[x].segmento}{baixas[x].t_docRef}</td>
                                    <td>{filtroNome(baixas[x].vendedor)}</td>
                                    <td>{calculaDias(baixas[x].t_dataVenc)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].t_saldo)}</td>
                                    </tr>""")
            if x == linhas-1:
                somaSaldo += filtroFloat(baixas[x].t_saldo)
                html.write(f"""<tr>
                                    <td id="nota">{filtroData(baixas[x].t_dataVenc)}</td>
                                    <td>{baixas[x].t_numDoc} / {baixas[x].t_numParcela}</td>
                                    <td>{baixas[x].segmento}{baixas[x].t_docRef}</td>
                                    <td>{filtroNome(baixas[x].vendedor)}</td>
                                    <td>{calculaDias(baixas[x].t_dataVenc)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].t_saldo)}</td>
                                    </tr>""")
                html.write(f"""
                                <tr id="tr-total">
                        <td id="td-total">Total Dia</td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td style='text-align: right;'>{filtroValor(somaSaldo)}</td>
                        </tr>
                                """)
        somaTotalSaldo += somaSaldo
        somaSaldo = 0
        html.write(f"""
                            <tr id="tr-total-geral">
                <td id="td-total">Total Geral</td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td style='text-align: right;'>{filtroValor(somaTotalSaldo)}</td>
                </tr>
                            """)
        
        html.write("""
            </tbody>
            </table>
            </div>
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

            