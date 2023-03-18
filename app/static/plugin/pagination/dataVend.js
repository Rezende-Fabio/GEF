var dataVend = []

$.ajax({
    url: '/vendedores',
    type: 'POST',
    async: false,
    dataType: 'json',
    contentType: 'application/json',
    success: function(resp){
        for(x in resp){
           dataresp = {
            cod: resp[x].cod,
            nome: resp[x].nome,
            cpfCnpj: resp[x].cpfCnpj,
            tel: resp[x].tel,
            status: resp[x].status,  
            vizualizar: `<div style="width: 100%;display: flex;align-items: center;text-align: center;justify-content: center;"><a href="/lista-vendedores/${resp[x].cod}" class="btn btn-outline-primary btn-sm"><i class="fa-solid fa-eye" style="font-size: 17px;"></i></a></div>` 
           }
           dataVend.push(dataresp)
        }
    }
});

var columnsVend = {
    cod: 'Código',
    nome: 'Nome',
    cpfCnpj: 'CPF/CNPJ',
    tel: "Telefone",
    status: 'Status',
    vizualizar: "<span style='display:flex; text-align: center; justify-content: center;align-items: center;'>Vizualizar</span>"
}
