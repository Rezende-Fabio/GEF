function mostraAlert() {
    var div = document.querySelector(".alert");
    div.classList.remove("d-none");
    div.innerHTML = "";
    div.innerHTML += '<i class="fa-solid fa-circle-exclamation"></i> <h6>As senhas não são iguais!</h6>'
    div.innerHTML += '<div class="progress active"></div>';
    setTimeout(() => {
        div.classList.add("d-none");
    }, 8000);
}


function validarSenha(campo1, campo2) {
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

    if (senha1 != "" && senha2 != "" && senha1 === senha2) {
        return true;
    } else {
        mostraAlert();
        return false;
    }
}


function mostrarSenha(button) {
    var inputSenha = document.getElementById("senha");
    var inputConfirm = document.getElementById("confSenha");

    if (inputSenha.type == "password") {
        inputSenha.type = "text";
        inputConfirm.type = "text";
        button.innerHTML = '<i class="fa-solid fa-eye-slash"></i>';
    } else {
        inputSenha.type = "password";
        inputConfirm.type = "password";
        button.innerHTML = '<i class="fa-solid fa-eye"></i>';
    }
}