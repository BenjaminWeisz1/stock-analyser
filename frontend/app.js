    const API_BASE = "https://stock-analyser.onrender.com";
    let currentUserEmail = null;

    function showError(message) {
        let errorBox = document.getElementById("error-message");

        if (!errorBox) {
            errorBox = document.createElement("div");
            errorBox.id = "error-message";
            errorBox.className = "error";
            document.getElementById("dashboard-view").prepend(errorBox);
        }

        errorBox.textContent = message;
    }

    function clearError() {
        const errorBox = document.getElementById("error-message");
        if (errorBox) {
            errorBox.remove();
        }
    }
    

    async function analyzeStock() {
        const stock = document.getElementById("stock-select").value;
        const date = document.getElementById("date-input").value;

        // Get the endpoint created by main.py
        let url = `${API_BASE}/stocks/analyze?stock=${stock}`;
        if (date) {
            url += `&date=${date}`;
        }

        try {
            // Send an HTTP POST request
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "X-User-Email": currentUserEmail
                }
            });

            let data = null

            // Store the response body content as a JSON object
            try {
                data = await response.json();
            } catch {
                data = null;
            }

            // Handle backend errors
            if (!response.ok) {
                if (data && data.detail) {
                    showError(data.detail);
                } else {
                    showError("No data available for the selected date.");
                }
                return;
            }

            // Clear any previous error message
            clearError()

            document.getElementById("stock-title").textContent = data.name;
            document.getElementById("stock-date").textContent = data.date;
            document.getElementById("stock-price").textContent = data.price.toFixed(2);
            document.getElementById("stock-returns").textContent = (data.returns * 100).toFixed(2);
            document.getElementById("stock-volume").textContent = data.volume.toLocaleString();

            const trend = document.getElementById("stock-trend");

            if (data.trend === "green") {
                trend.textContent = "🟢 Increasing";
                trend.className = "green";
            } else {
                trend.textContent = "🔴 Decreasing";
                trend.className = "red";
            }

            // Show the dashboard so the user can conveniently re-run analysis
            document.getElementById("dashboard-view").style.display = "block";
            
            // Show the stock details
            document.getElementById("stock-view").style.display = "block";

            // After showing results, scroll into view smoothly
            document.getElementById("stock-view").scrollIntoView({ behavior: "smooth" });
        } catch (err) {
            showError("Network error. Please try again.")
        }
        
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

            if (endpoint === "register") {
                // Registration does NOT log the user in
                message.textContent = "Registration successful. Please log in.";
                return;
            }

            // Show success message for logging in
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
    document
        .getElementById("analyze-btn")
        .addEventListener("click", (event) => {
            event.preventDefault();
            analyzeStock();
        });


    // When the login or register button is clicked, run authRequest
    document.getElementById("login-btn").addEventListener("click", () => authRequest("login"));
    document.getElementById("register-btn").addEventListener("click", () => authRequest("register"));