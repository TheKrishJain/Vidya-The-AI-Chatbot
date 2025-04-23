const chatbotOverlay = document.getElementById('chatbot-overlay');
const chatLog = document.getElementById('chat-log');
const chatInput = document.getElementById('chat-input');
const sendButton = document.getElementById('send-button');
const clearChatBtn = document.getElementById('clear-chat-btn');
const suggestionsList = document.getElementById('suggested-questions');


// JavaScript to toggle the visibility of the menu options
function toggleMenu() {
    const menuOptions = document.getElementById('menu-options'); // Get the menu options
    alert("hi"); // Check if the alert is showing

    // Toggle the menu visibility
    if (menuOptions.style.display === 'none' || menuOptions.style.display === '') {
        menuOptions.style.display = 'flex'; // Correct way to show the menu
    } else {
        menuOptions.style.display = 'none'; // Correct way to hide the menu
    }
}



// Show the chatbot automatically on load
document.addEventListener('DOMContentLoaded', () => {

    chatbotOverlay.style.display = 'flex'; // Show the chatbot on load
    addMessage('Chatbot', 'Hello, Welcome To VSIT, my name is Vidya and I am here to assist you always.', 'bot-message');
});

// Function to toggle visibility of the chatbot
function toggleChatbot() {
    chatbotOverlay.style.display = chatbotOverlay.style.display === 'none' ? 'flex' : 'none';  // Toggle visibility
}
let isExpanded = false; // Track the expansion state



// Function to expand or collapse the chatbot window
function toggleExpand() {
    if (isExpanded) {
        chatbotOverlay.classList.remove('expanded'); // Remove the expanded class
        document.getElementById('expand-chat-btn').innerHTML = '🔍<br> Expand'; // Change button text
    } else {
        chatbotOverlay.classList.add('expanded'); // Add the expanded class
        document.getElementById('expand-chat-btn').innerHTML = '🔼<br> Collapse'; // Change button text
    }
    isExpanded = !isExpanded; // Toggle the state
}

// Function to speak the message using speech synthesis
function speakMessage(message) {
    const utterance = new SpeechSynthesisUtterance(message);
    speechSynthesis.onvoiceschanged = () => {
        const voices = speechSynthesis.getVoices();
        utterance.voice = voices.find(voice => voice.name === 'Google UK English Female') || voices[0];
        window.speechSynthesis.speak(utterance);
    };
}

// Handle sending messages
async function sendMessage() {
    const message = chatInput.value;
    addMessage('You', message, 'user-message'); // Display user message
    chatInput.value = ''; // Clear input field

    // Send message to Django backend
    const response = await fetch('/api/chat/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
    });

    const data = await response.json();
    addMessage('Chatbot', data.reply, 'bot-message'); // Display bot response
}

// Handle Enter key press to send the message
chatInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

// Function to add messages to the chat log
function addMessage(sender, message, className) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ' + className;

    // Create a smile icon and append it first for bot messages
    if (className === 'bot-message') {
        const icon = document.createElement('img');
        icon.src = '/static/smile.png'; // Ensure this path is correct
        icon.alt = 'Smile Icon';
        icon.className = 'smile-icon'; // Optional: for styling if needed
        messageDiv.appendChild(icon); // Append the smile icon to the message div
    }

    // Create a text container for the message
    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    textDiv.appendChild(document.createTextNode(`${message}`));

    // Append the text to the message div
    messageDiv.appendChild(textDiv);

    // Append the speaker icon only for bot messages
    if (className === 'bot-message') {
        const speakerIcon = document.createElement('i');
        speakerIcon.className = 'fas fa-volume-up speaker-icon'; // Use Font Awesome speaker icon
        speakerIcon.onclick = () => speakMessage(message); // Speak when clicked

        // Create a wrapper div for the message and the speaker icon
        const wrapperDiv = document.createElement('div');
        wrapperDiv.className = 'message-wrapper'; // Optional: for additional styling

        // Append the message div to the wrapper
        wrapperDiv.appendChild(messageDiv);

        // Append the speaker icon to the wrapper, outside the message box
        wrapperDiv.appendChild(speakerIcon); // Append the speaker icon at the end of the wrapper

        chatLog.appendChild(wrapperDiv); // Append the wrapper to chatLog
    } else {
        chatLog.appendChild(messageDiv); // Append user message directly
    }

    chatLog.scrollTop = chatLog.scrollHeight; // Scroll to the bottom
}

// Clear chat functionality
clearChatBtn.onclick = function() {
    chatLog.innerHTML = ''; // Clear the chat log
};

// Send button functionality
sendButton.onclick = sendMessage;

// Function to show suggested queries while typing
const suggestionBox = document.getElementById('suggestion-box');

chatInput.addEventListener('input', function() {
    const userInput = this.value; // Get the current input

    if (userInput.length > 0) { // Only fetch suggestions if there's input
        fetch('/api/suggested-questions/', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: userInput })
        })
        .then(response => response.json())
        .then(data => {
            suggestionsList.innerHTML = ''; // Clear previous suggestions

            if (data.questions && data.questions.length > 0) {
                data.questions.forEach(question => {
                    const li = document.createElement('li');
                    li.textContent = question.text; // Assuming 'text' is a field in your questions JSON
                    li.onclick = function() {
                        chatInput.value = question.text; // Set input value to clicked suggestion
                        suggestionBox.style.display = 'none'; // Hide suggestions
                    };
                    suggestionsList.appendChild(li);
                });
                suggestionBox.style.display = 'block'; // Show suggestion box
            } else {
                suggestionBox.style.display = 'none'; // Hide if no suggestions
            }
        })
        .catch(error => {
            console.error('Error fetching suggestions:', error);
            suggestionBox.style.display = 'none'; // Hide suggestions on error
        });
    } else {
        suggestionBox.style.display = 'none'; // Hide suggestions if input is empty
    }
});

// Function to select a suggestion and fill the input
function selectSuggestion(suggestion) {
    chatInput.value = suggestion; // Autofill input with selected suggestion
    suggestionsList.style.display = 'none'; // Hide suggestions after selection
}

// Utility function to get CSRF token (if needed)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
