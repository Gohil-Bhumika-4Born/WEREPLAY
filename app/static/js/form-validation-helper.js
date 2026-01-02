/**
 * Form Validation Helper
 * Automatically removes error styling when user interacts with form fields
 */

document.addEventListener('DOMContentLoaded', function() {
    // Remove error styling when user starts typing/changing field
    const allInputs = document.querySelectorAll('input, select, textarea');
    
    allInputs.forEach(input => {
        // For text inputs
        input.addEventListener('input', function() {
            removeFieldError(this);
        });
        
        // For select dropdowns
        if (input.tagName === 'SELECT') {
            input.addEventListener('change', function() {
                removeFieldError(this);
            });
        }
    });
    
    /**
     * Remove error styling and messages from a field
     * @param {HTMLElement} field - The input/select element
     */
    function removeFieldError(field) {
        // Remove red border classes
        field.classList.remove('border-red-500', '!border-red-500');
        
        // Find and hide the error message for this field
        const errorMessage = field.parentElement.querySelector('.text-red-600');
        if (errorMessage) {
            errorMessage.style.display = 'none';
        }
    }
});
