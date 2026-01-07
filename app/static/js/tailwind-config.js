// Tailwind CSS Configuration for Light/Dark Theme
// This file configures Tailwind CSS with custom colors and dark mode support

// Configure Tailwind when it's available
(function configureTailwind() {
    if (typeof tailwind !== 'undefined') {
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        primary: '#18CB96',
                        primaryDark: '#17635B',
                        dark: '#1f2937',
                        gray: '#6b7280',
                        light: '#f9fafb',
                        darkBg: '#1E1E1E',
                        darkCard: '#2A2A2A',
                        darkSidebar: '#252525',
                    }
                }
            }
        };
    } else {
        // Retry if Tailwind hasn't loaded yet (for async loading scenarios)
        setTimeout(configureTailwind, 10);
    }
})();
