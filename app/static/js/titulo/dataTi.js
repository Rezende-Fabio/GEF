var dataTi = []

$.ajax({
    url: '/titulos',
    type: 'POST',
    async: false,
    dataType: 'json',
    contentType: 'application/json',
    success: function(resp){
        for(x in resp){
           dataresp = {
                ref: resp[x].abrev + resp[x].ref,
                documento: resp[x].doc,
                par: resp[x].par,
                cpfCnpjVend: resp[x].cpfcnpjVend,
                cpfCnpjCli: resp[x].cpfcnpjCli,
                cliente: resp[x].cli,
                emissao: resp[x].lanc,  
                valor: gridjs.html(`<span style='display:flex; text-align: right; justify-content: right;align-items: center; margin-right: 7px;'>` + resp[x].total + `</span>`), 
                vizualizar: gridjs.html(`<div style="width: 100%;display: flex;align-items: center;text-align: center;justify-content: center;"><a data-id="${resp[x].doc}" class="abrirModal btn btn-primary btn-sm"><i class="fa-solid fa-eye" style="font-size: 17px;"></i></a></div>`),
                atualizar: gridjs.html(`<div style="width: 100%;display: flex;align-items: center;text-align: center;justify-content: center;"><a href="/editar-titulo/${resp[x].doc}" style='text-align: center; justify-content: right;' class="btn btn-success btn-sm"><i class="fa-solid fa-pen-to-square" style="font-size: 17px;"></i></a></div>`),
                excluir: gridjs.html(`<div style="width: 100%;display: flex;align-items: center;text-align: center;justify-content: center;"><a href="/lista-titulos/${resp[x].doc}" style='text-align: center; justify-content: right;' class="btn btn-danger btn-sm"><i class="fa-solid fa-trash" style="font-size: 17px;"></i></a></div>`)
           }
           dataTi.push(dataresp)
        }
    }
});

var columnsTi = [
    {
        id: 'ref',
        name: 'Ref.',
        width: "120px",
        sort: false,
    },
    {
        id: 'documento',
        name: "Documento",
        width: "150px"
    },
    {
        id: 'par',
        name: "Par.",
        width: "74.5px",
        sort: false,
    },
    {
        id: 'cpfCnpjVend',
        name: "cpfCnpjVend",
        hidden: true
    },
    {
        id: 'cpfCnpjCli',
        name: "cpfCnpjCli",
        hidden: true
    },
    {
        id: 'cliente',
        name: "Cliente",
        width: "130px",
        sort: false,
    },
    {
        id: 'emissao',
        name: "Emissão",
        sort: false,
    },
    {
        id: 'valor',
        name: gridjs.html("<span style='display:flex; text-align: right; justify-content: right;align-items: center; margin-right: 7px;'>Valor</span>"),
        width: "180px",
        sort: false,
    },
    {
        id: 'vizualizar',
        name: gridjs.html("<span style='display:flex; text-align: center; justify-content: center;align-items: center;'>Vizualizar</span>"),
        width: "120px",
        sort: false,
    },
    {
        id: 'atualizar',
        name: gridjs.html("<span style='display:flex; text-align: center; justify-content: center;align-items: center;'>Editar</span>"),
        sort: false,
    },
    {
        id: 'excluir',
        name: gridjs.html("<span style='display:flex; text-align: center; justify-content: center;align-items: center;'>Excluir</span>"),
        sort: false,
    }
]



