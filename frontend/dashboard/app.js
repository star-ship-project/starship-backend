// Grab DOM elements
const buttons = document.querySelectorAll('.nav-btn');
const mainContentArea = document.getElementById('main-content');

// --- NEW: Logout Logic ---
const logoutBtn = document.querySelector('.logout-btn');

if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
        // 1. Add the fade-out class to the entire body
        document.body.classList.add('page-fade-out');

        // 2. Wait for the CSS animation to finish (400ms) before redirecting
        setTimeout(() => {
            window.location.href = '../login_page.html';
        }, 400); 
    });
}
// -------------------------

// Load the default view on startup
window.addEventListener('DOMContentLoaded', () => {
    loadComponent('table1'); 
});

// Sidebar Click Logic
buttons.forEach(button => {
    button.addEventListener('click', () => {
        // Update active button state
        buttons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');

        // Get the target filename and load it
        const targetId = button.getAttribute('data-target');
        loadComponent(targetId);
    });
});

// The Component Loader (The Modular Magic)
async function loadComponent(componentName) {
    try {
        // 1. Fetch the HTML layout for the specific table
        const response = await fetch(`components/${componentName}.html`);
        if (!response.ok) throw new Error(`Could not load ${componentName}.html`);
        
        // 2. Inject the HTML into the main container
        const html = await response.text();
        mainContentArea.innerHTML = html;

        // 3. Now that the table exists in the DOM, fetch the data to fill it
        if (componentName === 'table1') {
            fetchTable1();
        } else if (componentName === 'table2') {
            fetchTable2();
        } else if (componentName === 'table3') {
            fetchTable3();
        }
    } catch (error) {
        console.error("Component loading error:", error);
        mainContentArea.innerHTML = `<h2 style="color: #f87171; padding: 30px;">System Error: Failed to load module.</h2>`;
    }
}


// --- Data Fetching Functions ---

async function fetchTable1() {
    const tableBody = document.getElementById('alpha-table-body');
    if (!tableBody) return;

    try {
        /*
        ========================================================
        HOW TO CONNECT API (TABLE 1)
        ========================================================
        1. Uncomment the two lines below (fetch and response.json).
        2. Replace 'https://your-api.com/alpha' with API.
        3. Delete or comment out the "MOCK DATA".
        4. API should have matching array objects; properties matching c1, c2, c3, etc.
        5. API should have access to JSON file of the database not the SQL
        ========================================================
        */
        // const response = await fetch('https://your-api.com/alpha');
        // const data = await response.json();

        // --- MOCK DATA (Delete when API is ready) ---
        const data = [
            { c1: "A1", c2: "A2", c3: "A3", c4: "A4", c5: "A5", c6: "A6", c7: "A7", c8: "A8", c9: "A9", c10: "A10" },
            { c1: "B1", c2: "B2", c3: "B3", c4: "B4", c5: "B5", c6: "B6", c7: "B7", c8: "B8", c9: "B9", c10: "B10" }
        ];
        // --------------------------------------------

        tableBody.innerHTML = '';
        data.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.c1}</td><td>${item.c2}</td><td>${item.c3}</td><td>${item.c4}</td><td>${item.c5}</td>
                <td>${item.c6}</td><td>${item.c7}</td><td>${item.c8}</td><td>${item.c9}</td><td>${item.c10}</td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Alpha Data Error:", error);
        tableBody.innerHTML = `<tr><td colspan="10" style="color: #f87171;">Failed to load data.</td></tr>`;
    }
}

async function fetchTable2() {
    const tableBody = document.getElementById('beta-table-body');
    if (!tableBody) return;

    try {
        /*
        ========================================================
        HOW TO CONNECT API (TABLE 2)
        ========================================================
        1. Uncomment the two lines below (fetch and response.json).
        2. Replace 'https://your-api.com/alpha' with API.
        3. Delete or comment out the "MOCK DATA".
        4. API should have matching array objects;
        5. API should have access to JSON file of the database not the SQL
        ========================================================
        */
        // const response = await fetch('https://your-api.com/beta');
        // const data = await response.json();

        // --- MOCK DATA (Delete when API is ready) ---
        const data = [
            { sysA: "OK", sysB: "OK", sysC: "WARN", sysD: "OK", sysE: "OK", sysF: "ERR", sysG: "OK", sysH: "OK", sysI: "OK", sysJ: "OK" }
        ];
        // --------------------------------------------

        tableBody.innerHTML = '';
        const statusColor = (status) => status === 'ERR' ? '#f87171' : (status === 'WARN' ? '#fbbf24' : '#e2e8f0');
        
        data.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td style="color: ${statusColor(item.sysA)}">${item.sysA}</td>
                <td style="color: ${statusColor(item.sysB)}">${item.sysB}</td>
                <td style="color: ${statusColor(item.sysC)}">${item.sysC}</td>
                <td style="color: ${statusColor(item.sysD)}">${item.sysD}</td>
                <td style="color: ${statusColor(item.sysE)}">${item.sysE}</td>
                <td style="color: ${statusColor(item.sysF)}">${item.sysF}</td>
                <td style="color: ${statusColor(item.sysG)}">${item.sysG}</td>
                <td style="color: ${statusColor(item.sysH)}">${item.sysH}</td>
                <td style="color: ${statusColor(item.sysI)}">${item.sysI}</td>
                <td style="color: ${statusColor(item.sysJ)}">${item.sysJ}</td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Beta Data Error:", error);
        tableBody.innerHTML = `<tr><td colspan="10" style="color: #f87171;">Failed to load data.</td></tr>`;
    }
}

async function fetchTable3() {
    const tableBody = document.getElementById('crew-table-body');
    if (!tableBody) return;

    try {
        /*
        ========================================================
        HOW TO CONNECT API (TABLE 2)
        ========================================================
        1. Uncomment the two lines below (fetch and response.json).
        2. Replace 'https://your-api.com/alpha' with API.
        3. Delete or comment out the "MOCK DATA".
        4. API should have matching array objects;
        5. API should have access to JSON file of the database not the SQL
        ========================================================
        */
        // const response = await fetch('https://your-api.com/crew');
        // const data = await response.json();

        // --- MOCK DATA (Delete when API is ready) ---
        const data = [
            { id: "001", name: "Sarah Connor", rank: "Commander", status: "Active" },
            { id: "002", name: "Arthur Dent", rank: "Passenger", status: "Offline" }
        ];
        // --------------------------------------------

        tableBody.innerHTML = '';
        data.forEach(member => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${member.id}</td>
                <td>${member.name}</td>
                <td>${member.rank}</td>
                <td style="color: ${member.status === 'Active' ? '#4ade80' : '#f87171'}">
                    ${member.status}
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Crew Data Error:", error);
        tableBody.innerHTML = `<tr><td colspan="4" style="color: #f87171;">Failed to load data.</td></tr>`;
    }
}