/**
 * Password Visibility Toggle
 * Toggles password field visibility and eye icon
 */
function togglePasswordVisibility(inputId, iconId) {
    const passwordInput = document.getElementById(inputId);
    const eyeIcon = document.getElementById(iconId);
    const eyeIconClosed = document.getElementById(iconId + 'Closed');
    
    if (passwordInput && eyeIcon && eyeIconClosed) {
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            eyeIcon.classList.add('hidden');
            eyeIconClosed.classList.remove('hidden');
        } else {
            passwordInput.type = 'password';
            eyeIcon.classList.remove('hidden');
            eyeIconClosed.classList.add('hidden');
        }
    }
}
