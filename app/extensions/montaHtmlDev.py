import os
import shutil
from datetime import datetime
from app.extensions.configHtml import *

##################################################################
# Monta o HTML com as devoluções feita para a impressão
##################################################################
def htmlDevolucao(devolucoes, linhas):
    caminho = get_path(__name__)
    pasta = f"{caminho}/app/templates/impressoes"
    shutil.rmtree(pasta, ignore_errors=False, onerror=None)
    
    with open(f"{caminho}/app/templates/baseImpressao/baseDevolucao.html", "r+", encoding='utf-8') as html:
        htmlBase = html.read()
        html.flush()
    
    os.makedirs(pasta)
    hora = datetime.now().strftime("%H:%M:%S")
    
    nomeHtml = f"impressaoDev{hora}.html".replace(":", "")
    
    with open(f"{caminho}/app/templates/impressoes/{nomeHtml}", "a+", encoding='utf-8') as html:
        html.write(htmlBase)
        somaValor = 0
        somaSaldo = 0
        for x in range(0, linhas):
            somaValor += filtroFloat(devolucoes[x].d_valor)
            somaSaldo += filtroFloat(devolucoes[x].d_saldo)
            html.write(f"""<tr>
                            <td id="nota">{devolucoes[x].d_docRef}</td>
                            <td>{filtroData(devolucoes[x].d_dataCad)}</td>
                            <td style='text-align: right;'>{filtroValor(devolucoes[x].d_valor)}</td>
                            <td style='text-align: right;'>{filtroValor(devolucoes[x].d_saldo)}</td>
                            </tr>""")
        html.write(f"""<tr id="tr-total">
                        <td id="td-total">Total</td>
                        <td></td>
                        <td style='text-align: right;'>{filtroValor(somaValor)}</td>
                        <td></td>
                        </tr>
                        """)
        html.write(f"""<tr id="tr-total">
                        <td id="td-total">Credito</td>
                        <td></td>
                        <td></td>
                        <td style='text-align: right;'>{filtroValor(somaSaldo)}</td>
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
# Monta o HTML de baixas por devolução para a impressão
##################################################################
def htmlBaixasDev(baixas, linhas):
    caminho = get_path(__name__)
    pasta = f"{caminho}/app/templates/impressoes"
    shutil.rmtree(pasta, ignore_errors=False, onerror=None)
    
    with open(f"{caminho}/app/templates/baseImpressao/baseBaixaDev.html", "r+", encoding='utf-8') as html:
        htmlBase = html.read()
        html.flush()
    
    os.makedirs(pasta)
    hora = datetime.now().strftime("%H:%M:%S")
    
    nomeHtml = f"impressaoDev{hora}.html".replace(":", "")
    
    with open(f"{caminho}/app/templates/impressoes/{nomeHtml}", "a+", encoding='utf-8') as html:
        html.write(htmlBase)
        somaValor = 0
        somaSaldo = 0
        somaTotalValor = 0
        somaTotalSaldo = 0
        for x in range(0, linhas):
            if x < linhas-1:
                somaValor += filtroFloat(baixas[x].m_valor)
                somaSaldo += filtroFloat(baixas[x].saldo)
                if baixas[x].m_dataBaixa != baixas[x+1].m_dataBaixa:
                    html.write(f"""<tr>
                                        <td id="nota">{filtroData(baixas[x].m_dataBaixa)}</td>
                                        <td>{baixas[x].m_numDoc} / {baixas[x].m_parcela}</td>
                                        <td>{baixas[x].m_docRef}</td>
                                        <td>{filtroNome(baixas[x].cliente)}</td>
                                        <td>{filtroNome(baixas[x].vendedor)}</td>
                                        <td>{filtroTipoBaixa(baixas[x].m_tipoBaixa)}</td>
                                        <td style='text-align: right;'>{filtroValor(baixas[x].m_valor)}</td>
                                        <td style='text-align: right;'>{filtroValor(baixas[x].saldo)}</td>
                                        </tr>""")
                    html.write(f"""
                                <tr id="tr-total">
                        <td id="td-total">Total Dia</td>
                        <td></td>
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
                                        <td id="nota">{filtroData(baixas[x].m_dataBaixa)}</td>
                                        <td>{baixas[x].m_numDoc} / {baixas[x].m_parcela}</td>
                                        <td>{baixas[x].m_docRef}</td>
                                        <td>{filtroNome(baixas[x].cliente)}</td>
                                        <td>{filtroNome(baixas[x].vendedor)}</td>
                                        <td>{filtroTipoBaixa(baixas[x].m_tipoBaixa)}</td>
                                        <td style='text-align: right;'>{filtroValor(baixas[x].m_valor)}</td>
                                        <td style='text-align: right;'>{filtroValor(baixas[x].saldo)}</td>
                                        </tr>""")
            if x == linhas-1:
                somaValor += filtroFloat(baixas[x].m_valor)
                somaSaldo += filtroFloat(baixas[x].saldo)
                html.write(f"""<tr>
                                        <td id="nota">{filtroData(baixas[x].m_dataBaixa)}</td>
                                        <td>{baixas[x].m_numDoc} / {baixas[x].m_parcela}</td>
                                        <td>{baixas[x].m_docRef}</td>
                                        <td>{filtroNome(baixas[x].cliente)}</td>
                                        <td>{filtroNome(baixas[x].vendedor)}</td>
                                        <td>{filtroTipoBaixa(baixas[x].m_tipoBaixa)}</td>
                                        <td style='text-align: right;'>{filtroValor(baixas[x].m_valor)}</td>
                                        <td style='text-align: right;'>{filtroValor(baixas[x].saldo)}</td>
                                        </tr>""")
                html.write(f"""
                            <tr id="tr-total">
                    <td id="td-total">Total Dia</td>
                    <td></td>
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
                        <tr id="tr-total">
                <td id="td-total">Total</td>
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