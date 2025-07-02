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

    var apiKey = document.getElementById("apiKey").value;
    var conversationModel = document.getElementById("conversationModelSelect").value;
    var toolcallingModel = document.getElementById("toolcallingModelSelect").value;

    try {
        const response = await fetch('/save_key', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                apiKey: apiKey,
                conversationModel: conversationModel,
                toolcallingModel: toolcallingModel
            })
        });

        if (!response.ok) {
            alert('Erro ao salvar chave!');
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro na requisição!');
    }
});
