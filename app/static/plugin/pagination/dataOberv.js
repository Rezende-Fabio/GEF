var dataObserv = []

$.ajax({
    url: '/observacoes',
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
            emissao: resp[x].lanc,
            valor: `<span style='display:flex; text-align: right; justify-content: right;align-items: center; margin-right: 15px;'>` + resp[x].valor + `</span>`,
            vizualizar: `<div style="width: 100%;display: flex;align-items: center;text-align: center;justify-content: center;"><a href="/lista-observacoes/view/${resp[x].doc}/${resp[x].par}" class="btn btn-outline-primary btn-sm"><i class="fa-solid fa-eye" style="font-size: 17px;"></i></a></div>`
           }
           dataObserv.push(dataresp)
        }
    }
});

var columnsObserv = {
    ref: 'Ref.',
    documento: 'Documento',
    par: 'Parcela',
    cliente: 'Cliente',
    emissao: 'Emissão',
    valor: `<span style='display:flex; text-align: right; justify-content: right;align-items: center; margin-right: 15px;'>Valor</span>`,
    vizualizar: "<span style='display:flex; text-align: center; justify-content: center;align-items: center;'>Vizualizar</span>"
}
