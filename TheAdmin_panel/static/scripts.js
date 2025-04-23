function toggleForms() {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    loginForm.classList.toggle('hidden');
    signupForm.classList.toggle('hidden');
}

document.getElementById("refresh").addEventListener("click", function() {
    var icon = document.getElementById("refreshicon");
    
    // Add the rotation class to the icon
    icon.style.transform = "rotate(0deg)";
    
    // Trigger a reflow to reset the animation
    icon.offsetHeight; // This is a hack to trigger the reflow

    // Apply 360-degree rotation
    icon.style.transform = "rotate(360deg)";
});


document.getElementById("refresh").addEventListener("click",fetchDataAndDisplay());
document.getElementById("dashboard-link").addEventListener("click",fetchDataAndDisplay());
let barChart, lineChart, pieChart;  // Store chart instances globally
document.getElementById('timeRange').addEventListener('change', function () {
    const selectedRange = this.value;
    fetchDataAndDisplay(selectedRange);
});

function fetchDataAndDisplay(timeRange = "current") {
    fetch(`fetch/?timeRange=${timeRange}`)
        .then(response => response.json())
        .then(data => {
            console.log(`Dashboard Data (${timeRange}):`, data);
            
            console.log('Dashboard Data:', data);

            document.getElementById('users-visited').textContent = `Users Visited: ${data.users_visited}`;
            document.getElementById('inquiries-done').textContent = `Inquiries Done: ${data.inquiries_done}`;
            document.getElementById('most-asked-questions').textContent = `Most Asked Question: ${data.most_asked_question}`;
            document.getElementById('unique-visitors').textContent = `Unique Visitors: ${data.unique_visitors}`;
            document.getElementById('avg-time-per-user').textContent = `Avg Time Per User: ${data.avg_time_per_user} seconds`;
            document.getElementById('avg-response-time').textContent = `Avg Response Time: ${data.avg_response_time} seconds`;
            // Show the most asked questions on the dashboard
            document.getElementById('most-asked-questions').textContent = `Most Asked Question: ${data.most_asked_question}`;
            

            // Destroy existing charts before creating new ones
            if (barChart) barChart.destroy();
            if (lineChart) lineChart.destroy();
            if (pieChart) pieChart.destroy();

            // Bar Chart
            const barChartCtx = document.getElementById('barChart').getContext('2d');
            barChart = new Chart(barChartCtx, {
                type: 'bar',
                data: {
                    labels: data.message_data.labels,
                    datasets: [{
                        label: 'Messages Per Day',
                        data: data.message_data.counts,
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { display: true, position: 'bottom' } },
                    scales: {
                        x: { title: { display: true, text: 'Date', font: { size: 14 } } },
                        y: { title: { display: true, text: 'Messages Count', font: { size: 14 } }, beginAtZero: true }
                    }
                }
            });

            // Line Chart
            const lineChartCtx = document.getElementById('lineChart').getContext('2d');
            lineChart = new Chart(lineChartCtx, {
                type: 'line',
                data: {
                    labels: data.line_chart_data.labels,
                    datasets: [{
                        label: 'Messages Trend',
                        data: data.line_chart_data.counts,
                        fill: false,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { display: true, position: 'bottom' } },
                    scales: {
                        x: { title: { display: true, text: 'Date', font: { size: 14 } } },
                        y: { title: { display: true, text: 'Messages Count', font: { size: 14 } }, beginAtZero: true }
                    }
                }
            });

            // Pie Chart
            const pieChartCtx = document.getElementById('pieChart').getContext('2d');
            pieChart = new Chart(pieChartCtx, {
                type: 'pie',
                data: {
                    labels: data.pie_chart_data.labels,
                    datasets: [{
                        data: data.pie_chart_data.counts,
                        backgroundColor: ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)', 'rgba(75, 192, 192, 0.2)'],
                        borderColor: ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)', 'rgba(75, 192, 192, 1)'],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { display: true, position: 'bottom' } }
                }
            });
        })
        .catch(error => console.error('Error fetching dashboard data:', error));
}

// Event Listeners
document.getElementById("refresh").addEventListener("click", fetchDataAndDisplay);
document.getElementById("dashboard-link").addEventListener("click", fetchDataAndDisplay);










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
    console.log(`Showing tab: ${tabId}`); // Debugging log

    // Hide all tabs and remove the 'active' class
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => {
        if (tab.id === tabId) {
            tab.style.display = 'block'; // Show the selected tab
            tab.classList.add('active');
        } else {
            tab.style.display = 'none'; // Hide other tabs
            tab.classList.remove('active');
        }
    });

    // Update the active state of the sidebar menu items
    const sidebarLinks = document.querySelectorAll('.sidebar ul li');
    sidebarLinks.forEach(link => {
        if (link.id === activeLinkId) {
            link.classList.add('active'); // Add 'active' class to the selected menu item
        } else {
            link.classList.remove('active'); // Remove 'active' class from other menu items
        }
    });
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
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken  // ✅ CSRF token must be in the header
            }
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
document.getElementById('users-visited-item').addEventListener('click', function () {
    fetch('get_user_details/')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#user-details-table tbody');
            tableBody.innerHTML = ''; // Clear existing rows

            // Sort data by created_at in descending order (latest first)
            data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

            // Populate the table with sorted user data
            data.forEach(user => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${user.first_name}</td>  
                    <td>${user.email}</td>
                    <td>${user.phone}</td>
                    <td>${new Date(user.created_at).toLocaleString()}</td>
                `;
                tableBody.appendChild(row);
            });

            // Show the user details table and hide other sections
            document.getElementById('user-details').style.display = 'block';
            document.getElementById('dashboard').style.display = 'none';
            document.getElementById('upload-pdf').style.display = 'none';
        })
        .catch(error => console.error('Error fetching user details:', error));
});


document.getElementById('unique-user').addEventListener('click', function () {
    fetch('unique_user_details/')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#unique-user-details-table tbody');
            tableBody.innerHTML = ''; // Clear existing rows

            // Create a Map to store unique users with the latest timestamp
            const uniqueUsersMap = new Map();

            // Process users to retain only the latest occurrence
            data.forEach(user => {
                const userEmail = user.email;
                const userCreatedAt = new Date(user.created_at);

                // If the user doesn't exist in the Map OR has a newer timestamp, update the Map
                if (!uniqueUsersMap.has(userEmail) || userCreatedAt > new Date(uniqueUsersMap.get(userEmail).created_at)) {
                    uniqueUsersMap.set(userEmail, user);
                }
            });

            // Convert the Map values to an array and sort by created_at in descending order (latest first)
            const uniqueUsers = Array.from(uniqueUsersMap.values()).sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

            // Populate the table with sorted unique user data
            uniqueUsers.forEach(user => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${user.first_name}</td>
                    <td>${user.email}</td>
                    <td>${user.phone}</td>
                    <td>${new Date(user.created_at).toLocaleString()}</td>
                `;
                tableBody.appendChild(row);
            });

            // Show the unique user details table and hide other sections
            document.getElementById('user-details-unique').style.display = 'block';
            document.getElementById('dashboard').style.display = 'none';
            document.getElementById('upload-pdf').style.display = 'none';
        })
        .catch(error => console.error('Error fetching unique user details:', error));
});



document.getElementById("back-button2").addEventListener("click", function() {
    document.getElementById("user-details-unique").style.display = "none";
    document.getElementById("dashboard").style.display = "block";
    fetchDataAndDisplay();
});
document.getElementById("back-button1").addEventListener("click", function() {
    document.getElementById("user-details").style.display = "none";
    document.getElementById("dashboard").style.display = "block";
    fetchDataAndDisplay();
});

document.getElementById('signoutbtn').addEventListener('click', function() {
    // Get the base URL (i.e., without '/dashboard')
    const currentUrl = window.location.origin;  // This gets the base URL (e.g., http://127.0.0.1)

    // Redirect to '/theadmin' (or '/theadmin/login' if needed)
    const redirectUrl = currentUrl + '/theadmin';  // This is the URL you want to go to after sign-out

    // Perform the redirect
    window.location.href = redirectUrl;
});










document.addEventListener('DOMContentLoaded', function() {
    const sidebarLinks = document.querySelectorAll('.sidebar ul li');
    const tabContents = document.querySelectorAll('.tab-content');

    // Add event listeners to sidebar links
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function() {
            const target = this.id.replace('-link', '');
            showTab(target);
        });
    });

    // Function to show the selected tab
    function showTab(tabId) {
        tabContents.forEach(tab => {
            tab.style.display = 'none';
        });
        document.getElementById(tabId).style.display = 'block';
    }

    // Handle the notification form submission
    const notificationForm = document.getElementById('notification-form');
    const notificationStatus = document.getElementById('notification-status');

    if (notificationForm) {
        notificationForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const subject = document.getElementById('notification-subject').value;
            const message = document.getElementById('notification-message').value;
            const type = document.getElementById('notification-type').value;

            // Simulate sending the notification (replace with actual API call)
            setTimeout(() => {
                notificationStatus.textContent = 'Notification sent successfully!';
                notificationStatus.style.color = 'green';
                notificationForm.reset();
            }, 1000);
        });
    }
});



document.addEventListener('DOMContentLoaded', function () {
    const notificationForm = document.getElementById('notification-form');
    const notificationType = document.getElementById('notification-type');
    const notificationSubject = document.getElementById('notification-subject');
    const notificationMessage = document.getElementById('notification-message');

    // Predefined messages for each notification type
    const predefinedMessages = {
        event: {
            subject: "Upcoming Event: Join Us!",
            message: "We are excited to invite you to our upcoming event. Mark your calendar and don't miss out on this amazing opportunity!\n\nDate: [Insert Date]\nTime: [Insert Time]\nLocation: [Insert Location]\n\nLooking forward to seeing you there!"
        },
        reminder: {
            subject: "Reminder: Don't Forget!",
            message: "This is a friendly reminder about your upcoming commitment.\n\nDetails:\n- What: [Insert Event/Task]\n- When: [Insert Date and Time]\n- Where: [Insert Location]\n\nPlease make sure to attend or complete this on time. Thank you!"
        },
        update: {
            subject: "Important Update",
            message: "We have an important update to share with you.\n\nDetails:\n- What: [Insert Update Details]\n- When: [Insert Date]\n- Impact: [Insert Impact]\n\nPlease review this information carefully and let us know if you have any questions."
        },
        other: {
            subject: "",
            message: ""
        }
    };

    // Function to populate subject and message based on selected type
    function populateFields() {
        const selectedType = notificationType.value;

        if (predefinedMessages[selectedType]) {
            notificationSubject.value = predefinedMessages[selectedType].subject;
            notificationMessage.value = predefinedMessages[selectedType].message;
        } else {
            notificationSubject.value = "";
            notificationMessage.value = "";
        }
    }

    // Add event listener to the dropdown
    notificationType.addEventListener('change', populateFields);

    // Handle form submission
    if (notificationForm) {
        notificationForm.addEventListener('submit', function (event) {
            event.preventDefault();

            // Simulate sending the notification (replace with actual API call)
            setTimeout(() => {
                const notificationStatus = document.getElementById('notification-status');
                notificationStatus.textContent = 'Notification sent successfully!';
                notificationStatus.style.color = 'green';
                notificationForm.reset();
            }, 1000);
        });
    }
});


document.addEventListener('DOMContentLoaded', function () {
    const notificationForm = document.getElementById('notification-form');

    if (notificationForm) {
        notificationForm.addEventListener('submit', function (event) {
            event.preventDefault();

            // Get form data
            const subject = document.getElementById('notification-subject').value;
            const message = document.getElementById('notification-message').value;

            // Send data to the server using AJAX
            fetch('send-notification-email/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}',  // Include CSRF token for Django
                },
                body: JSON.stringify({
                    subject: subject,
                    message: message,
                }),
            })
            .then(response => response.json())
            .then(data => {
                const notificationStatus = document.getElementById('notification-status');
                if (data.status === 'success') {
                    notificationStatus.textContent = data.message;
                    notificationStatus.style.color = 'green';
                } else {
                    notificationStatus.textContent = 'Error: ' + data.message;
                    notificationStatus.style.color = 'red';
                }
            })
            .catch(error => {
                const notificationStatus = document.getElementById('notification-status');
                notificationStatus.textContent = 'Error: ' + error.message;
                notificationStatus.style.color = 'red';
            });
        });
    }
});




