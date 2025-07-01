// Pega os elementos
var modal = document.getElementById("keyModal");
var btn = document.querySelector(".nav-item.key");
var span = document.querySelector(".close");

btn.onclick = function(e) {
    e.preventDefault();
    modal.style.display = "block";
}

span.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

document.getElementById("keyForm").onsubmit = function(e) {
    e.preventDefault();
    var selectedModel = document.getElementById("modelSelect").value;
    var apiKey = document.getElementById("apiKey").value;

    console.log("Modelo selecionado:", selectedModel);
    console.log("Chave:", apiKey);

    alert("Chave salva com sucesso!");
    modal.style.display = "none";
}
