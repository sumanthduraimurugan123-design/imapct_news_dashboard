let allAlerts = [];


/* GET ALERTS */

async function getAlerts() {
    console.log("GET ALERTS FUNCTION IS RUNNING");

    const role =
        document.getElementById("role").value;

    const loading =
        document.getElementById("loading");

    const container =
        document.getElementById("alertsContainer");


    loading.style.display = "block";

    container.innerHTML = "";


    try {

        const response =
            await fetch(
                `http://127.0.0.1:8000/alerts/${role}`
            );


        if (!response.ok) {
            throw new Error("Unable to fetch alerts");
        }


        allAlerts = await response.json();


        displayAlerts(allAlerts);

        updateStatistics(allAlerts);


    } catch (error) {

        container.innerHTML = `
            <div class="alert-card critical">

                <h2>⚠️ Error</h2>

                <p>
                    Unable to connect to the server.
                    Please make sure your FastAPI server is running.
                </p>

            </div>
        `;

    } finally {

        loading.style.display = "none";
    }
}



/* DISPLAY ALERTS */

function displayAlerts(alerts) {

    const container =
        document.getElementById("alertsContainer");


    container.innerHTML = "";


    if (alerts.length === 0) {

        container.innerHTML = `
            <div class="alert-card">

                <h2>✅ No alerts</h2>

                <p>
                    No alerts are currently available
                    for this role.
                </p>

            </div>
        `;

        return;
    }


    alerts.forEach(alert => {

        const priority =
            alert.priority || "Medium";


        const score =
            alert.impact_score || 0;


        const card = document.createElement("div");

        card.className =
            `alert-card ${priority.toLowerCase()}`;


        card.innerHTML = `

            <span class="priority">
                ${priority}
            </span>

            <h2 class="alert-title">
                🚨 ${alert.event}
            </h2>

            <p class="impact">
                <strong>⚠ Impact:</strong>
                ${alert.impact_text}
            </p>

            <p class="action">
                <strong>💡 Recommended Action:</strong>
                ${alert.action_text}
            </p>

            <p class="score">
                📊 Impact Score:
                ${score}/100
            </p>

        `;


        container.appendChild(card);

    });
}



/* STATISTICS */

function updateStatistics(alerts) {

    document.getElementById("totalAlerts")
        .textContent = alerts.length;


    document.getElementById("criticalAlerts")
        .textContent =
        alerts.filter(
            a => a.priority === "Critical"
        ).length;


    document.getElementById("highAlerts")
        .textContent =
        alerts.filter(
            a => a.priority === "High"
        ).length;


    document.getElementById("mediumAlerts")
        .textContent =
        alerts.filter(
            a => a.priority === "Medium"
        ).length;
}



/* FILTER */

function filterAlerts(priority) {

    if (priority === "all") {

        displayAlerts(allAlerts);

        return;
    }


    const filtered =
        allAlerts.filter(
            alert =>
                alert.priority === priority
        );


    displayAlerts(filtered);
}
async function loadNews() {
    const container = document.getElementById("newsContainer");

    if (!container) {
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/news");

        if (!response.ok) {
            throw new Error("Failed to fetch news");
        }

        const data = await response.json();

        container.innerHTML = "";

        if (!data.articles || data.articles.length === 0) {
            container.innerHTML = "<p>No news available.</p>";
            return;
        }

        data.articles.forEach(article => {
            const card = document.createElement("div");

            card.className = "news-card";

            card.innerHTML = `
                <h3>${article.title || "Untitled"}</h3>
                <p>${article.description || "No description available."}</p>
                <a href="${article.url}" target="_blank">
                    Read Full News →
                </a>
            `;

            container.appendChild(card);
        });

    } catch (error) {
        console.error("News error:", error);

        container.innerHTML = `
            <p>Unable to load news.</p>
        `;
    }
}

loadNews();