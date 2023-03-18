var dataBiax = []

$.ajax({
    url: '/baixas',
    type: 'POST',
    async: false,
    dataType: 'json',
    contentType: 'application/json',
    success: function(resp){
        for(x in resp){
           dataresp = {
            ref: resp[x].ref,
            documento: resp[x].doc,
            par: resp[x].par,
            cliente: resp[x].cli,
            vendedor: resp[x].vend,
            emissão: resp[x].lanc,
            vencimento: resp[x].venc,
            valor: `<span style='display:flex; text-align: right; justify-content: right;align-items: center; margin-right: 15px;'>` + resp[x].saldo + `</span>`, 
            baixar: `<div style="width: 100%;display: flex;align-items: center;text-align: center;justify-content: center;"><a href="/cad-baixa/${resp[x].doc}/${resp[x].par}" style='text-align: center; justify-content: center;' class="btn btn-outline-success btn-sm"><i class="fa-solid fa-circle-down"></i> Baixar</a></div>`
            }
           dataBiax.push(dataresp)
        }
    }
});

var columnsBaix = {
    ref: 'Ref.',
    documento: 'Documento',
    par: 'Par.',
    cliente: 'Cliente',
    vendedor: 'Vendedor',
    emissão: 'Emissão',
    vencimento: "Vencimento",
    valor: `<span style='display:flex; text-align: right; justify-content: right;align-items: center; margin-right: 15px;'>Valor</span>`,
    baixar: "<span style='display:flex; text-align: center; justify-content: center;align-items: center;'>Baixar</span>"
}
