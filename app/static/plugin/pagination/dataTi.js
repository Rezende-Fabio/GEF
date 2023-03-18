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
            cliente: resp[x].cli,
            emissão: resp[x].lanc,  
            valor: `<span style='display:flex; text-align: right; justify-content: right;align-items: center; margin-right: 7px;'>` + resp[x].total + `</span>`, 
            vizualizar: `<div style="width: 100%;display: flex;align-items: center;text-align: center;justify-content: center;"><a href="/lista-titulos/view/${resp[x].doc}" class="btn btn-outline-primary btn-sm"><i class="fa-solid fa-eye" style="font-size: 17px;"></i></a></div>`,
            atualizar: `<div style="width: 100%;display: flex;align-items: center;text-align: center;justify-content: center;"><a href="/editar-titulo/${resp[x].doc}" style='text-align: center; justify-content: right;' class="btn btn-outline-success btn-sm"><i class="fa-solid fa-pen-to-square" style="font-size: 17px;"></i></a></div>`,
            excluir: `<div style="width: 100%;display: flex;align-items: center;text-align: center;justify-content: center;"><a href="/lista-titulos/${resp[x].doc}" style='text-align: center; justify-content: right;' class="btn btn-outline-danger btn-sm"><i class="fa-solid fa-trash" style="font-size: 17px;"></i></a></div>`
           }
           dataTi.push(dataresp)
        }
    }
});

var columnsTi = {
    ref: 'Ref.',
    documento: 'Documento',
    par: 'Par.',
    cliente: 'Cliente',
    emissão: 'Emissão',
    valor: `<span style='display:flex; text-align: right; justify-content: right;align-items: center; margin-right: 7px;'>Valor</span>`,
    vizualizar: "<span style='display:flex; text-align: center; justify-content: center;align-items: center;'>Vizualizar</span>",
    atualizar: "<span style='display:flex; text-align: center; justify-content: center;align-items: center;'>Editar</span>",
    excluir: "<span style='display:flex; text-align: center; justify-content: center;align-items: center;'>Excluir</span>"
}




