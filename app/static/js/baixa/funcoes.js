function calculaSaldo(){
    let inputSaldo = document.getElementById("saldoAtual");
    inputSaldo.value = (document.getElementById("valorSaldo").value - document.getElementById("valorBaixa").value).toFixed(2);
}

function adicionaBorda(){
    console.log("colocou");
    let inputSaldo = document.getElementById("saldoAtual");
    inputSaldo.classList.add("saldo-atual");
}

function retiraBorda(){
    console.log("tirou");
    let inputSaldo = document.getElementById("saldoAtual");
    inputSaldo.classList.remove("saldo-atual");
}