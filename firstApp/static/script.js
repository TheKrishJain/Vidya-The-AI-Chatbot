window.addEventListener('DOMContentLoaded', () => {
    const header = document.querySelector('.chatbot-header');
    const robotLogo = document.querySelector('.chatbot-header img'); // Robot logo
    const myDiv = document.querySelector('.mydiv'); // Scrollable chat content
  
    // Add scroll event listener to .mydiv
    myDiv.addEventListener('scroll', () => {
        const scrollPosition = myDiv.scrollTop; // Track scroll position
  
        if (scrollPosition > 20) {
            // Change header background color to dark red
            header.style.backgroundColor = '#d9534f';
  
            // Move robot logo to the top-left corner of the header
            robotLogo.style.transform = 'translate(15px, 10px)';
            robotLogo.style.top = '10px';
            robotLogo.style.left = '15px';
        } else {
            // Reset header background color to transparent
            header.style.backgroundColor = 'transparent';
  
            // Center robot logo within the header
            robotLogo.style.transform = 'translate(-50%, -50%)';
            robotLogo.style.top = '50%';
            robotLogo.style.left = '50%';
        }
    });
  });

  document.getElementById('robot-icon').addEventListener('click', function() {
    // Add the animation class on click
    this.style.animation = 'rotate360 1s ease-in-out';
    
    // Reset the animation after it finishes so you can click again to trigger it
    this.addEventListener('animationend', () => {
        this.style.animation = '';
    });
});







  
  document.addEventListener('DOMContentLoaded', () => {
      const chatbotWrapper = document.querySelector('.chatbot-wrapper');
      const chatbotHeader = document.querySelector('.chatbot-header');
      const robotLogo = document.querySelector('.chatbot-header .fas.fa-robot');
      const startChatButton = document.getElementById('start-chat-btn');
      const footerChatButton = document.getElementById('footer-chat-btn');
      const chatForm = document.querySelector('.chat-form-container');
      const backButton = document.querySelector('.back-btn');
      const footerHomeButton = document.getElementById('footer-home-btn');
      const minimizeButton = document.querySelector('.minimize-btn');
      const minimizeButtonForm = document.querySelector('.minimize-btn-form');
      const homeBtn = document.querySelector('.home-btn');
      const chatBtn = document.querySelector('.chat-btn');
      const myDiv = document.querySelector('.mydiv');
      // Show chat form and hide welcome section when 'Start Chat' button is clicked
      startChatButton.addEventListener('click', () => {
          myDiv.style.display = 'none'; // Hide the welcome section
          chatForm.style.display = 'flex'; // Show the chat form
          chatbotHeader.style.display = 'none'; // Hide the header
      });
  footerChatButton.addEventListener('click', () => {
          myDiv.style.display = 'none'; // Hide the welcome section
          chatForm.style.display = 'flex'; // Show the chat form
          chatbotHeader.style.display = 'none'; // Hide the header
      });
  
      // Show welcome section and hide chat form when back button is clicked
      backButton.addEventListener('click', () => {
          chatForm.style.display = 'none'; // Hide the chat form
          myDiv.style.display = 'block'; // Show the welcome section
          chatbotHeader.style.display = 'flex'; // Show the header
         
      });
      footerHomeButton.addEventListener('click', () => {
          chatForm.style.display = 'none'; // Hide the chat form
          myDiv.style.display = 'block'; // Show the welcome section
          chatbotHeader.style.display = 'flex'; // Show the header
      });
  
     // Optional: Add minimize functionality
   
     minimizeButton.addEventListener('click', () => {
         chatbotWrapper.style.display = 'none'; // Hide the chatbot
         chatbotToggle.style.display = 'block';  // Show the open button again
     });
  
      const chatbotToggle = document.querySelector('.chatbot-open-btn');
  
      // Add click event listener to chatbot-open-btn
      chatbotToggle.addEventListener('click', () => {
          chatbotWrapper.style.display = 'block'; // Show the chatbot
          chatbotToggle.style.display = 'none';  // Hide the open button
      });
  
      // Footer button activation
      function activateButton(button) {
          document.querySelectorAll('.footer-btn').forEach(btn => {
              btn.classList.remove('active');
          });
          button.classList.add('active');
      }
  
      homeBtn.addEventListener('click', () => activateButton(homeBtn));
      chatBtn.addEventListener('click', () => activateButton(chatBtn));
  
  
  
      // Activate button functionality for footer buttons
      function activateButton(button) {
          document.querySelectorAll('.footer-btn').forEach(btn => {
              btn.classList.remove('active');
          });
          button.classList.add('active');
      }
  
      // Event listeners for footer buttons
      homeBtn.addEventListener('click', () => activateButton(homeBtn));
      chatBtn.addEventListener('click', () => activateButton(chatBtn));
  
      // Fade header on scroll
      let lastScrollTop = 0; // Variable to keep track of the last scroll position
      window.onscroll = function() {
          fadeHeader();
      };
  

    
      const soundToggle = document.getElementById('sound-toggle'); // Assuming you have this toggle element
      soundToggle=false;
  });
  // Debugging-enhanced Chatbot JavaScript Code

// Handle the start chat button click
function validatePhone(phone) {
    const phonePattern = /^[0-9]{10}$/; // Example pattern for a 10-digit phone number
    const isValid = phonePattern.test(phone);
    console.log(`Phone validation result for ${phone}: ${isValid}`);

    const phoneError = document.getElementById("phone-error");
    if (!isValid) {
        phoneError.style.display = "block"; // Show error message if invalid
    } else {
        phoneError.style.display = "none"; // Hide error message if valid
    }
    
    
    return isValid;
}

function validateName(name) {
    const namePattern = /^[A-Za-z\s]+$/; // Pattern to allow only alphabets and spaces
    const isValid = namePattern.test(name);
    console.log(`Name validation result for ${name}: ${isValid}`);



    return isValid;}
    
    document.getElementById('start-chat-button').addEventListener('click', () => {
        console.log('Start Chat button clicked');
        const firstName = document.getElementById('first-name').value.trim();
        const email = document.getElementById('email').value.trim();
        const phone = document.getElementById('phone').value.trim();
    
        console.log(`User Input - Name: ${firstName}, Email: ${email}, Phone: ${phone}`);
    
        // Validate inputs
        // Validate Name
    if (!firstName || !validateName(firstName)) {
        alert('Please enter a valid name');
        console.error('Validation failed: Invalid or missing Name');
        return;  // Stop further execution if name is invalid
    }

    // Validate Email
    if (!email || !validateEmail(email)) {
        alert('Please enter a valid email');
        console.error('Validation failed: Invalid or missing Email');
        return;  // Stop further execution if email is invalid
    }

    // Optionally validate phone if required
    if (!phone || !validatePhone(phone)) {
        
        console.error('Validation failed: Invalid or missing Phone number');
        return;
    }
    
    // If all validations pass
    console.log('All inputs are valid. Proceed with the next action.');
    
        // Send user information to the backend
        console.log('Sending user details to the backend...');
        fetch('/send-user-info/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ firstName, email, phone }),
        })
        .then(response => {
            console.log("Response status for user info:", response.status);
            return response.json();
        })
        .then(data => {
            console.log("Response data:", data);  // Check the structure of the response here
    
            // Handle the single greeting from the backend
            if (data.greeting) {
                const botTimestamp = new Date().toLocaleString();  // Get timestamp for bot message
                conversation.push({ "sender": "Vidya", "message": data.greeting, "timestamp": botTimestamp });
                appendChatMessage(`<strong>Vidya:</strong> ${data.greeting}`, 'chatbot');
                readBotMessage(data.greeting);  // Optional: Read the message aloud
            } else {
                console.error("No greeting found in the response");
            }
        })
        .catch(error => {
            console.error('Error in sending user info:', error);
        });
    
        // Hide user info form and show chat screen
        document.getElementById('userinformation').style.display = 'none';
        document.getElementById('display-screen').style.display = 'block';
    
        // Add user details as the first message
        const chatLog = document.getElementById('chat-log');
        const userDetails = `
            <div class="user-details">
                <p><strong>User Details:</strong></p>
                <p>Name: ${firstName}</p>
                <p>Email: ${email}</p>
                <p>Phone: ${phone || 'Not provided'}</p>
            </div>
        `;
        chatLog.innerHTML = userDetails + chatLog.innerHTML;
        chatLog.scrollTop = chatLog.scrollHeight;
        console.log('User details added to chat log');
    
        // Update profile text and styling
        const profileText = document.getElementById('profile-text');
        const profileHeader = document.getElementById('profile-header');
        profileText.textContent = "Continue the Conversation";
        profileText.style.fontSize = "13px";  // Smaller font size
        profileText.style.fontWeight = "normal";  // Less bold
        profileHeader.style.fontWeight = "bold";
        profileText.style.color = "#7a7a7a";  // Optional: Change the color for better emphasis
    });


    function appendChatMessage(messageContent, messageType) {
        const chatLog = document.getElementById('chat-log');
        let messageHTML = '';
    
        if (messageType === 'chatbot' && messageContent) {
            messageHTML = `
            <div class="msg">
                <img src="/static/vidya-circle3.png" alt="hundaVidya Logo" class="bot-logo">
                <div class="message ${messageType}">
                    <p>${messageContent.replace(/\n/g, "<br>")}</p>
                    <button class="copy-btn" onclick="copyToClipboard(this)">
                        <i class="fas fa-copy"></i>
                    </button>
                </div>
            </div>
            `;
        } else if (messageType === 'user' && messageContent) {
            messageHTML = `
            <div class="msg">
                <div class="message ${messageType}">
                    <p>${messageContent}</p>
                    <button class="copy-btn" onclick="copyToClipboard(this)">
                        <i class="fas fa-copy"></i>
                    </button>
                </div>
            </div>
            `;
        }
    
        chatLog.innerHTML = messageHTML + chatLog.innerHTML;
        chatLog.scrollTop = chatLog.scrollHeight;
        console.log('Message appended to chat log');
    }
    function copyToClipboard(button) {
        // Find the message text within the same message container
        let messageText = button.parentElement.querySelector('p').innerText;
    
        // Remove "You: " or "Vidya: " from the beginning, if present
        messageText = messageText.replace(/^(You: |Vidya: )/, "");
    
        navigator.clipboard.writeText(messageText).then(() => {
            console.log('Text copied to clipboard');
    
            // Change button text to "Copied!"
            button.innerHTML = "Copied!";
    
            // Reset button back to icon after 2 seconds
            setTimeout(() => {
                button.innerHTML = '<i class="fas fa-copy"></i>';
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy text: ', err);
        });
    }
    
    
    
    

// Validate email format
function validateEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const isValid = emailPattern.test(email);
    console.log(`Email validation result for ${email}: ${isValid}`);
    return isValid;
}
////////////////////////////////////////////////////////////////////////send btton/////////////////////////////////////////
let conversation = [];  
document.getElementById('send-button').addEventListener('click', function () {
    const chatInput = document.getElementById('chat-input');
    const userMessage = chatInput.value.trim();
    const selectedLanguage = document.getElementById('language-dropdown').value; // Get the selected language

    if (userMessage) {

        const timestamp = new Date().toLocaleString();  // Get the current time
        conversation.push({ "sender": "user", "message": userMessage, "timestamp": timestamp });  // Add user message with timestamp

        appendChatMessage(`<strong>You:</strong> ${userMessage}`, 'user');
        chatInput.value = '';
        console.log('Sending message to backend...');
        // Send the message to the backend
        fetch('/chatbot-response/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({
                message: userMessage,
                language: selectedLanguage  // Pass the language code
            }),
        })
        .then(response => {
            console.log("Response status:", response.status);
            return response.json();
        })
        .then(data => {
            
            console.log("Response data:", data);
            
            const botMessage = data.response;
            // Check if the response contains a link (PDF/Brochure)
            // ... (previous code) ...
            if (botMessage.includes('<a href="')) { 
                appendChatMessage(`<strong>Vidya:</strong> ${botMessage}`, 'chatbot'); 
            } else {



            const botTimestamp = new Date().toLocaleString();  // Get timestamp for bot message
            conversation.push({ "sender": "Vidya", "message": botMessage, "timestamp": botTimestamp });  // Add bot response with timestamp
            appendChatMessage(`<strong>Vidya:</strong> ${botMessage}`, 'chatbot');
            readBotMessage(botMessage);
            }
        })
        .catch(error => {
            console.error('Error in fetch:', error);
            appendChatMessage('<strong>Vidya :</strong> Sorry, there was an error processing your message.', 'chatbot');
        });
        
    }
});
function getCSRFToken() {
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return csrfToken ? csrfToken.value : '';
}




// Allow Enter key to send the message
document.getElementById('chat-input').addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
        document.getElementById('send-button').click();
        console.log('Enter key pressed');
    }
});

///////////////////////////////////////////////////////////////////////////////////////////////


// Handle send transcript functionality
document.getElementById('send-transcript').addEventListener('click', () => {
    const email = document.getElementById('email').value.trim();  // Get the user's email

    // Create the formatted transcript from the conversation array
    let formattedTranscript = '';
    conversation.forEach(msg => {
        const speaker = msg.sender === 'user' ? 'User' : 'Bot';
        formattedTranscript += `${speaker} says: ${msg.message} (at ${msg.timestamp})\n\n`;
    });

    if (email && formattedTranscript) {
        sendTranscriptToBackend(email, formattedTranscript);
    } else {
        alert('Please ensure your email and transcript are valid.');
    }
});


function sendTranscriptToBackend(email, transcript) {
    console.log("Sending transcript to backend...");

    fetch('/send-transcript/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),  // Include CSRF token if using Django
        },
        body: JSON.stringify({
            email: email,
            transcript: transcript,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Transcript sent to your email!');
        } else {
            alert('Failed to send transcript.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was an error sending the transcript.');
    });
}


let soundEnabled = false; // Sound off by default
let voicesLoaded = false; // Track if voices are loaded

// Get the sound toggle element
const soundToggle = document.getElementById('sound-toggle');

// Set the toggle to be off by default
soundToggle.checked = false; 

// Listen for changes in the toggle
soundToggle.addEventListener('change', (e) => {
    soundEnabled = e.target.checked;
    console.log(`Sound state: ${soundEnabled ? 'ON' : 'OFF'}`);
    
    // Load voices when first enabling sound
    if (soundEnabled && !voicesLoaded) {
        loadVoices();
    }
});

let voices = [];

// Function to load voices
function loadVoices() {
    voices = window.speechSynthesis.getVoices();
    if (voices.length > 0) {
        voicesLoaded = true;
        console.log('Voices loaded:', voices);

        console.log('Available voices:');
        voices.forEach((v, i) => {
            console.log(`${i + 1}. ${v.name} - ${v.lang}`);
        });
    } else {
        console.log('No voices yet - retrying...');
        setTimeout(loadVoices, 500);
    }
}

// Initialize voice synthesis when page loads
function initSpeech() {
    // Chrome needs this event listener
    window.speechSynthesis.onvoiceschanged = loadVoices;
    
    // Some browsers need direct call
    loadVoices();
}

// Call initialization when page loads
document.addEventListener('DOMContentLoaded', initSpeech);

function readBotMessage(messageContent) {
    if (!soundEnabled) return;
    
    // Ensure speech synthesis is available
    if (!window.speechSynthesis) {
        console.error('Speech synthesis not supported');
        return;
    }

    // Cancel any current speech
    window.speechSynthesis.cancel();

    // Wait for voices to be loaded (with timeout)
    if (!voicesLoaded) {
        console.log('Voices not loaded yet - waiting...');
        setTimeout(() => readBotMessage(messageContent), 500);
        return;
    }

    const speech = new SpeechSynthesisUtterance(messageContent);
    
    // Set speech properties
    speech.volume = 1; // 0-1
    speech.rate = 1; // 0.1-10
    speech.pitch = 1; // 0-2

    // Select voice - try female first, then default
    const femaleVoice = voices.find(v => 
        v.name.toLowerCase().includes('zira') || 
        v.name.toLowerCase().includes('google') && v.name.toLowerCase().includes('female') || // Chrome|| 
        v.lang.includes('en-US') || 
        v.lang.includes('en-GB')
    );
    
    speech.voice = femaleVoice || voices[0];
    console.log('Using voice:', speech.voice ? speech.voice.name : 'default');

    // Error handling
    speech.onerror = (event) => {
        console.error('Speech synthesis error:', event.error);
    };

    // Speak the message
    window.speechSynthesis.speak(speech);
    console.log('Bot message read aloud:', messageContent);

}


// Clear Chat
document.getElementById('clear-chat').addEventListener('click', function () {
    const chatLog = document.getElementById('chat-log');
    
    // Store user info
    const userDetails = chatLog.querySelector('.user-details');
    
    // Clear all messages but preserve user info
    chatLog.innerHTML = '';  // Clear the chat log
    if (userDetails) {
        chatLog.appendChild(userDetails);  // Re-add the user info to the chat log
    }

    console.log('Chat cleared, but user info preserved.');
});
document.getElementById("clear-chat").addEventListener("mouseover", function() {
    var icon = this.querySelector("i");
    icon.classList.remove("bi-trash");
    icon.classList.add("bi-trash-fill");
  });
  
  document.getElementById("clear-chat").addEventListener("mouseout", function() {
    var icon = this.querySelector("i");
    icon.classList.remove("bi-trash-fill");
    icon.classList.add("bi-trash");
  });
  

// Login
document.getElementById('login-btns').addEventListener('click', () => {
    // Get the current URL and append '/theadmin/login'
    const currentUrl = window.location.origin;  // This will get the base URL (e.g., http://127.0.0.1)
    const loginPageUrl = currentUrl + '/theadmin/';  // Append '/theadmin/login' for login page

    // Redirect to the login page
    window.location.href = loginPageUrl;
});



// Toggle the options menu
const optionsMenu = document.getElementById('options-menu');
const optionsButton = document.getElementById('options-btn');
function toggleOptionsMenu() {
    optionsMenu.style.display = optionsMenu.style.display === 'block' ? 'none' : 'block';
}
optionsButton.addEventListener('click', (event) => {
    event.stopPropagation();
    toggleOptionsMenu();
    console.log('Options menu toggled');
});
document.addEventListener('click', (event) => {
    if (!optionsMenu.contains(event.target) && !optionsButton.contains(event.target)) {
        optionsMenu.style.display = 'none';
        console.log('Options menu hidden due to outside click');
    }
});
