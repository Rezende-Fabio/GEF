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
            valor: gridjs.html(`<span style='display:flex; text-align: right; justify-content: right;align-items: center; margin-right: 15px;'>` + resp[x].valor + `</span>`),
            vizualizar: gridjs.html(`<div style="width: 100%;display: flex;align-items: center;text-align: center;justify-content: center;"><a href="/lista-observacoes/view/${resp[x].doc}/${resp[x].par}" class="btn btn-outline-primary btn-sm"><i class="fa-solid fa-eye" style="font-size: 17px;"></i></a></div>`)
           }
           dataObserv.push(dataresp)
        }
    }
});

var columnsObserv = [
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
        id: 'emissao',
        name: "Emissão",
        sort: false,
    },
    {
        id: 'valor',
        name: gridjs.html(`<span style='display:flex; text-align: right; justify-content: right;align-items: center; margin-right: 15px;'>Valor</span>`),
        width: "120px",
        sort: false,
    },
    {
        id: 'vizualizar',
        name: gridjs.html("<span style='display:flex; text-align: center; justify-content: center;align-items: center;'>Vizualizar</span>"),
        width: "120px",
        sort: false,
    }
]