var modal = document.getElementById("keyModal");
var btn = document.querySelector(".nav-item.key");
var span = document.querySelector(".close");


document.addEventListener('DOMContentLoaded', () => {
    if (!KEY_EXISTS) {
        document.getElementById('keyModal').style.display = 'block';
    }
});

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

document.getElementById("keyForm").addEventListener('submit', async function(e) {
    e.preventDefault();

    var apiKey = document.getElementById("apiKey");
    var conversationModel = document.getElementById("conversationModelSelect").value;
    var toolcallingModel = document.getElementById("toolcallingModelSelect").value;
    var keyError = document.getElementById("apiKeyError");
    var loader = document.getElementById("saveLoader");

    loader.style.display = "inline-block"

    try {
        const response = await fetch('/save_key', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                apiKey: apiKey.value,
                conversationModel: conversationModel,
                toolcallingModel: toolcallingModel
            })
        });

        if (!response.ok) {
            const data = await response.json();
            apiKey.style.marginBottom = "2px";
            keyError.textContent = data.error || "Erro ao salvar a chave";
            keyError.style.display = "block";

        } else {
            modal.style.display = "none";
            apiKey.style.marginBottom = "10px";
            keyError.textContent = "";
            keyError.style.display = "none";
        }

    } catch (error) {
        console.error('Erro:', error);
        keyError.style.display = "block";
        keyError.textContent = 'Erro Interno!';
    } finally {
        loader.style.display = "none";
    }
});
