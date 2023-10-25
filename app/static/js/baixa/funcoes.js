function mostraAlert(msg) {
    var div = document.querySelector("#alerBaixa");
    div.classList.remove("d-none");
    div.innerHTML = "";
    div.innerHTML += `<i class="fa-solid fa-circle-exclamation"></i> <h6>${msg}</h6>`
    div.innerHTML += '<div class="progress active"></div>';
    window.scroll({
        top: 0,
        behavior: "smooth",
    });
    setTimeout(() => {
        div.classList.add("d-none");
    }, 8000);
}

function calculaSaldo(){
    let inputSaldo = document.getElementById("saldoAtual");
    inputSaldo.value = (document.getElementById("valorSaldo").value - document.getElementById("valorBaixa").value).toFixed(2);
}

function adicionaBorda(){
    let inputSaldo = document.getElementById("saldoAtual");
    inputSaldo.classList.add("saldo-atual");
}

function retiraBorda(){
    let inputSaldo = document.getElementById("saldoAtual");
    inputSaldo.classList.remove("saldo-atual");
}