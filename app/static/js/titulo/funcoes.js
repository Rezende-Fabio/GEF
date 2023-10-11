function parcelamento(numParcelas){
    /*
    # Função que pega o número de parcelas e divide o valor do documento
    
    # PARAMETROS:
    #   numParcelas = Número de parcelas selecionadas.
    
    # RETORNOS:
    #   Não tem retorno.
    */

    var qtdePar = numParcelas.value;
    var valorTotal = document.getElementById("valorTotal").value;
    var div = document.getElementById("rowParcelamento");
    var parcelas = document.getElementById("parcelas").value;

    if (qtdePar != 0){
        //limpa a div
        div.innerHTML = "";

        valor = valorTotal / qtdePar;

        //Pega data atual e formata
        const data = new Date().toLocaleDateString();
        var dataFormat = data.split('/').reverse().join('-');

        div.innerHTML += '<div class="row justify-content-md-center">' + 
            '<div class="col-2">' +
                '<label style="font-weight: 700; font-size:15px;">Num. Parcelas</label>' + 
            '</div>' +
            '<div class="col-4">' +
                '<label style="font-weight: 700; font-size:15px;">Valor</label>' +
            '</div>' + 
            '<div class="col-4 mb-2">' + 
                '<label style="font-weight: 700; font-size:15px;">Data Vencimento</label>' + 
            '</div>' + 
        '</div>'

        //Insere os inputs de cordo com o número de parcelas
        for (var i = 1; i <= qtdePar; i++){
            if (qtdePar == i){
                var inputValor = `<div class="row justify-content-md-center">` +
                    `<div class="col-2">` +
                        `<h6 style="margin-top: 0.4rem;">x${i} R$</h6>` +
                    `</div>` +
                    `<div class="col-4">` +
                        `<input type="text" class="form-control" style="text-transform: uppercase;" name="valor${i}" id="valor${i}" maxlength="10" size="10" tabindex="4" value="${valor.toFixed(2)}">` +
                    `</div>` +
                    `<div class="col-4 mb-2">` +
                        `<input type="date" class="form-control" class="" style="text-transform: uppercase;" name="parcela${i}" id="parcela${i}" maxlength="10" size="10" tabindex="4" autocomplete="off" value="${dataFormat}">` +
                    `</div>` +
                `</div>`
            }else{
                var inputValor = `<div class="row justify-content-md-center">` +
                    `<div class="col-2">` +
                        `<h6 style="margin-top: 0.4rem;">x${i} R$</h6>` +
                    `</div>` +
                    `<div class="col-4">` +
                        `<input type="text" class="form-control" style="text-transform: uppercase;" name="valor${i}" id="valor${i}" maxlength="10" size="10" tabindex="4" value="${valor.toFixed(2)}" readonly>` +
                    `</div>` +
                    `<div class="col-4 mb-2">` +
                        `<input type="date" class="form-control" class="" style="text-transform: uppercase;" name="parcela${i}" id="parcela${i}" maxlength="10" size="10" tabindex="4" autocomplete="off" value="${dataFormat}">` +
                    `</div>` +
                `</div>`
            }
        
            div.innerHTML += inputValor;
        }
    }

    var soma = 0;
    var valor = 0;
    for (var i = 1; i <= parcelas; i++){
        valor = document.getElementById(`valor${i}`).value;
        ultimaParcela = document.getElementById(`valor${i}`);
        soma = parseFloat(soma) + parseFloat(valor);
    }

    soma = soma.toFixed(2);

    if(soma != parseFloat(valorTotal)){
        if (soma > valorTotal){
            var diferenca = soma - valorTotal;
            ultimaParcela.value = (parseFloat(valor) - diferenca).toFixed(2);
        }else{
            var diferenca = valorTotal - soma;
            ultimaParcela.value = (parseFloat(valor) + diferenca).toFixed(2);
        }
    }
    
}

function exibeFechaAlert(){
    var alert = document.getElementById("alert");
    window.scrollTo(0, 0);
    alert.classList.remove("d-none");

    setTimeout(function () {
        alert.classList.add("d-none");
    }, 2000);
}


function validaFilial(){
    var filial = document.getElementById("filialSelc").value;
    var filiaOri = document.getElementById("filial").value;
    var alert = document.getElementById("alert");
    var msg = document.querySelector(".msg");
    var vendedor = document.getElementById("vendedor").value.split(' ');
    var cliente = document.getElementById("cliente").value.split(' ');
    var doc = document.getElementById("docRef").value;
    var respDoc;
    var respVend;
    var respCli;


    $.ajax({
        url: '/docRecfTitulo',
        type: 'POST',
        async: false,
        dataType: 'json',
        contentType: 'application/json',
        data:JSON.stringify({
            doc: doc,
            filial: filiaOri,
        }),
        success: function(data){
            respDoc = data;
        }
    });

    $.ajax({
        url: '/api-id-cliente',
        type: 'POST',
        async: false,
        dataType: 'json',
        contentType: 'application/json',
        data:JSON.stringify({
            id: cliente[0],
        }),
        success: function(data){
            respCli = data.resp;
        }
    });

    $.ajax({
        url: '/api-id-vendedor',
        type: 'POST',
        async: false,
        dataType: 'json',
        contentType: 'application/json',
        data:JSON.stringify({
            id: vendedor[0],
        }),
        success: function(data){
            respVend = data.resp;
        }
    });


    if (!respDoc){
        alert.innerHTML = "";
        var message = 'O Documento de referência já está cadastrado';
        msg.innerHTML += message;
        exibeFechaAlert(alert);
        return false;

    }else if (filial != filiaOri){
        alert.innerHTML = "";
        var message = 'A Filial que foi selecionada é diferente da filial logada!';
        msg.innerHTML += message;
        exibeFechaAlert(alert);
        return false;

    }else if (!respCli){
        alert.innerHTML = "";
        var message = 'Verifique o campo do Cliente';
        msg.innerHTML += message;
        exibeFechaAlert(alert);
        return false;

    }else if (!respVend){
        alert.innerHTML = "";
        var message = 'Verifique o campo do Vendedor';
        msg.innerHTML += message;
        exibeFechaAlert(alert);
        return false;

    }else{
        return true;
    }
}

