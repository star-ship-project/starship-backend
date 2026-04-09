// --- Show & Hide Password Logic ---
const passwordInput = document.getElementById('password');
const toggleBtn = document.getElementById('toggleBtn');
const eyeIcon = document.getElementById('eyeIcon');

// SVG paths for the eye icons
const eyeOpenSVG = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />`;

const eyeClosedSVG = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />`;

// Toggle event listener
toggleBtn.addEventListener('click', () => {
    const isPassword = passwordInput.getAttribute('type') === 'password';
    passwordInput.setAttribute('type', isPassword ? 'text' : 'password');
    eyeIcon.innerHTML = isPassword ? eyeClosedSVG : eyeOpenSVG;
});

// --- Authentication Logic ---
const loginForm = document.getElementById('loginForm');
const usernameInput = document.getElementById('username');

// Login form submission event listener
loginForm.addEventListener('submit', function(event) {
    //  Prevent the default form submission (page reload)
    event.preventDefault(); 

    //  Capture the current input values
    const enteredUsername = usernameInput.value;
    const enteredPassword = passwordInput.value;

    //  Hardcoded Validation
    //  Hardcoded for now, can and will be changed later if possible
    if (enteredUsername === 'admin1' && enteredPassword === '12345') {
        
        // When successful: Redirect to the main dashboard
        window.location.href = 'dashboard/index.html';
    } else {
        // Failure: Show error and clear password
        alert('Authentication Failed: Invalid Username or Security Code.');
        passwordInput.value = ''; 
        passwordInput.focus(); 
    }
});