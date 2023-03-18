var dataEstorn = []

$.ajax({
    url: '/estornos',
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
            emissao: resp[x].lanc,
            vencimento: resp[x].venc,
            estornar: `<div style="width: 100%;display: flex;align-items: center;text-align: center;justify-content: center;"><a href="/deletar-baixa/${resp[x].doc}/${resp[x].par}" class="btn btn-outline-danger btn-sm"><i class="fa-solid fa-circle-up"></i> Estornar</a></div>`
           }
           dataEstorn.push(dataresp)
        }
    }
});

var columnsEstorn = {
    ref: 'Ref.',
    documento: 'Documento',
    par: 'Parcela',
    cliente: 'Cliente',
    vendedor: 'Vendedor',
    emissao: 'Emissão',
    vencimento: "Vencimento",
    estornar: "<span style='display:flex; text-align: center; justify-content: center;align-items: center;'>Estornar</span>"
}
