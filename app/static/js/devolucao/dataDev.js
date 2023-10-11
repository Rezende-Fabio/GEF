var dataDev = []

$.ajax({
    url: '/devolucoes',
    type: 'POST',
    async: false,
    dataType: 'json',
    contentType: 'application/json',
    success: function(resp){
        for(x in resp){
           dataresp = {
                cpfCnpj: resp[x].cpfCnpj,
                cliente: resp[x].cli,
                ref: resp[x].ref,
                cad: resp[x].cad,
                valor: gridjs.html(`<span style='display:flex; text-align: right; justify-content: right;align-items: center; margin-right: 15px;'>` + resp[x].valor + `</span>`),
                excluir: gridjs.html(`<div style="width: 100%;display: flex;align-items: center;text-align: center;justify-content: center;"><a href="/exluir-devolucao-modal/${resp[x].idDev}" style='text-align: center; justify-content: right;' class="btn btn-outline-danger btn-sm"><i class="fa-solid fa-trash" style="font-size: 17px;"></i></a></div>`)
           }
           dataDev.push(dataresp)
        }
    }
});

var columnsDev = [
    {
        id: 'cpfCnpj',
        name: "cpfCnpj",
        hidden: true,
    },
    {
        id: 'cliente',
        name: "Cliente",
        width: "130px",
        sort: false,
    },
    {
        id: 'ref',
        name: "Ref.",
        sort: false,
    },
    {
        id: 'cad',
        name: "Data Cadastro",
        sort: false,
    },
    {
        id: 'valor',
        name: gridjs.html(`<span style='display:flex; text-align: right; justify-content: right;align-items: center; margin-right: 15px;'>Valor</span>`),
        width: "180px",
        sort: false,
    },
    {
        id: 'excluir',
        name: gridjs.html("<span style='display:flex; text-align: center; justify-content: center;align-items: center;'>Excluir</span>"),
        sort: false,
    }
]
