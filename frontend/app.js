const API_BASE = "http://127.0.0.1:8000";

async function analyzeStock() {
    const stock = document.getElementById("stock-select").value;
    const date = document.getElementById("date-input").value;

    // Get the endpoint created by main.py
    let url = `${API_BASE}/stocks/analyze?stock=${stock}`;
    if (date) {
        url += `&date=${date}`;
    }
    
    // Send an HTTP POST request
    const response = await fetch(url, { method: "POST" });

    // Store the response body content as a JSON object
    const data = await response.json();

    document.getElementById("stock-title").textContent = data.name;
    document.getElementById("result").textContent = JSON.stringify(data, null, 2);

    // Hide the dashboard view
    document.getElementById("dashboard-view").style.display = "none";
    
    // Show the stock details
    document.getElementById("stock-view").style.display = "block";
}

// When the analyze button is clicked, run analyzeStock()
document.getElementById("analyze-btn").addEventListener("click", analyzeStock);
