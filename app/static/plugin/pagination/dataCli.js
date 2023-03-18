var dataCli = []

$.ajax({
    url: '/clientes',
    type: 'POST',
    async: false,
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
            vizualizar: `<div style="width: 100%;display: flex;align-items: center;text-align: center;justify-content: center;"><a href="/lista-clientes/${resp[x].cod}" class="btn btn-outline-primary btn-sm"><i class="fa-solid fa-eye"></i></a></div>` 
           }
           dataCli.push(dataresp)
        }
    }
});

var columnsCli = {
    cod: 'Código',
    loja: 'Loja',
    nome: 'Nome',
    cpfCnpj: 'CPF/CNPJ',
    status: 'Status',
    vizualizar: "<span style='display:flex; text-align: center; justify-content: center;align-items: center;'>Vizualizar</span>"
}