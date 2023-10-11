var dataCli = []

$.ajax({
    url: '/clientes',
    type: 'POST',
    dataType: 'json',
    contentType: 'application/json',
    success: function(resp){
        for(x in resp){
           dataresp = {
            cod: resp[x].cod,
            loja: resp[x].loja,
            nome: resp[x].nome,
            cpfCnpj: resp[x].cpfCnpj,
            status: resp[x].status,  
            vizualizar: gridjs.html(`<div style="width: 100%;display: flex;align-items: center;text-align: center;justify-content: center;"><a class="abrirModal  btn btn-primary" data-id="${resp[x].cod}"><i class="fa-solid fa-eye" style="font-size: 17px;"></i></a></div>`) 
           }
           dataCli.push(dataresp)
        }
    }
});

var columnsCli = [
    {
        id: 'cod',
        name: 'Código'
    },
    {
        id: 'loja',
        name: 'Loja'
    },
    {
        id: 'nome',
        name: "Nome"
    },
    {
        id: 'cpfCnpj',
        name: "CPF/CNPJ"
    },
    {
        id: 'status',
        name: "Status"
    },
    {
        id: 'vizualizar',
        name: gridjs.html("<span style='display:flex; text-align: center; justify-content: center;align-items: center;'>Vizualizar</span>")
    }
]