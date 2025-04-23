function toggleForms() {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    loginForm.classList.toggle('hidden');
    signupForm.classList.toggle('hidden');
}

function handleLogin(event) {
    event.preventDefault();  // Prevent form submission to handle it via JavaScript

    // Get the form data
    const username = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    // Hardcoded credentials (for frontend authentication only)
    const validUsername = "admin";
    const validPassword = "tiger";

    // Check if the entered credentials are correct
    if (username === validUsername && password === validPassword) {
        // If login is successful, redirect to the dashboard
        const currentUrl = window.location.href;  // Get the current URL
        const redirectUrl = currentUrl.endsWith('/') ? currentUrl + 'dashboard' : currentUrl + '/dashboard';  // Append /dashboard
        window.location.href = redirectUrl;  // Redirect to the dashboard page
    } else {
        // If login fails, show an error message
        alert("Invalid credentials. Please try again.");
    }
}


function handleSignup(event) {
    event.preventDefault();
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('signupConfirmPassword').value;

    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    alert(`Signed up with: ${email}`);
    // Here you would typically send the signup data to your server
}

document.getElementById('hamburger').addEventListener('click', function() {
    document.getElementById('sidebar').classList.toggle('active');
    document.getElementById('content').classList.toggle('active');
});

// Function to show the selected tab and update the active sidebar item
function showTab(tabId, activeLinkId) {
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => {
        if (tab.id === tabId) {
            tab.style.display = 'block'; // Show the selected tab
            tab.classList.add('active'); // Add active class
        } else {
            tab.style.display = 'none'; // Hide other tabs
            tab.classList.remove('active'); // Remove active class
        }
    });

    // Update active link
    const links = document.querySelectorAll('.sidebar ul li');
    links.forEach(link => {
        link.classList.remove('active'); // Remove active class from all links
    });
    document.getElementById(activeLinkId).classList.add('active'); // Add active class to the clicked link
}

// Event listeners for sidebar links
document.getElementById('dashboard-link').addEventListener('click', function() {
    showTab('dashboard', 'dashboard-link');
});

document.getElementById('upload-pdf-link').addEventListener('click', function() {
    showTab('upload-pdf', 'upload-pdf-link');
});








document.getElementById('pdf-upload-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const pdfName = document.getElementById('pdf-name').value;
    const pdfAlias = document.getElementById('pdf-alias').value;
    const pdfFile = document.getElementById('pdf-file').files[0];
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;  // Get the CSRF token

    console.log('Form submitted with: ', {
        pdfName: pdfName,
        pdfAlias: pdfAlias,
        pdfFile: pdfFile ? pdfFile.name : 'No file selected',
        csrfToken: csrfToken
    });

    if (pdfFile) {
        const formData = new FormData();
        formData.append('name', pdfName);
        formData.append('alias', pdfAlias);
        formData.append('file', pdfFile);
        formData.append('csrfmiddlewaretoken', csrfToken);  // Add CSRF token

        console.log('FormData prepared:', formData);

        fetch('upload/', {  // Corrected URL path
            method: 'POST',
            body: formData
        })
        .then(response => {
            console.log('Response from server:', response);  // Log the full response object for debugging
            if (!response.ok) {
                console.error('Failed request: ', response);
                throw new Error('Server returned an error');
            }
            return response.json();
        })
        .then(data => {
            console.log('Success response from server:', data);
            document.getElementById('upload-status').innerText = 'PDF uploaded successfully!';
            // Reset the form fields after successful upload
            resetForm('pdf-upload-form');
        })
        .catch((error) => {
            console.error('Error caught in fetch:', error);
            document.getElementById('upload-status').innerText = 'PDF upload failed!';
        });
    } else {
        console.error('No file selected!');
    }
});

// Function to reset form fields
function resetForm(formId) {
    const form = document.getElementById(formId);
    form.reset();  // This will reset all fields in the form
}




// Initial display
showTab('dashboard', 'dashboard-link'); // Show the dashboard by default



document.getElementById('signoutbtn').addEventListener('click', function() {
    // Get the base URL (i.e., without '/dashboard')
    const currentUrl = window.location.origin;  // This gets the base URL (e.g., http://127.0.0.1)

    // Redirect to '/theadmin' (or '/theadmin/login' if needed)
    const redirectUrl = currentUrl + '/theadmin';  // This is the URL you want to go to after sign-out

    // Perform the redirect
    window.location.href = redirectUrl;
});
