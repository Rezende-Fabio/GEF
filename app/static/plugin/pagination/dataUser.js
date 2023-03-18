var dataUser = []

$.ajax({
    url: '/usuarios',
    type: 'POST',
    async: false,
    dataType: 'json',
    contentType: 'application/json',
    success: function(resp){
        for(x in resp){
           dataresp = {
            cod: resp[x].cod,
            ususario: resp[x].user,
            nome: resp[x].nome,
            admin: resp[x].admin,
            atualizar: `<div style="width: 100%;display: flex;align-items: center;text-align: center;justify-content: center;"><a href="/editar-usuario/${resp[x].cod}" style='text-align: center; justify-content: right;' class="btn btn-outline-success btn-sm"><i class="fa-solid fa-pen-to-square" style="font-size: 17px;"></i></a></div>`,  
            excluir: `<div style="width: 100%;display: flex;align-items: center;text-align: center;justify-content: center;"><a href="/lista-usuarios/${resp[x].cod}" style='text-align: center; justify-content: right;' class="btn btn-outline-danger btn-sm"><i class="fa-solid fa-trash" style="font-size: 17px;"></i></a></div>` 
           }
           dataUser.push(dataresp)
        }
    }
});

var columnsUser = {
    cod: 'Código',
    ususario: 'Usuário',
    nome: 'Nome',
    admin: 'Admin?',
    atualizar: "<span style='display:flex; text-align: center; justify-content: center;align-items: center;'>Editar</span>",
    excluir: "<span style='display:flex; text-align: center; justify-content: center;align-items: center;'>Excluir</span>"
}