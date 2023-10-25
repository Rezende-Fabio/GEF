
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