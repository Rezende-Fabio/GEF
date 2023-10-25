var dataObserv = []

$.ajax({
    url: '/observacao/observacoes',
    type: 'GET',
    async: false,
    success: function(resp){
        for(x in resp){
           dataresp = {
            ref: resp[x].ref,
            documento: resp[x].doc,
            par: resp[x].par,
            cliente: resp[x].cli,
            emissao: resp[x].lanc,
            valor: gridjs.html(`<span style='display:flex; text-align: right; justify-content: right;align-items: center; margin-right: 15px;'>` + resp[x].valor + `</span>`),
            vizualizar: gridjs.html(`<div style="width: 100%;display: flex;align-items: center;text-align: center;justify-content: center;"><a class="abrirModal btn btn-primary" data-id="${resp[x].doc}/${resp[x].par}"><i class="fa-solid fa-eye" style="font-size: 17px;"></i></a></div>`)
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


new gridjs.Grid({
    columns: columnsObserv,
    data: () => {
        return new Promise(resolve => {
            setTimeout(() => resolve(dataObserv), 2000);
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
}).render(document.getElementById("lista-observacoes"));