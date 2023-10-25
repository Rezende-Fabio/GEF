var dataUser = []

$.ajax({
    url: '/usuario/usuarios',
    type: 'GET',
    async: false,
    success: function(resp){
        for(x in resp){
           dataresp = {
            codigo: resp[x].cod,
            usuario: resp[x].user,
            nome: resp[x].nome,
            admin: resp[x].admin,
            editar: gridjs.html(`<div style="width: 100%;display: flex;align-items: center;text-align: center;justify-content: center;"><a href="/usuario/editar-usuario/${resp[x].cod}" style='text-align: center; justify-content: right;' class="btn btn-success btn-sm"><i class="fa-solid fa-pen-to-square" style="font-size: 17px;"></i></a></div>`),  
            excluir: gridjs.html(`<div style="width: 100%;display: flex;align-items: center;text-align: center;justify-content: center;"><button style='text-align: center; justify-content: right;' class="abrirModal btn btn-danger btn-sm" data-id="${resp[x].cod}"><i class="fa-solid fa-trash" style="font-size: 17px;"></i></button></div>`) 
           }
           dataUser.push(dataresp)
        }
    }
});

var columnsUser = [
    {
        id: 'codigo',
        name: 'Código'
    },
    {
        id: 'usuario',
        name: 'Usuário'
    },
    {
        id: 'nome',
        name: "Nome"
    },
    {
        id: 'admin',
        name: "Admin?"
    },
    {
        id: 'editar',
        name: gridjs.html("<span style='display:flex; text-align: center; justify-content: center;align-items: center;'>Editar</span>")
    },
    {
        id: 'excluir',
        name: gridjs.html("<span style='display:flex; text-align: center; justify-content: center;align-items: center;'>Excluir</span>")
    }
]



new gridjs.Grid({
    columns: columnsUser,
    data: () => {
        return new Promise(resolve => {
            setTimeout(() => resolve(dataUser), 2000);
        });
    },
    search: true,
    sort: true,
    paginationAutoPageSize: true,
    pagination: true,
}).render(document.getElementById("lista-usuarios"));