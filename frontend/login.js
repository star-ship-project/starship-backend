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
const usernameError = document.getElementById('usernameError');
const passwordError = document.getElementById('passwordError');
const authError = document.getElementById('authError'); // Grab the new global error

// Login form submission event listener
loginForm.addEventListener('submit', function(event) {
    // 1. Prevent the default form submission (page reload)
    event.preventDefault(); 

    // 2. Capture the current input values
    const enteredUsername = usernameInput.value.trim();
    const enteredPassword = passwordInput.value;

    // 3. Reset ALL error states on every submit attempt
    usernameError.classList.remove('show');
    passwordError.classList.remove('show');
    authError.classList.remove('show'); // Hide global error
    usernameInput.style.borderColor = '';
    passwordInput.style.borderColor = '';

    let hasEmptyFields = false;

    // 4. Check for empty fields simultaneously
    if (enteredUsername === '') {
        usernameError.classList.add('show');
        usernameInput.style.borderColor = '#ef4444'; 
        hasEmptyFields = true;
    }

    if (enteredPassword === '') {
        passwordError.classList.add('show');
        passwordInput.style.borderColor = '#ef4444'; 
        hasEmptyFields = true;
    }

    // Stop here if there are empty fields
    if (hasEmptyFields) return;

    // 5. Hardcoded Validation (Only runs if both fields have text)
    if (enteredUsername === 'admin1' && enteredPassword === '12345') {
        // Success: Redirect to the main console dashboard
        window.location.href = '/frontend/dashboard/index.html';
    } else {
        // Failure: Show inline vague error and clear password
        authError.classList.add('show'); 
        passwordInput.value = ''; 
        passwordInput.focus(); 
    }
});