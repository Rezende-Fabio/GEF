function validarSenha(campo1, campo2){
    /*
    # Função que valida se as senha que foram informadas estão iguais.
    
    # PARAMETROS:
    #   campo1 = Senha digitada no input de senha;
    #   campo2 = Senha digitada no input de confirme a senha.
    
    # RETORNOS:
    #   return true = Retorna true caso esteja tudo certo;
    #   return false = Retorna flase com mesnagem do erro.
    */

    var senha1 = document.getElementById(campo1).value;
    var senha2 = document.getElementById(campo2).value;
    var div = document.getElementById("alert")

    if (senha1 != "" && senha2 != "" && senha1 === senha2){
        return true;
    }else{
        div.style.display = "block";
        document.getElementById(campo1).focus(); //Exibe mensagem de erro
        setTimeout(() =>{
            div.style.display = "none";
        }, "3000");
        return false;
    }
}

function fechaAlert(){
    /*
    # Função que fecha o alert da função validarSenha(campo1, campo2).
    
    # PARAMETROS:
    #   Não tem parametro.
    
    # RETORNOS:
    #   Não tem retorno.
    */
    var div = document.getElementById("alert")
    div.style.display = "none"
}

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
            '<div class="col-4">' + 
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
                    `<div class="col-4">` +
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
                    `<div class="col-4">` +
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

function validaFilial(){
    var filial = document.getElementById("filialSelc").value;
    var filiaOri = document.getElementById("filial").value;
    var alert = document.getElementById("alert");
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
        alert.innerHTML += '<button type="button" id="close" class="btn-close" onclick="fechaAlert()" aria-label="Close"></button>';
        var message = '<i class="fa-solid fa-circle-exclamation" style="font-size: 1rem; padding-right: 0.5rem;"></i><h6>O Documento de referência já está cadastrado</h6>';
        alert.innerHTML += message;
        alert.style.display = "block";
        window.scrollTo(0, 0);
        return false;

    }else if (filial != filiaOri){
        alert.innerHTML = "";
        alert.innerHTML += '<button type="button" id="close" class="btn-close" onclick="fechaAlert()" aria-label="Close"></button>';
        var message = '<i class="fa-solid fa-circle-exclamation" style="font-size: 1rem; padding-right: 0.5rem;"></i><h6>A Filial que foi selecionada é diferente da filial logada!</h6>';
        alert.innerHTML += message;
        alert.style.display = "block";
        window.scrollTo(0, 0);
        return false;

    }else if (!respCli){
        alert.innerHTML = "";
        alert.innerHTML += '<button type="button" id="close" class="btn-close" onclick="fechaAlert()" aria-label="Close"></button>';
        var message = '<i class="fa-solid fa-circle-exclamation" style="font-size: 1rem; padding-right: 0.5rem;"></i><h6>Verifique o campo do Cliente</h6>';
        alert.innerHTML += message;
        alert.style.display = "block";
        window.scrollTo(0, 0);
        return false;

    }else if (!respVend){
        alert.innerHTML = "";
        alert.innerHTML += '<button type="button" id="close" class="btn-close" onclick="fechaAlert()" aria-label="Close"></button>';
        var message = '<i class="fa-solid fa-circle-exclamation" style="font-size: 1rem; padding-right: 0.5rem;"></i><h6>Verifique o campo do Vendedor</h6>';
        alert.innerHTML += message;
        alert.style.display = "block";
        window.scrollTo(0, 0);
        return false;

    }else{
        return true;
    }
}

function validaValorBaixa(){
    var valorBaixa = document.getElementById("valorBaixa").value;
    var valorParcela = document.getElementById("valorParcela").value;
    var valorSaldo = document.getElementById("valorSaldo").value;
    var alert = document.getElementById("alert");
    var input = document.getElementById("valorBaixa");

    if (parseFloat(valorBaixa) > parseFloat(valorParcela)){
        alert.innerHTML = "";
        alert.innerHTML += '<button type="button" id="close" class="btn-close" onclick="fechaAlert()" aria-label="Close"></button>';
        var message = "<h6>Valor da baixa maior do que o da parcela!</h6>";
        alert.innerHTML += message;
        alert.style.display = "block";
        window.scrollTo(0, 0);
        return false

    }else if (parseFloat(valorBaixa) > parseFloat(valorSaldo)){
        alert.innerHTML = "";
        alert.innerHTML += '<button type="button" id="close" class="btn-close" onclick="fechaAlert()" aria-label="Close"></button>';
        var message = "<h6>Valor da baixa maior do que o saldo!</h6>";
        alert.innerHTML += message;
        alert.style.display = "block";
        window.scrollTo(0, 0);
        return false

    }else{
        return true
    }
}

function ValidaVendDev(){
    var alert = document.getElementById("alert");
    var cliente = document.getElementById("cliente").value.split(' ');
    var docRef = document.getElementById("docRef").value;
    var respCli;
    var respDocRef;

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
        url: '/api-docRef',
        type: 'POST',
        async: false,
        dataType: 'json',
        contentType: 'application/json',
        data:JSON.stringify({
            id: cliente[0],
            docRef: docRef,
        }),
        success: function(data){
            respDocRef = data.resp;
        }
    });

    if (!respCli){
        alert.innerHTML = "";
        alert.innerHTML += '<button type="button" id="close" class="btn-close" onclick="fechaAlert()" aria-label="Close"></button>';
        var message = "<h6>Verifique o campo do Cliente</h6>";
        alert.innerHTML += message;
        alert.style.display = "block";
        window.scrollTo(0, 0);
        return false;

    }else if(!respDocRef){
        alert.innerHTML = "";
        alert.innerHTML += '<button type="button" id="close" class="btn-close" onclick="fechaAlert()" aria-label="Close"></button>';
        var message = "<h6>O documento de referência não está vinculado com este cliente</h6>";
        alert.innerHTML += message;
        alert.style.display = "block";
        window.scrollTo(0, 0);
        return false;
    }else{
        return true;
    }


}
