    const API_BASE = "http://127.0.0.1:8000";
    let currentUserEmail = null;

    async function analyzeStock() {
        const stock = document.getElementById("stock-select").value;
        const date = document.getElementById("date-input").value;

        // Get the endpoint created by main.py
        let url = `${API_BASE}/stocks/analyze?stock=${stock}`;
        if (date) {
            url += `&date=${date}`;
        }
        
        // Send an HTTP POST request
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "X-User-Email": currentUserEmail
            }
        });

        // Store the response body content as a JSON object
        const data = await response.json();

        document.getElementById("stock-title").textContent = data.name;
        document.getElementById("result").textContent = JSON.stringify(data, null, 2);

        // Hide the dashboard view
        document.getElementById("dashboard-view").style.display = "none";
        
        // Show the stock details
        document.getElementById("stock-view").style.display = "block";
    }

    async function authRequest(endpoint) {
        const email = document.getElementById("email-input").value;
        const password = document.getElementById("password-input").value;
        const message = document.getElementById("auth-message");

        try {
            const url = `${API_BASE}/auth/${endpoint}`;
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({email, password})
            });

            const data = await response.json();
            if (!response.ok) {
                message.textContent = data.detail || "Authentication failed";
                return;
            }

            // Show success message
            message.textContent = data.message;

            currentUserEmail = email;

            // Make stocks visible if login successful
            document.getElementById("login-view").style.display = "none";
            document.getElementById("dashboard-view").style.display = "block";
        } catch(err) {
            message.textContent = "Server error";
        }
    }

    // When the analyze button is clicked, run analyzeStock()
    document.getElementById("analyze-btn").addEventListener("click", analyzeStock);

    // When the login or register button is clicked, run authRequest
    document.getElementById("login-btn").addEventListener("click", () => authRequest("login"));
    document.getElementById("register-btn").addEventListener("click", () => authRequest("register"));