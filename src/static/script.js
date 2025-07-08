var modal = document.getElementById("keyModal");
var btn = document.getElementById("open-key-popup");
var span = document.querySelector(".close");

var toggleKeyVisibilityBtn = document.getElementById("toggle-key-visibility");
var apiKeyInput = document.getElementById("apiKey");

btn.onclick = function(e) {
    e.preventDefault();
    modal.style.display = "flex";
}

span.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

if (toggleKeyVisibilityBtn) {
    toggleKeyVisibilityBtn.addEventListener('click', function() {
        if (apiKeyInput.type === 'password') {
            apiKeyInput.type = 'text';
            toggleKeyVisibilityBtn.textContent = 'visibility';
        } else {
            apiKeyInput.type = 'password';
            toggleKeyVisibilityBtn.textContent = 'visibility_off';
        }
    });
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
            keyError.textContent = data.error || "Erro ao salvar a chave";
            keyError.style.display = "block";

        } else {
            modal.style.display = "none";
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
