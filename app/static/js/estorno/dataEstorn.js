var dataEstorn = []

$.ajax({
    url: '/estorno/estornos',
    type: 'GET',
    async: false,
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
                estornar: gridjs.html(`<div style="width: 100%;display: flex;align-items: center;text-align: center;justify-content: center;"><button data-id="${resp[x].doc}/${resp[x].par}" class="abrirModal btn btn-danger btn-sm"><i class="fa-solid fa-circle-up"></i> Estornar</button></div>`)
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


new gridjs.Grid({
    columns: columnsEstorn,
    data: () => {
        return new Promise(resolve => {
            setTimeout(() => resolve(dataEstorn), 2000);
        });
    },
    search: {
        ignoreHiddenColumns: false,
    },
    sort: true,
    paginationAutoPageSize: true,
    pagination: true,
    style: {
        td: {
            'font-size': '13.5px'
        }
    },
}).render(document.getElementById("lista-baixas"));