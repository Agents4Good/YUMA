let idChatLocal = null;
let arquivosSelecionados = [];
let synth = window.speechSynthesis;
let isSpeaking = false;

document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById('user__input');
    const form = document.getElementById('chat_form');
    const chatContainer = document.getElementById('chat_container');

    // Atualiza placeholder
    function atualizarPlaceholder() {
        input.placeholder = "Pergunte alguma coisa";
    }

    atualizarPlaceholder();
    window.addEventListener('resize', atualizarPlaceholder);

    // Submete ao apertar Enter
    form.addEventListener('keypress', function (event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            form.dispatchEvent(new Event('submit'));
        }
    });

    // Submissão do formulário
    form.addEventListener('submit', function (event) {
        event.preventDefault();
        const message = input.value.trim();
        if (message === "") return;

        input.value = "";
        addUserMessage(message);
        sendMessage(message);
    });

    function addUserMessage(message) {
        const userBubble = `
            <div class="bubble user">
                ${message}
            </div>`;
        chatContainer.insertAdjacentHTML("beforeend", userBubble);
        scrollToBottom();
    }

    function addBotMessage(markdownResponse = "Pensando...") {
        const botBubble = `
            <div class="bubble bot">
                ${markdownResponse}
            </div>`;
        chatContainer.insertAdjacentHTML("beforeend", botBubble);
        scrollToBottom();
    }

    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function speak(text) {
        if (isSpeaking) {
            synth.cancel();
            isSpeaking = false;
        } else {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'pt-BR';
            synth.speak(utterance);
            isSpeaking = true;
        }
    }

    function sendMessage(message) {
        addBotMessage(); // placeholder "pensando..."
        disableInput();

        const formData = new FormData();
        formData.append('input_data', message);
        arquivosSelecionados.forEach(file => formData.append('archives[]', file));

        fetch('/chat', {
            method: 'POST',
            body: formData
        })
        .then(async response => {
            if (!response.ok) throw new Error("Erro na requisição");
            const data = await response.json();

            const markdownResponse = data.response;
            const htmlResponse = marked.parse(markdownResponse);

            const lastBot = chatContainer.querySelector('.bubble.bot:last-child');
            lastBot.innerHTML = htmlResponse;

            speak(markdownResponse);

            scrollToBottom();
            enableInput();
        })
        .catch(error => {
            const lastBot = chatContainer.querySelector('.bubble.bot:last-child');
            lastBot.textContent = "Desculpe, algo deu errado.";
            console.error(error);
            enableInput();
        });

        arquivosSelecionados = [];
    }

    function disableInput() {
        input.disabled = true;
    }

    function enableInput() {
        input.disabled = false;
        input.focus();
    }
});
