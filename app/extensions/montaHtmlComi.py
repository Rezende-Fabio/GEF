import os
import shutil
from datetime import datetime
from app.extensions.configHtml import *
from ..models.Models import *

##################################################################
# Monta o HTML de comissão geral para a impressão
##################################################################
def htmlComissao(comissoes, linhas):
    caminho = get_path(__name__)
    pasta = f"{caminho}/app/templates/impressoes"
    shutil.rmtree(pasta, ignore_errors=False, onerror=None)
    
    with open(f"{caminho}/app/templates/baseImpressao/baseComissao.html", "r+", encoding='utf-8') as html:
        htmlBase = html.read()
        html.flush()
    
    os.makedirs(pasta)
    hora = datetime.now().strftime("%H:%M:%S")
    
    nomeHtml = f"impressaoComi{hora}.html".replace(":", "")
                   
    with open(f"{caminho}/app/templates/impressoes/{nomeHtml}", "a+", encoding='utf-8') as html:
        html.write(htmlBase)
        somaValor = 0
        somaTotal = 0
        for x in range(0, linhas):
            if x < linhas-1:
                somaValor += filtroFloat(comissoes[x].c_valor)
                if comissoes[x].segmento != comissoes[x+1].segmento:
                    html.write(f"""<tr>
                                <td id="nota">{comissoes[x].c_docRef}</td>
                                <td>{comissoes[x].c_numDoc} / {comissoes[x].parcela}</td>
                                <td>{filtroNome(comissoes[x].cliente)}</td>
                                <td>{filtroTipoBaixa(comissoes[x].tipoBaixa)}</td>
                                <td>{filtroData(comissoes[x].c_dataBaixa)}</td>
                                <td style='text-align: right;'>{filtroValor(comissoes[x].c_baseCalc)}</td>
                                <td style='text-align: right;'>{filtroFloat(comissoes[x].c_perc)} %</td>
                                <td id="valor" style='text-align: right;'>{filtroValor(comissoes[x].c_valor)}</td>
                                </tr>""")
                    html.write(f"""
                                <tr id="tr-total">
                                <td id="td-total">Total Segmento</td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td style='text-align: right;'>{filtroValor(somaValor)}</td>
                                </tr>
                                """)
                    somaTotal += somaValor
                    somaValor = 0
                else:
                    html.write(f"""<tr>
                                <td id="nota">{comissoes[x].c_docRef}</td>
                                <td>{comissoes[x].c_numDoc} / {comissoes[x].parcela}</td>
                                <td>{filtroNome(comissoes[x].cliente)}</td>
                                <td>{filtroTipoBaixa(comissoes[x].tipoBaixa)}</td>
                                <td>{filtroData(comissoes[x].c_dataBaixa)}</td>
                                <td style='text-align: right;'>{filtroValor(comissoes[x].c_baseCalc)}</td>
                                <td style='text-align: right;'>{filtroFloat(comissoes[x].c_perc)} %</td>
                                <td id="valor" style='text-align: right;'>{filtroValor(comissoes[x].c_valor)}</td>  
                                </tr>""")
            if x == linhas-1:
                somaValor += filtroFloat(comissoes[x].c_valor)
                html.write(f"""<tr>
                                    <td id="nota">{comissoes[x].c_docRef}</td>
                                    <td>{comissoes[x].c_numDoc} / {comissoes[x].parcela}</td>
                                    <td>{filtroNome(comissoes[x].cliente)}</td>
                                    <td>{filtroTipoBaixa(comissoes[x].tipoBaixa)}</td>
                                    <td>{filtroData(comissoes[x].c_dataBaixa)}</td>
                                    <td style='text-align: right;'>{filtroValor(comissoes[x].c_baseCalc)}</td>
                                    <td style='text-align: right;'>{filtroFloat(comissoes[x].c_perc)} %</td>
                                    <td id="valor" style='text-align: right;'>{filtroValor(comissoes[x].c_valor)}</td>
                                    </tr>""")
                html.write(f"""
                            <tr id="tr-total">
                            <td id="td-total">Total Segmento</td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td style='text-align: right;'>{filtroValor(somaValor)}</td>
                            </tr>
                            """)
        somaTotal += somaValor
        somaValor = 0
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
# Monta o HTML de comissão por vendedor para a impressão
##################################################################
def htmlComissaoVend(listaVend, dataDe, dataAte):
    caminho = get_path(__name__)
    pasta = f"{caminho}/app/templates/impressoes"
    shutil.rmtree(pasta, ignore_errors=False, onerror=None)
    
    with open(f"{caminho}/app/templates/baseImpressao/baseComissaoVend.html", "r+", encoding='utf-8') as html:
        htmlBase = html.read()
        html.flush()
    
    os.makedirs(pasta)
    hora = datetime.now().strftime("%H:%M:%S")
    
    nomeHtml = f"impressaoComi{hora}.html".replace(":", "")
                   
    with open(f"{caminho}/app/templates/impressoes/{nomeHtml}", "a+", encoding='utf-8') as html:
        html.write(htmlBase)
        conexao = Gf3005
        conexao2 = Gf3001
        conexao3 = Gf3002
        conexao4 = Gf3006
        conexao5 = Gf3003
        valorTotal = 0
        for idVend in listaVend:
            comissoes = DB.session.query(conexao.c_baseCalc, conexao.c_valor, conexao.c_perc, conexao.c_dataBaixa, conexao.c_docRef, conexao.c_numDoc, conexao4.m_parcela.label("parcela"),
                                                    conexao4.m_tipoBaixa.label('tipoBaixa'), conexao2.c_razaosocial.label('cliente'), conexao5.s_abrev.label('segmento'), conexao5.s_desc.label("decSeg"), conexao3.v_nome.label("vendedor")).join(conexao4, conexao4.m_id == conexao.c_idBaixa).join(conexao2, conexao2.c_id == conexao4.m_idCliente).join(conexao5, conexao5.s_id == conexao4.m_segmento).join(conexao3, conexao.c_idVendedor==conexao3.v_id).filter(
                                                                                                                                                                                                                                                                                                                                            conexao.c_ativo==1, conexao.c_dataBaixa>=dataDe, conexao.c_dataBaixa<=dataAte, conexao.c_idVendedor==idVend).order_by(conexao3.v_nome, conexao.c_docRef, conexao.c_dataBaixa)
            linhas = DB.session.query(conexao.c_baseCalc, conexao.c_valor, conexao.c_perc, conexao.c_dataBaixa, conexao.c_docRef, conexao.c_numDoc,
                                            conexao4.m_tipoBaixa.label('tipoBaixa'), conexao2.c_razaosocial.label('cliente'), conexao5.s_abrev.label('segmento'), conexao5.s_desc.label("decSeg"), conexao3.v_nome.label("vendedor")).join(conexao4, conexao4.m_id == conexao.c_idBaixa).join(conexao2, conexao2.c_id == conexao4.m_idCliente).join(conexao5, conexao5.s_id == conexao4.m_segmento).join(conexao3, conexao.c_idVendedor==conexao3.v_id).filter(
                                                                                                                                                                                                                                                                                                                                    conexao.c_ativo==1, conexao.c_dataBaixa>=dataDe, conexao.c_dataBaixa<=dataAte, conexao.c_idVendedor==idVend).order_by(conexao3.v_nome, conexao.c_docRef, conexao.c_dataBaixa).count()
            
            html.write(f"""
                <div class="header-vend">
                    <h5>Vendedor: {comissoes[0].vendedor}</h5>
                </div>
                    """)
            html.write("""<table class='table' id="table">
                    <thead>
                        <tr>
                            <th style="width: 12%;">Ref.</th>
                            <th style="width: 10%;">No. Doc.</th>
                            <th>Cliente</th>
                            <th>Tp. Baixa</th>
                            <th>Data Baixa</th>
                            <th style="width: 10%; text-align: right;">Base</th>
                            <th style="width: 10%; text-align: right;">% Comis.</th>
                            <th style="width: 10%; text-align: right;">Valor</th>
                        </tr>
                    </thead>
                    <tbody id="tbody">""")
            somaValor = 0
            somaTotal = 0
            for x in range(0, linhas):  
                if x < linhas-1:
                    somaValor += filtroFloat(comissoes[x].c_valor)
                    if comissoes[x].segmento != comissoes[x+1].segmento:
                        html.write(f"""<tr>
                                    <td id="nota">{comissoes[x].c_docRef}</td>
                                    <td>{comissoes[x].c_numDoc} / {comissoes[x].parcela}</td>
                                    <td>{filtroNome(comissoes[x].cliente)}</td>
                                    <td>{filtroTipoBaixa(comissoes[x].tipoBaixa)}</td>
                                    <td>{filtroData(comissoes[x].c_dataBaixa)}</td>
                                    <td style='text-align: right;'>{filtroValor(comissoes[x].c_baseCalc)}</td>
                                    <td style='text-align: right;'>{filtroFloat(comissoes[x].c_perc)} %</td>
                                    <td id="valor" style='text-align: right;'>{filtroValor(comissoes[x].c_valor)}</td>
                                    </tr>""")
                        html.write(f"""
                                    <tr id="tr-total">
                                    <td id="td-total" colspan="3">Total Segmento {comissoes[x].decSeg}</td>
                                    <td></td>
                                    <td></td>
                                    <td></td>
                                    <td></td>
                                    <td style='text-align: right;'>{filtroValor(somaValor)}</td>
                                    </tr>
                                    """)
                        somaTotal += somaValor
                        valorTotal += somaValor
                        somaValor = 0
                    else:
                        html.write(f"""<tr>
                                    <td id="nota">{comissoes[x].c_docRef}</td>
                                    <td>{comissoes[x].c_numDoc} / {comissoes[x].parcela}</td>
                                    <td>{filtroNome(comissoes[x].cliente)}</td>
                                    <td>{filtroTipoBaixa(comissoes[x].tipoBaixa)}</td>
                                    <td>{filtroData(comissoes[x].c_dataBaixa)}</td>
                                    <td style='text-align: right;'>{filtroValor(comissoes[x].c_baseCalc)}</td>
                                    <td style='text-align: right;'>{filtroFloat(comissoes[x].c_perc)} %</td>
                                    <td id="valor" style='text-align: right;'>{filtroValor(comissoes[x].c_valor)}</td>  
                                    </tr>""")
                if x == linhas-1:
                    somaValor += filtroFloat(comissoes[x].c_valor)
                    html.write(f"""<tr>
                                        <td id="nota">{comissoes[x].c_docRef}</td>
                                        <td>{comissoes[x].c_numDoc} / {comissoes[x].parcela}</td>
                                        <td>{filtroNome(comissoes[x].cliente)}</td>
                                        <td>{filtroTipoBaixa(comissoes[x].tipoBaixa)}</td>
                                        <td>{filtroData(comissoes[x].c_dataBaixa)}</td>
                                        <td style='text-align: right;'>{filtroValor(comissoes[x].c_baseCalc)}</td>
                                        <td style='text-align: right;'>{filtroFloat(comissoes[x].c_perc)} %</td>
                                        <td id="valor" style='text-align: right;'>{filtroValor(comissoes[x].c_valor)}</td>
                                        </tr>""")
                    html.write(f"""
                                <tr id="tr-total">
                                <td id="td-total" colspan="3">Total Segmento {comissoes[x].decSeg}</td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td style='text-align: right;'>{filtroValor(somaValor)}</td>
                                </tr>
                                """)
            somaTotal += somaValor
            valorTotal += somaValor
            somaValor = 0
            html.write(f"""
                        <tr id="tr-total-geral">
                            <td id="td-total">Total Vendedor</td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td style='text-align: right;'>{filtroValor(somaTotal)}</td>
                        </tr>
                        </tbody>
                    </table>
                        """)
            
        html.write(f"""
                   <table class='table' id="table">
                   <tbody>
                        <tr id="tr-total-geral">
                            <td id="td-total">Total Geral</td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td style='text-align: right;'>{filtroValor(valorTotal)}</td>
                        </tr>
                    </tbody>
                    </table>
                   """)

        html.write("""
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