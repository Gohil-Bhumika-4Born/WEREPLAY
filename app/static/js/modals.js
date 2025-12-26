/**
 * Modal Functions
 * Handles opening and closing of modals
 */

// Profile Dropdown Functions
// Note: closeProfileDropdown is defined globally because it's called from inline onclick handlers
function closeProfileDropdown() {
    const profileDropdown = document.getElementById('profileDropdown');
    const profileDropdownBtn = document.getElementById('profileDropdownBtn');

    if (profileDropdown) {
        profileDropdown.classList.add('hidden');
    }
    if (profileDropdownBtn) {
        profileDropdownBtn.setAttribute('aria-expanded', 'false');
    }
}

// Initialize profile dropdown on page load
document.addEventListener('DOMContentLoaded', function () {
    const profileDropdownBtn = document.getElementById('profileDropdownBtn');
    const profileDropdown = document.getElementById('profileDropdown');

    if (profileDropdownBtn && profileDropdown) {
        profileDropdownBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            const isHidden = profileDropdown.classList.contains('hidden');
            profileDropdown.classList.toggle('hidden');
            profileDropdownBtn.setAttribute('aria-expanded', !isHidden);
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function (e) {
            if (!profileDropdownBtn.contains(e.target) && !profileDropdown.contains(e.target)) {
                closeProfileDropdown();
            }
        });
    }
});

// Logout Modal Functions
function openLogoutModal() {
    const modal = document.getElementById('logoutModal');
    if (modal) {
        modal.classList.remove('hidden');
        closeProfileDropdown();
    }
}

function closeLogoutModal() {
    const modal = document.getElementById('logoutModal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

function confirmLogout() {
    window.location.href = '/logout';
}

// Welcome Modal Functions
function openWelcomeModal() {
    const modal = document.getElementById('welcomeModal');
    if (modal) {
        modal.classList.remove('hidden');
    }
}

function closeWelcomeModal() {
    const modal = document.getElementById('welcomeModal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

// Check if we should show welcome modal (e.g., from URL parameter or session)
document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('welcome') === 'true') {
        openWelcomeModal();
    }
});
