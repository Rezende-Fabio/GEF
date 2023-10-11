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
                estornar: gridjs.html(`<div style="width: 100%;display: flex;align-items: center;text-align: center;justify-content: center;"><a href="/deletar-baixa/${resp[x].doc}/${resp[x].par}" class="btn btn-outline-danger btn-sm"><i class="fa-solid fa-circle-up"></i> Estornar</a></div>`)
           }
           dataEstorn.push(dataresp)
        }
    }
});

var columnsEstorn = [
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
        id: 'estornar',
        name: gridjs.html("<span style='display:flex; text-align: center; justify-content: center;align-items: center;'>Estornar</span>"),
        width: "120px",
        sort: false,
    }
]
