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
    var div = document.querySelector(".alert");

    if (senha1 != "" && senha2 != "" && senha1 === senha2){
        return true;
    }else{
        div.classList.remove("d-none");
        document.getElementById(campo1).focus(); //Exibe mensagem de erro
        setTimeout(() =>{
            div.classList.add("d-none");
        }, "3000");
        return false;
    }
}


function mostrarSenha(button){
    var inputSenha = document.getElementById("senha");
    var inputConfirm = document.getElementById("confSenha");

    if (inputSenha.type == "password"){
        inputSenha.type = "text";
        inputConfirm.type = "text";
        button.innerHTML = '<i class="fa-solid fa-eye-slash"></i>';
    }else{
        inputSenha.type = "password";
        inputConfirm.type = "password";
        button.innerHTML = '<i class="fa-solid fa-eye"></i>';
    }
}