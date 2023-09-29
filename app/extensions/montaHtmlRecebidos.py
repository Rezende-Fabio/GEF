import os
import shutil
from datetime import datetime
from app.extensions.configHtml import *           


##################################################################
#Monta o HTML quando o opção escolhida foi por Segmento
##################################################################
def htmlRecebSegmento(baixas, linhas, seg):
    caminho = get_path(__name__)
    pasta = f"{caminho}/app/templates/impressoes"
    shutil.rmtree(pasta, ignore_errors=False, onerror=None)
    
    with open(f"{caminho}/app/templates/baseImpressao/baseRecebidosSeg.html", "r+", encoding='utf-8') as html:
        htmlBase = html.read()
    
    os.makedirs(pasta)
    hora = datetime.now().strftime("%H:%M:%S")
    
    nomeHtml = f"impressaoRecebidos{hora}.html".replace(":", "")
    
    with open(f"{caminho}/app/templates/impressoes/{nomeHtml}", "a+", encoding='utf-8') as html:
        html.write(htmlBase)
        somaValor = 0
        somaComi = 0
        somaReceb = 0
        somaJuros = 0
        somaDesc = 0
        somaTotal = 0
        somaToatalComi = 0
        somaTotalReceb = 0
        somaTotalJuros = 0
        somaTotalDesc = 0
        
        for x in range(0, linhas):
            if x < linhas-1:
                somaValor += filtroFloat(baixas[x].m_valor)
                somaComi += filtroFloat(baixas[x].comissao)
                somaReceb += filtroFloat(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)
                somaJuros += filtroFloat(baixas[x].m_juros)
                somaDesc += filtroFloat(baixas[x].m_deconto)
                if baixas[x].segmento != baixas[x+1].segmento:
                    html.write(f"""<tr>
                                    <td id="nota">{filtroData(baixas[x].m_dataBaixa)}</td>
                                    <td>{baixas[x].m_numDoc} / {baixas[x].m_parcela}</td>
                                    <td>{baixas[x].m_docRef}</td>
                                    <td>{filtroNome(baixas[x].cliente)}</td>
                                    <td>{filtroNome(baixas[x].vendedor)}</td>
                                    <td>{filtroTipoBaixa(baixas[x].m_tipoBaixa)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_deconto)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_juros)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)}</td>
                                    <td id="valor" style='text-align: right;'>{filtroFloat(baixas[x].comissao)}</td>
                                    </tr>""")
                    html.write(f"""
                                <tr id="tr-total">
                                <td id="td-total" colspan="3">Total Segmento {baixas[x].descSeg}</td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td style='text-align: right;'>{filtroValor(somaValor)}</td>
                                <td style='text-align: right;'>{filtroValor(somaDesc)}</td>
                                <td style='text-align: right;'>{filtroValor(somaJuros)}</td>
                                <td style='text-align: right;'>{filtroValor(somaReceb)}</td>
                                <td style='text-align: right;'>{filtroValor(somaComi)}</td>
                                </tr>
                                """)
                    somaTotal += somaValor
                    somaToatalComi += somaComi
                    somaTotalReceb += somaReceb
                    somaTotalJuros += somaJuros
                    somaTotalDesc += somaDesc
                    somaValor = 0
                    somaComi = 0
                    somaReceb = 0
                    somaJuros = 0
                    somaDesc = 0
                else:
                    html.write(f"""<tr>
                                    <td id="nota">{filtroData(baixas[x].m_dataBaixa)}</td>
                                    <td>{baixas[x].m_numDoc} / {baixas[x].m_parcela}</td>
                                    <td>{baixas[x].m_docRef}</td>
                                    <td>{filtroNome(baixas[x].cliente)}</td>
                                    <td>{filtroNome(baixas[x].vendedor)}</td>
                                    <td>{filtroTipoBaixa(baixas[x].m_tipoBaixa)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_deconto)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_juros)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)}</td>
                                    <td id="valor" style='text-align: right;'>{filtroFloat(baixas[x].comissao)}</td>
                                    </tr>""")
            if x == linhas-1:
                somaValor += filtroFloat(baixas[x].m_valor)
                somaComi += filtroFloat(baixas[x].comissao)
                somaReceb += filtroFloat(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)
                somaJuros += filtroFloat(baixas[x].m_juros)
                somaDesc += filtroFloat(baixas[x].m_deconto)
                html.write(f"""<tr>
                                    <td id="nota">{filtroData(baixas[x].m_dataBaixa)}</td>
                                    <td>{baixas[x].m_numDoc} / {baixas[x].m_parcela}</td>
                                    <td>{baixas[x].m_docRef}</td>
                                    <td>{filtroNome(baixas[x].cliente)}</td>
                                    <td>{filtroNome(baixas[x].vendedor)}</td>
                                    <td>{filtroTipoBaixa(baixas[x].m_tipoBaixa)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_deconto)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_juros)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)}</td>
                                    <td id="valor" style='text-align: right;'>{filtroFloat(baixas[x].comissao)}</td>
                                    </tr>""")
                if seg == True:
                    html.write(f"""
                                    <tr id="tr-total">
                                    <td id="td-total" colspan="3">Total Segmento {baixas[x].descSeg}</td>
                                    <td></td>
                                    <td></td>
                                    <td></td>
                                    <td style='text-align: right;'>{filtroValor(somaValor)}</td>
                                    <td style='text-align: right;'>{filtroValor(somaDesc)}</td>
                                    <td style='text-align: right;'>{filtroValor(somaJuros)}</td>
                                    <td style='text-align: right;'>{filtroValor(somaReceb)}</td>
                                    <td style='text-align: right;'>{filtroValor(somaComi)}</td>
                                    </tr>
                                    """)
        somaTotal += somaValor
        somaToatalComi += somaComi
        somaTotalReceb += somaReceb
        somaTotalJuros += somaJuros
        somaTotalDesc += somaDesc
        somaValor = 0
        somaComi = 0
        somaReceb = 0
        somaJuros = 0
        somaDesc = 0
        html.write(f"""
                            <tr id="tr-total">
                            <td id="td-total">Total Geral</td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td style='text-align: right;'>{filtroValor(somaTotal)}</td>
                            <td style='text-align: right;'>{filtroValor(somaTotalDesc)}</td>
                            <td style='text-align: right;'>{filtroValor(somaTotalJuros)}</td>
                            <td style='text-align: right;'>{filtroValor(somaTotalReceb)}</td>
                            <td style='text-align: right;'>{filtroValor(somaToatalComi)}</td>
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
def htmlRecebPeriodo(baixas, linhas):
    caminho = get_path(__name__)
    pasta = f"{caminho}/app/templates/impressoes"
    shutil.rmtree(pasta, ignore_errors=False, onerror=None)
    
    with open(f"{caminho}/app/templates/baseImpressao/baseRecebidos.html", "r+", encoding='utf-8') as html:
        htmlBase = html.read()
        html.flush()
        
    os.makedirs(pasta)
    hora = datetime.now().strftime("%H:%M:%S")
    
    nomeHtml = f"impressaoRecebidos{hora}.html".replace(":", "")
    
    with open(f"{caminho}/app/templates/impressoes/{nomeHtml}", "a+", encoding='utf-8') as html:
        html.write(htmlBase)
        somaValor = 0
        somaComi = 0
        somaReceb = 0
        somaJuros = 0
        somaDesc = 0
        somaTotal = 0
        somaToatalComi = 0
        somaTotalReceb = 0
        somaTotalJuros = 0
        somaTotalDesc = 0
        for x in range(0, linhas):
            if x < linhas-1:
                somaValor += filtroFloat(baixas[x].m_valor)
                somaComi += filtroFloat(baixas[x].comissao)
                somaReceb += filtroFloat(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)
                somaJuros += filtroFloat(baixas[x].m_juros)
                somaDesc += filtroFloat(baixas[x].m_deconto)
                if baixas[x].m_dataBaixa != baixas[x+1].m_dataBaixa:
                    html.write(f"""<tr">
                                    <td id="nota">{filtroData(baixas[x].m_dataBaixa)}</td>
                                    <td>{baixas[x].m_numDoc} / {baixas[x].m_parcela}</td>
                                    <td>{baixas[x].m_docRef}</td>
                                    <td>{filtroNome(baixas[x].cliente)}</td>
                                    <td>{filtroNome(baixas[x].vendedor)}</td>
                                    <td>{filtroTipoBaixa(baixas[x].m_tipoBaixa)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_deconto)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_juros)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)}</td>
                                    <td id="valor" style='text-align: right;'>{filtroValor(baixas[x].comissao)}</td>
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
                                <td style='text-align: right;'>{filtroValor(somaDesc)}</td>
                                <td style='text-align: right;'>{filtroValor(somaJuros)}</td>
                                <td style='text-align: right;'>{filtroValor(somaReceb)}</td>
                                <td style='text-align: right;'>{filtroValor(somaComi)}</td>
                                </tr>
                                """)
                    somaTotal += somaValor
                    somaToatalComi += somaComi
                    somaTotalReceb += somaReceb
                    somaTotalJuros += somaJuros
                    somaTotalDesc += somaDesc
                    somaValor = 0
                    somaComi = 0
                    somaReceb = 0
                    somaJuros = 0
                    somaDesc = 0
                else:
                    html.write(f"""<tr>
                                    <td id="nota">{filtroData(baixas[x].m_dataBaixa)}</td>
                                    <td>{baixas[x].m_numDoc} / {baixas[x].m_parcela}</td>
                                    <td>{baixas[x].m_docRef}</td>
                                    <td>{filtroNome(baixas[x].cliente)}</td>
                                    <td>{filtroNome(baixas[x].vendedor)}</td>
                                    <td>{filtroTipoBaixa(baixas[x].m_tipoBaixa)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_deconto)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_juros)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)}</td>
                                    <td id="valor" style='text-align: right;'>{filtroValor(baixas[x].comissao)}</td>
                                    </tr>""")
            if x == linhas-1:
                somaValor += filtroFloat(baixas[x].m_valor)
                somaComi += filtroFloat(baixas[x].comissao)
                somaReceb += filtroFloat(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)
                somaJuros += filtroFloat(baixas[x].m_juros)
                somaDesc += filtroFloat(baixas[x].m_deconto)
                html.write(f"""<tr>
                                    <td id="nota">{filtroData(baixas[x].m_dataBaixa)}</td>
                                    <td>{baixas[x].m_numDoc} / {baixas[x].m_parcela}</td>
                                    <td>{baixas[x].m_docRef}</td>
                                    <td>{filtroNome(baixas[x].cliente)}</td>
                                    <td>{filtroNome(baixas[x].vendedor)}</td>
                                    <td>{filtroTipoBaixa(baixas[x].m_tipoBaixa)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_deconto)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_juros)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)}</td>
                                    <td id="valor" style='text-align: right;'>{filtroValor(baixas[x].comissao)}</td>
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
                                <td style='text-align: right;'>{filtroValor(somaDesc)}</td>
                                <td style='text-align: right;'>{filtroValor(somaJuros)}</td>
                                <td style='text-align: right;'>{filtroValor(somaReceb)}</td>
                                <td style='text-align: right;'>{filtroValor(somaComi)}</td>
                                </tr>
                                """)
        somaTotal += somaValor
        somaToatalComi += somaComi
        somaTotalReceb += somaReceb
        somaTotalJuros += somaJuros
        somaTotalDesc += somaDesc
        somaValor = 0
        somaComi = 0
        somaReceb = 0
        somaJuros = 0
        somaDesc = 0
        html.write(f"""
                            <tr id="tr-total-geral">
                            <td id="td-total">Total Geral</td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td style='text-align: right;'>{filtroValor(somaTotal)}</td>
                            <td style='text-align: right;'>{filtroValor(somaTotalDesc)}</td>
                            <td style='text-align: right;'>{filtroValor(somaTotalJuros)}</td>
                            <td style='text-align: right;'>{filtroValor(somaTotalReceb)}</td>
                            <td style='text-align: right;'>{filtroValor(somaToatalComi)}</td>
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
def htmlRecebVend(baixas, linhas):
    caminho = get_path(__name__)
    pasta = f"{caminho}/app/templates/impressoes"
    shutil.rmtree(pasta, ignore_errors=False, onerror=None)
    
    with open(f"{caminho}/app/templates/baseImpressao/baseRecebidosCliVend.html", "r+", encoding='utf-8') as html:
        htmlBase = html.read()
        html.flush()
    
    os.makedirs(pasta)
    hora = datetime.now().strftime("%H:%M:%S")
    
    nomeHtml = f"impressaoRecebidos{hora}.html".replace(":", "")
    
    with open(f"{caminho}/app/templates/impressoes/{nomeHtml}", "a+", encoding='utf-8') as html:
        html.write(htmlBase)
        somaValor = 0
        somaComi = 0
        somaReceb = 0
        somaJuros = 0
        somaDesc = 0
        somaTotal = 0
        somaToatalComi = 0
        somaTotalReceb = 0
        somaTotalJuros = 0
        somaTotalDesc = 0
        for x in range(0, linhas):
            if x < linhas-1:
                somaValor += filtroFloat(baixas[x].m_valor)
                somaComi += filtroFloat(baixas[x].comissao)
                somaReceb += filtroFloat(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)
                somaJuros += filtroFloat(baixas[x].m_juros)
                somaDesc += filtroFloat(baixas[x].m_deconto)
                if baixas[x].m_dataBaixa != baixas[x+1].m_dataBaixa:
                    html.write(f"""<tr>
                                    <td id="nota">{filtroData(baixas[x].m_dataBaixa)}</td>
                                    <td>{baixas[x].m_numDoc} / {baixas[x].m_parcela}</td>
                                    <td>{baixas[x].m_docRef}</td>
                                    <td>{filtroNome(baixas[x].cliente)}</td>
                                    <td>{filtroTipoBaixa(baixas[x].m_tipoBaixa)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_deconto)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_juros)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)}</td>
                                    <td id="valor" style='text-align: right;'>{filtroValor(baixas[x].comissao)}</td>
                                    </tr>""")
                    html.write(f"""
                                <tr id="tr-total">
                                <td id="td-total">Total Dia</td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td style='text-align: right;'>{filtroValor(somaValor)}</td>
                                <td style='text-align: right;'>{filtroValor(somaDesc)}</td>
                                <td style='text-align: right;'>{filtroValor(somaJuros)}</td>
                                <td style='text-align: right;'>{filtroValor(somaReceb)}</td>
                                <td style='text-align: right;'>{filtroValor(somaComi)}</td>
                                </tr>
                                """)
                    somaTotal += somaValor
                    somaToatalComi += somaComi
                    somaTotalReceb += somaReceb
                    somaTotalJuros += somaJuros
                    somaTotalDesc += somaDesc
                    somaValor = 0
                    somaComi = 0
                    somaReceb = 0
                    somaJuros = 0
                    somaDesc = 0
                else:
                    html.write(f"""<tr>
                                    <td id="nota">{filtroData(baixas[x].m_dataBaixa)}</td>
                                    <td>{baixas[x].m_numDoc} / {baixas[x].m_parcela}</td>
                                    <td>{baixas[x].m_docRef}</td>
                                    <td>{filtroNome(baixas[x].cliente)}</td>
                                    <td>{filtroTipoBaixa(baixas[x].m_tipoBaixa)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_deconto)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_juros)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)}</td>
                                    <td id="valor" style='text-align: right;'>{filtroValor(baixas[x].comissao)}</td>
                                    </tr>""")
            if x == linhas-1:
                somaValor += filtroFloat(baixas[x].m_valor)
                somaComi += filtroFloat(baixas[x].comissao)
                somaReceb += filtroFloat(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)
                somaJuros += filtroFloat(baixas[x].m_juros)
                somaDesc += filtroFloat(baixas[x].m_deconto)
                html.write(f"""<tr>
                                    <td id="nota">{filtroData(baixas[x].m_dataBaixa)}</td>
                                    <td>{baixas[x].m_numDoc} / {baixas[x].m_parcela}</td>
                                    <td>{baixas[x].m_docRef}</td>
                                    <td>{filtroNome(baixas[x].cliente)}</td>
                                    <td>{filtroTipoBaixa(baixas[x].m_tipoBaixa)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_deconto)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_juros)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)}</td>
                                    <td id="valor" style='text-align: right;'>{filtroValor(baixas[x].comissao)}</td>
                                    </tr>""")
                html.write(f"""
                                <tr id="tr-total">
                                <td id="td-total">Total Dia</td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td style='text-align: right;'>{filtroValor(somaValor)}</td>
                                <td style='text-align: right;'>{filtroValor(somaDesc)}</td>
                                <td style='text-align: right;'>{filtroValor(somaJuros)}</td>
                                <td style='text-align: right;'>{filtroValor(somaReceb)}</td>
                                <td style='text-align: right;'>{filtroValor(somaComi)}</td>
                                </tr>
                                """)
        somaTotal += somaValor
        somaToatalComi += somaComi
        somaTotalReceb += somaReceb
        somaTotalJuros += somaJuros
        somaTotalDesc += somaDesc
        somaValor = 0
        somaComi = 0
        somaReceb = 0
        somaJuros = 0
        somaDesc = 0
        html.write(f"""
                            <tr id="tr-total-geral">
                            <td id="td-total">Total Geral</td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td style='text-align: right;'>{filtroValor(somaTotal)}</td>
                            <td style='text-align: right;'>{filtroValor(somaTotalDesc)}</td>
                            <td style='text-align: right;'>{filtroValor(somaTotalJuros)}</td>
                            <td style='text-align: right;'>{filtroValor(somaTotalReceb)}</td>
                            <td style='text-align: right;'>{filtroValor(somaToatalComi)}</td>
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
def htmlRecebCli(baixas, linhas):
    caminho = get_path(__name__)
    pasta = f"{caminho}/app/templates/impressoes"
    shutil.rmtree(pasta, ignore_errors=False, onerror=None)
    
    with open(f"{caminho}/app/templates/baseImpressao/baseRecebidosCliVend.html", "r+", encoding='utf-8') as html:
        htmlBase = html.read()
        html.flush()
    
    os.makedirs(pasta)
    hora = datetime.now().strftime("%H:%M:%S")
    
    nomeHtml = f"impressaoRecebidos{hora}.html".replace(":", "")
    with open(f"{caminho}/app/templates/impressoes/{nomeHtml}", "a+", encoding='utf-8') as html:
        html.write(htmlBase)
        somaValor = 0
        somaComi = 0
        somaReceb = 0
        somaJuros = 0
        somaDesc = 0
        somaTotal = 0
        somaToatalComi = 0
        somaTotalReceb = 0
        somaTotalJuros = 0
        somaTotalDesc = 0
        for x in range(0, linhas):
            if x < linhas-1:
                somaValor += filtroFloat(baixas[x].m_valor)
                somaComi += filtroFloat(baixas[x].comissao)
                somaReceb += filtroFloat(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)
                somaJuros += filtroFloat(baixas[x].m_juros)
                somaDesc += filtroFloat(baixas[x].m_deconto)
                if baixas[x].m_dataBaixa != baixas[x+1].m_dataBaixa:
                    html.write(f"""<tr>
                                    <td id="nota">{filtroData(baixas[x].m_dataBaixa)}</td>
                                    <td>{baixas[x].m_numDoc} / {baixas[x].m_parcela}</td>
                                    <td>{baixas[x].m_docRef}</td>
                                    <td>{filtroNome(baixas[x].vendedor)}</td>
                                    <td>{filtroTipoBaixa(baixas[x].m_tipoBaixa)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_deconto)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_juros)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)}</td>
                                    <td id="valor" style='text-align: right;'>{filtroValor(baixas[x].comissao)}</td>
                                    </tr>""")
                    html.write(f"""
                                <tr id="tr-total">
                                <td id="td-total">Total Dia</td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td style='text-align: right;'>{filtroValor(somaValor)}</td>
                                <td style='text-align: right;'>{filtroValor(somaDesc)}</td>
                                <td style='text-align: right;'>{filtroValor(somaJuros)}</td>
                                <td style='text-align: right;'>{filtroValor(somaReceb)}</td>
                                <td style='text-align: right;'>{filtroValor(somaComi)}</td>
                                </tr>
                                """)
                    somaTotal += somaValor
                    somaToatalComi += somaComi
                    somaTotalReceb += somaReceb
                    somaTotalJuros += somaJuros
                    somaTotalDesc += somaDesc
                    somaValor = 0
                    somaComi = 0
                    somaReceb = 0
                    somaJuros = 0
                    somaDesc = 0
                else:
                    html.write(f"""<tr>
                                    <td id="nota">{filtroData(baixas[x].m_dataBaixa)}</td>
                                    <td>{baixas[x].m_numDoc} / {baixas[x].m_parcela}</td>
                                    <td>{baixas[x].m_docRef}</td>
                                    <td>{filtroNome(baixas[x].vendedor)}</td>
                                    <td>{filtroTipoBaixa(baixas[x].m_tipoBaixa)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_deconto)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_juros)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)}</td>
                                    <td id="valor" style='text-align: right;'>{filtroValor(baixas[x].comissao)}</td>
                                    </tr>""")
            if x == linhas-1:
                somaValor += filtroFloat(baixas[x].m_valor)
                somaComi += filtroFloat(baixas[x].comissao)
                somaReceb += filtroFloat(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)
                somaJuros += filtroFloat(baixas[x].m_juros)
                somaDesc += filtroFloat(baixas[x].m_deconto)
                html.write(f"""<tr>
                                    <td id="nota">{filtroData(baixas[x].m_dataBaixa)}</td>
                                    <td>{baixas[x].m_numDoc} / {baixas[x].m_parcela}</td>
                                    <td>{baixas[x].m_docRef}</td>
                                    <td>{filtroNome(baixas[x].vendedor)}</td>
                                    <td>{filtroTipoBaixa(baixas[x].m_tipoBaixa)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_deconto)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_juros)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)}</td>
                                    <td id="valor" style='text-align: right;'>{filtroValor(baixas[x].comissao)}</td>
                                    </tr>""")
                html.write(f"""
                                <tr id="tr-total">
                                <td id="td-total">Total Dia</td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td style='text-align: right;'>{filtroValor(somaValor)}</td>
                                <td style='text-align: right;'>{filtroValor(somaDesc)}</td>
                                <td style='text-align: right;'>{filtroValor(somaJuros)}</td>
                                <td style='text-align: right;'>{filtroValor(somaReceb)}</td>
                                <td style='text-align: right;'>{filtroValor(somaComi)}</td>
                                </tr>
                                """)
        somaTotal += somaValor
        somaToatalComi += somaComi
        somaTotalReceb += somaReceb
        somaTotalJuros += somaJuros
        somaTotalDesc += somaDesc
        somaValor = 0
        somaComi = 0
        somaReceb = 0
        somaJuros = 0
        somaDesc = 0
        html.write(f"""
                            <tr id="tr-total-geral">
                            <td id="td-total">Total Geral</td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td style='text-align: right;'>{filtroValor(somaTotal)}</td>
                            <td style='text-align: right;'>{filtroValor(somaTotalDesc)}</td>
                            <td style='text-align: right;'>{filtroValor(somaTotalJuros)}</td>
                            <td style='text-align: right;'>{filtroValor(somaTotalReceb)}</td>
                            <td style='text-align: right;'>{filtroValor(somaToatalComi)}</td>
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
def htmlRecebPeriodoMes(baixas, linhas):
    caminho = get_path(__name__)
    pasta = f"{caminho}/app/templates/impressoes"
    shutil.rmtree(pasta, ignore_errors=False, onerror=None)
    
    with open(f"{caminho}/app/templates/baseImpressao/baseRecebidosMes.html", "r+", encoding='utf-8') as html:
        htmlBase = html.read()
        html.flush()
        
    os.makedirs(pasta)
    hora = datetime.now().strftime("%H:%M:%S")
    
    nomeHtml = f"impressaoRecebidos{hora}.html".replace(":", "")
    
    with open(f"{caminho}/app/templates/impressoes/{nomeHtml}", "a+", encoding='utf-8') as html:
        html.write(htmlBase)
        somaValor = 0
        somaReceb = 0
        somaJuros = 0
        somaDesc = 0
        somaTotal = 0
        somaTotalReceb = 0
        somaTotalJuros = 0
        somaTotalDesc = 0
        for x in range(0, linhas):
            if x < linhas-1:
                somaValor += filtroFloat(baixas[x].m_valor)
                somaReceb += filtroFloat(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)
                somaJuros += filtroFloat(baixas[x].m_juros)
                somaDesc += filtroFloat(baixas[x].m_deconto)
                if baixas[x].m_dataBaixa[4:6] != baixas[x+1].m_dataBaixa[4:6]:
                    html.write(f"""<tr">
                                    <td id="nota">{filtroData(baixas[x].m_dataBaixa)}</td>
                                    <td>{filtroData(baixas[x].lancamento)}</td>
                                    <td>{baixas[x].m_numDoc} / {baixas[x].m_parcela}</td>
                                    <td>{baixas[x].m_docRef}</td>
                                    <td>{filtroNome(baixas[x].cliente)}</td>
                                    <td>{filtroNome(baixas[x].vendedor)}</td>
                                    <td>{filtroTipoBaixa(baixas[x].m_tipoBaixa)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_deconto)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_juros)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)}</td>
                                    </tr>""")
                    html.write(f"""
                                <tr id="tr-total">
                                <td id="td-total">Total Mes</td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                               <td></td>
                                <td style='text-align: right;'>{filtroValor(somaValor)}</td>
                                <td style='text-align: right;'>{filtroValor(somaDesc)}</td>
                                <td style='text-align: right;'>{filtroValor(somaJuros)}</td>
                                <td style='text-align: right;'>{filtroValor(somaReceb)}</td>
                                </tr>
                                """)
                    somaTotal += somaValor
                    somaTotalReceb += somaReceb
                    somaTotalJuros += somaJuros
                    somaTotalDesc += somaDesc
                    somaValor = 0
                    somaReceb = 0
                    somaJuros = 0
                    somaDesc = 0
                else:
                    html.write(f"""<tr>
                                    <td id="nota">{filtroData(baixas[x].m_dataBaixa)}</td>
                                    <td>{filtroData(baixas[x].lancamento)}</td>
                                    <td>{baixas[x].m_numDoc} / {baixas[x].m_parcela}</td>
                                    <td>{baixas[x].m_docRef}</td>
                                    <td>{filtroNome(baixas[x].cliente)}</td>
                                    <td>{filtroNome(baixas[x].vendedor)}</td>
                                    <td>{filtroTipoBaixa(baixas[x].m_tipoBaixa)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_deconto)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_juros)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)}</td>
                                    </tr>""")
            if x == linhas-1:
                somaValor += filtroFloat(baixas[x].m_valor)
                somaReceb += filtroFloat(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)
                somaJuros += filtroFloat(baixas[x].m_juros)
                somaDesc += filtroFloat(baixas[x].m_deconto)
                html.write(f"""<tr>
                                    <td id="nota">{filtroData(baixas[x].m_dataBaixa)}</td>
                                    <td>{filtroData(baixas[x].lancamento)}</td>
                                    <td>{baixas[x].m_numDoc} / {baixas[x].m_parcela}</td>
                                    <td>{baixas[x].m_docRef}</td>
                                    <td>{filtroNome(baixas[x].cliente)}</td>
                                    <td>{filtroNome(baixas[x].vendedor)}</td>
                                    <td>{filtroTipoBaixa(baixas[x].m_tipoBaixa)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_deconto)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_juros)}</td>
                                    <td style='text-align: right;'>{filtroValor(baixas[x].m_valor + baixas[x].m_juros - baixas[x].m_deconto)}</td>
                                    </tr>""")
                html.write(f"""
                                <tr id="tr-total">
                                <td id="td-total">Total Mes</td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td style='text-align: right;'>{filtroValor(somaValor)}</td>
                                <td style='text-align: right;'>{filtroValor(somaDesc)}</td>
                                <td style='text-align: right;'>{filtroValor(somaJuros)}</td>
                                <td style='text-align: right;'>{filtroValor(somaReceb)}</td>
                                </tr>
                                """)
        somaTotal += somaValor
        somaTotalReceb += somaReceb
        somaTotalJuros += somaJuros
        somaTotalDesc += somaDesc
        somaValor = 0
        somaReceb = 0
        somaJuros = 0
        somaDesc = 0
        html.write(f"""
                            <tr id="tr-total-geral">
                            <td id="td-total">Total Geral</td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td style='text-align: right;'>{filtroValor(somaTotal)}</td>
                            <td style='text-align: right;'>{filtroValor(somaTotalDesc)}</td>
                            <td style='text-align: right;'>{filtroValor(somaTotalJuros)}</td>
                            <td style='text-align: right;'>{filtroValor(somaTotalReceb)}</td>
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