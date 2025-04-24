var socketio = io();

const chatMessages = document.getElementById("chat-messages");

const createMessage = (name, msg, type) => {
    const timestamp = new Date().toLocaleTimeString();
    const messageHTML = `
        <div class="chat-message ${type}">
            <div class="text">
                <strong>${name}</strong>: ${msg}
                <div class="timestamp">${timestamp}</div>
            </div>
        </div>
    `;
    chatMessages.innerHTML += messageHTML;
    chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll to the bottom
};

socketio.on("message", (data) => {
    createMessage(data.name, data.message, data.type);
});

document.addEventListener('DOMContentLoaded', () => {
    const darkModeToggle = document.querySelector('.dark-mode-toggle');
    const navbar = document.querySelector('.navbar');
    const chatContainer = document.querySelector('.chat-container');

    // Function to toggle dark mode
    const toggleDarkMode = () => {
        document.body.classList.toggle('dark-mode');
        navbar.classList.toggle('dark-mode');
        chatContainer.classList.toggle('dark-mode');
        localStorage.setItem('darkMode', document.body.classList.contains('dark-mode') ? 'enabled' : 'disabled');
    };

    // Initialize dark mode based on user preference
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
        navbar.classList.add('dark-mode');
        chatContainer.classList.add('dark-mode');
    }

    darkModeToggle.addEventListener('click', toggleDarkMode);
});

const sendMessage = () => {
    const messageInput = document.getElementById("message");
    const messageText = messageInput.value.trim();
    if (messageText === "") return;
    socketio.emit("message", { data: messageText, type: 'sent' });
    messageInput.value = "";
};

// Render initial messages from the server
messages.forEach((msg) => {
    createMessage(msg.name, msg.message, msg.type);
});