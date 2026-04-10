// Grab DOM elements
const buttons = document.querySelectorAll('.nav-btn');
const mainContentArea = document.getElementById('main-content');

// --- Logout Logic ---
const logoutBtn = document.querySelector('.logout-btn');
if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
        document.body.classList.add('page-fade-out');
        setTimeout(() => {
            window.location.href = '../login_page.html';
        }, 400); 
    });
}

// Load the default view on startup
window.addEventListener('DOMContentLoaded', () => {
    loadComponent('schools'); 
});

// Sidebar Click Logic
buttons.forEach(button => {
    button.addEventListener('click', () => {
        buttons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        const targetId = button.getAttribute('data-target');
        loadComponent(targetId);
    });
});

// The Component Loader
async function loadComponent(componentName) {
    try {
        const response = await fetch(`components/${componentName}.html`);
        if (!response.ok) throw new Error(`Could not load ${componentName}.html`);
        
        const html = await response.text();
        mainContentArea.innerHTML = html;

        // Route to the correct fetch function
        if (componentName === 'schools') fetchSchools();
        else if (componentName === 'teachers-bio') fetchTeachersBio();
        else if (componentName === 'teachers-professional') fetchTeachersProfessional();
        else if (componentName === 'qualifications') fetchQualifications();
        else if (componentName === 'star-events') fetchStarEvents();

    } catch (error) {
        console.error("Component loading error:", error);
        mainContentArea.innerHTML = `<h2 style="color: #f87171; padding: 30px;">System Error: Failed to load module.</h2>`;
    }
}

// --- Data Fetching Functions ---
// Note: Uncomment fetch blocks when FastAPI is running (usually on port 8000)

async function fetchSchools() {
    const tbody = document.getElementById('schools-tbody');
    if (!tbody) return;
    try {
        const response = await fetch('http://localhost:8000/api/schools');
        const data = await response.json();
        
        // const data = [
        //     { school_id: "SCH001", name: "PUP Laboratory High School", region: "NCR", division: "Manila", total_enrollment: 500 }
        // ];

        tbody.innerHTML = data.map(item => `
            <tr>
                <td>${item.school_id}</td>
                <td>${item.name}</td>
                <td>${item.region}</td>
                <td>${item.division}</td>
                <td>${item.total_enrollment}</td>
            </tr>
        `).join('');
    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="5">Failed to load data.</td></tr>`;
    }
}

async function fetchTeachersBio() {
    const tbody = document.getElementById('bio-tbody');
    if (!tbody) return;
    try {
        const response = await fetch('http://localhost:8000/api/teachers-bio');
        const data = await response.json();
        
        // const data = [
        //     { deped_id: "DEPED-101", school_id: "SCH001", first_name: "Maria", last_name: "Reyes", sex: "Female", age: 34, phone_number: "+639171234567" }
        // ];

        tbody.innerHTML = data.map(item => `
            <tr>
                <td>${item.deped_id}</td>
                <td>${item.school_id}</td>
                <td>${item.first_name} ${item.last_name}</td>
                <td>${item.sex}</td>
                <td>${item.age}</td>
                <td>${item.phone_number}</td>
            </tr>
        `).join('');
    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="6">Failed to load data.</td></tr>`;
    }
}

async function fetchTeachersProfessional() {
    const tbody = document.getElementById('prof-tbody');
    if (!tbody) return;
    try {
        const response = await fetch('http://localhost:8000/api/teachers-professional');
        const data = await response.json();
        
        // const data = [
        //     { teacher_name: "Maria Reyes", years_experience: 10, teaching_level: "SHS", role_position: "Master Teacher II", specialization: "Science", is_internet_access: 1, device_count: 2 }
        // ];

        tbody.innerHTML = data.map(item => `
            <tr>
                <td>${item.teacher_name}</td>
                <td>${item.years_experience}</td>
                <td>${item.teaching_level}</td>
                <td>${item.role_position}</td>
                <td>${item.specialization}</td>
                <td>${item.is_internet_access ? 'Yes' : 'No'}</td>
                <td>${item.device_count}</td>
            </tr>
        `).join('');
    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="7">Failed to load data.</td></tr>`;
    }
}

async function fetchQualifications() {
    const tbody = document.getElementById('qual-tbody');
    if (!tbody) return;
    try {
        const response = await fetch('http://localhost:8000/api/qualifications');
        const data = await response.json();
        
        // const data = [
        //     { teacher_name: "Maria Reyes", cert_name: "Advanced Physics Certification", category: "Technical", awarding_body: "DOST", date_obtained: "2023-05-20" }
        // ];

        tbody.innerHTML = data.map(item => `
            <tr>
                <td>${item.teacher_name}</td>
                <td>${item.cert_name}</td>
                <td>${item.category}</td>
                <td>${item.awarding_body}</td>
                <td>${item.date_obtained}</td>
            </tr>
        `).join('');
    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="5">Failed to load data.</td></tr>`;
    }
}

async function fetchStarEvents() {
    const tbody = document.getElementById('events-tbody');
    if (!tbody) return;
    try {
        const response = await fetch('http://localhost:8000/api/star-events');
        const data = await response.json();
        
        //mock data
        // const data = [
        //     { teacher_name: "Maria Reyes", event_title: "International Nuclear Camp 2026", event_type: "Nuclear Camp", event_date: "2026-03-15" }
        // ];

        tbody.innerHTML = data.map(item => `
            <tr>
                <td>${item.teacher_name}</td>
                <td>${item.event_title}</td>
                <td>${item.event_type}</td>
                <td>${item.event_date}</td>
            </tr>
        `).join('');
    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="4">Failed to load data.</td></tr>`;
    }
}