/**
 * Theme Toggle Functionality
 * Handles dark/light mode switching
 */

// Toggle Theme Function
function toggleTheme() {
    const html = document.documentElement;
    html.classList.toggle('dark');
    const isDark = html.classList.contains('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');

    // Update icons (navbar)
    const sunIcons = document.querySelectorAll('#sunIconNavbar');
    const moonIcons = document.querySelectorAll('#moonIconNavbar');
    sunIcons.forEach(el => {
        if (el) {
            el.classList.toggle('hidden', !isDark);
            el.classList.toggle('block', isDark);
        }
    });
    moonIcons.forEach(el => {
        if (el) {
            el.classList.toggle('hidden', isDark);
            el.classList.toggle('block', !isDark);
        }
    });
}

// Initialize Theme on Page Load
document.addEventListener('DOMContentLoaded', function () {
    const html = document.documentElement;
    const currentTheme = localStorage.getItem('theme') || 'light';
    const isDark = currentTheme === 'dark';

    if (isDark) {
        html.classList.add('dark');
    } else {
        html.classList.remove('dark');
    }

    // Update icons on load
    const sunIcons = document.querySelectorAll('#sunIconNavbar');
    const moonIcons = document.querySelectorAll('#moonIconNavbar');
    sunIcons.forEach(el => {
        if (el) {
            el.classList.toggle('hidden', !isDark);
            el.classList.toggle('block', isDark);
        }
    });
    moonIcons.forEach(el => {
        if (el) {
            el.classList.toggle('hidden', isDark);
            el.classList.toggle('block', !isDark);
        }
    });

    // Attach event listener to theme toggle button
    const themeToggleBtn = document.getElementById('themeToggleNavbar');
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', toggleTheme);
    }
});
