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
                emissao: resp[x].lanc,
                vencimento: gridjs.html(resp[x].venc),
                valor: gridjs.html(`<span style='display:flex; text-align: right; justify-content: right;align-items: center; margin-right: 15px;'>${resp[x].saldo}</span>`), 
                baixar: gridjs.html(`<div style="width: 100%;display: flex;align-items: center;text-align: center;justify-content: center;"><a href="/cad-baixa/${resp[x].doc}/${resp[x].par}" style='text-align: center; justify-content: center; diplay: flex;' class="btn btn-outline-success btn-sm"><i class="fa-solid fa-circle-down"></i> Baixar</a></div>`)
            }
           dataBiax.push(dataresp)
        }
    }
});

var columnsBaix = [
    {
        id: 'ref',
        name: 'Ref.',
        width: "120px",
        sort: false,
    },
    {
        id: 'documento',
        name: "Doc.",
        width: "100px",
    },
    {
        id: 'par',
        name: "Par.",
        width: "74px",
        sort: false,
    },
    {
        id: 'cliente',
        name: "Cliente",
        width: "120px",
        sort: false,
    },
    {
        id: 'vendedor',
        name: "Vendedor",
        width: "120px",
        sort: false,
    },
    {
        id: 'emissao',
        name: "Emissão",
        sort: false,
    },
    {
        id: 'vencimento',
        name: "Vencimento",
        sort: false,
    },
    {
        id: 'valor',
        name: gridjs.html("<span style='display:flex; text-align: right; justify-content: right;align-items: center; margin-right: 15px;'>Valor</span>"),
        width: "150px",
        sort: false,
    },
    {
        id: 'baixar',
        name: gridjs.html("<span style='display:flex; text-align: center; justify-content: center;align-items: center;'>Baixar</span>"),
        width: "120px",
        sort: false,
    }
]