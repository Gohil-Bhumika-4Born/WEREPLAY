// Tailwind Configuration
window.tailwindConfig = {
  theme: {
    extend: {
      colors: {
        primary: '#18CB96',
        primaryDark: '#17635B',
        secondary: '#D1F5EA',
        dark: '#070808',
        gray: '#555555',
        light: '#F0F9F6',
        secondaryBtn: '#555555',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      container: {
        center: true,
        padding: '1rem',
        screens: {
          sm: '640px',
          md: '768px',
          lg: '1024px',
          xl: '1280px',
          '2xl': '1280px',
        },
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'pulse-glow': 'pulse-glow 3s ease-in-out infinite',
        'slide-up': 'slide-up 0.6s ease-out',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        'pulse-glow': {
          '0%, 100%': { opacity: '1', transform: 'scale(1)' },
          '50%': { opacity: '0.8', transform: 'scale(1.05)' },
        },
        'slide-up': {
          'from': { opacity: '0', transform: 'translateY(20px)' },
          'to': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    }
  }
};

// Initialize Tailwind Config
if (typeof tailwind !== 'undefined' && window.tailwindConfig) {
    tailwind.config = window.tailwindConfig;
}

// Form Utilities
// Form validation helper (if needed in future)
function validateForm(formElement) {
    return formElement.checkValidity();
}

// Phone number formatting helper
function formatPhoneNumber(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length > 15) value = value.slice(0, 15);
    input.value = value;
}

// Floating Label Functionality
function initFloatingLabels() {
    const floatingInputs = document.querySelectorAll('.floating-label-group input');
    
    floatingInputs.forEach(input => {
        const group = input.closest('.floating-label-group');
        
        // Check if input has value on load
        if (input.value) {
            group.classList.add('has-value');
        }
        
        // Handle input events
        input.addEventListener('input', function() {
            if (this.value) {
                group.classList.add('has-value');
            } else {
                group.classList.remove('has-value');
            }
        });
        
        // Handle blur event
        input.addEventListener('blur', function() {
            if (this.value) {
                group.classList.add('has-value');
            } else {
                group.classList.remove('has-value');
            }
        });
    });
}

// Initialize all functionality when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize floating labels
    initFloatingLabels();
    
    // Apply phone number formatting if phone input exists
    const phoneInput = document.getElementById('phone');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            formatPhoneNumber(e.target);
        });
    }
});

