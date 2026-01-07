/**
 * Toast Notification System
 * Handles displaying beautiful, animated toast notifications
 */

class Toast {
    constructor() {
        this.container = document.getElementById('toast-container');
        if (!this.container) {
            this.createContainer();
        }
    }

    createContainer() {
        this.container = document.createElement('div');
        this.container.id = 'toast-container';
        this.container.className = 'fixed top-5 right-5 z-[9999] flex flex-col gap-3 pointer-events-none';
        document.body.appendChild(this.container);
    }

    /**
     * Show a toast notification
     * @param {string} message - The message to display
     * @param {string} type - 'success', 'error', 'warning', or 'info'
     * @param {number} duration - Duration in ms before auto-dismiss (default: 4000)
     */
    show(message, type = 'info', duration = 4000) {
        // Validation
        if (!message) return;

        // Create toast element
        const toast = document.createElement('div');
        toast.className = `
            pointer-events-auto
            flex items-center gap-3 px-4 py-3 rounded-xl shadow-lg shadow-gray-200/50 backdrop-blur-md border outline-none
            transform transition-all duration-300 ease-out translate-x-full opacity-0
            min-w-[300px] max-w-sm
        `;

        // Style based on type
        const styles = {
            success: {
                bg: 'bg-white/95',
                border: 'border-green-100',
                iconColor: 'text-green-500',
                icon: `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>`
            },
            error: {
                bg: 'bg-white/95',
                border: 'border-red-100',
                iconColor: 'text-red-500',
                icon: `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>`
            },
            warning: {
                bg: 'bg-white/95',
                border: 'border-yellow-100',
                iconColor: 'text-yellow-500',
                icon: `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>`
            },
            info: {
                bg: 'bg-white/95',
                border: 'border-blue-100',
                iconColor: 'text-blue-500',
                icon: `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>`
            }
        };

        const style = styles[type] || styles.info;

        // Apply dynamic classes
        toast.classList.add(style.bg.split(' ')[0]); // simplistic fix, relying on template literal above for most styling
        // Tailwind arbitrary values and opacity/blur support might depend on config, reusing existing patterns if possible.
        // Let's stick to standard classes visible in other files: 'bg-white', 'text-dark', etc.
        // Adapting for glassmorphism
        toast.className += ` ${style.bg} ${style.border}`;

        // Content
        toast.innerHTML = `
            <div class="${style.iconColor} shrink-0">
                ${style.icon}
            </div>
            <div class="flex-1">
                <p class="text-sm font-medium text-gray-800">${message}</p>
            </div>
            <button class="shrink-0 text-gray-400 hover:text-gray-600 transition-colors focus:outline-none" onclick="this.parentElement.remove()">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
            </button>
        `;

        // Add to DOM
        this.container.appendChild(toast);

        // Animate In
        // Use requestAnimationFrame to ensure DOM is updated before adding classes for transition
        requestAnimationFrame(() => {
            toast.classList.remove('translate-x-full', 'opacity-0');
        });

        // Auto Dismiss
        if (duration > 0) {
            setTimeout(() => {
                this.dismiss(toast);
            }, duration);
        }
    }

    dismiss(toast) {
        toast.classList.add('translate-x-full', 'opacity-0');
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 300); // Wait for transition to finish
    }
}

// Global instance
window.toast = new Toast();
