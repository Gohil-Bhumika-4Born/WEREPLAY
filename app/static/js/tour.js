/**
 * WeReplay Guided Tour System
 * Smooth, animated first-time user onboarding tour
 */

class GuidedTour {
    constructor() {
        this.currentStep = 0;
        this.steps = [];
        this.overlay = null;
        this.tooltip = null;
        this.highlightBox = null;
        this.isActive = false;
        this.settings = this.loadSettings();
        
        // Tour configurations
        this.tours = {
            main: {
                key: 'hasSeenMainTour',
                steps: [
                    {
                        target: null, // Center modal
                        title: 'Welcome to WeReplayx 👋',
                        description: 'Let us give you a quick tour of the platform.',
                        position: 'center',
                        buttons: ['start', 'skip']
                    },
                    {
                        target: 'a[href="chat-reports.html"]',
                        title: 'Chat Reports',
                        description: 'Monitor conversations, sentiments, issues, and topic trends here.',
                        position: 'right',
                        buttons: ['next', 'skip']
                    },
                    {
                        target: 'a[href="ai-training.html"]',
                        title: 'AI Training Dashboard',
                        description: 'Training runs automatically when you upload documents. Track AI processing and accuracy here.',
                        position: 'right',
                        buttons: ['next', 'skip']
                    },
                    {
                        target: 'a[href="training-history.html"]',
                        title: 'Training History',
                        description: 'View your AI training history and track the progress of your training sessions.',
                        position: 'right',
                        buttons: ['next', 'skip']
                    },
                    {
                        target: 'a[href="notifications.html"]',
                        title: 'Notifications',
                        description: 'Stay updated with training results, errors, billing alerts, and system messages.',
                        position: 'bottom',
                        buttons: ['next', 'skip']
                    },
                    {
                        target: '#profileDropdownBtn',
                        title: 'Profile',
                        description: 'Access your profile settings, change password, and manage your account here. You\'re all set!',
                        position: 'bottom',
                        buttons: ['done']
                    }
                ]
            },
            aiTraining: {
                key: 'hasSeenAITrainingTour',
                steps: [
                    {
                        target: null,
                        title: 'Welcome to AI Training 🤖',
                        description: 'Let\'s explore the key features of the AI Training dashboard.',
                        position: 'center',
                        buttons: ['start', 'skip']
                    },
                    {
                        target: '#trainBtn',
                        title: 'Train AI Now',
                        description: 'Click here to start training your AI model with selected documents. Training happens automatically!',
                        position: 'bottom',
                        buttons: ['next', 'skip']
                    },
                    {
                        target: 'a[href="documents-upload.html"]',
                        title: 'Upload Documents',
                        description: 'Upload new documents here to train your AI. Supports PDFs, text files, and more.',
                        position: 'bottom',
                        buttons: ['next', 'skip']
                    },
                    {
                        target: 'a[href="documents.html"]',
                        title: 'View Document List',
                        description: 'See all your uploaded documents and manage them from this section.',
                        position: 'bottom',
                        buttons: ['next', 'skip']
                    },
                    {
                        target: '.grid.grid-cols-2.sm\\:grid-cols-4',
                        title: 'Training Stats',
                        description: 'Monitor last training time, accuracy score, and total tokens processed here.',
                        position: 'bottom',
                        buttons: ['next', 'skip']
                    },
                    {
                        target: null,
                        title: 'You\'re Ready! 🎉',
                        description: 'Start uploading documents and train your AI to provide better customer support.',
                        position: 'center',
                        buttons: ['done']
                    }
                ]
            }
        };
        
        this.init();
    }
    
    init() {
        // Bind keyboard events
        this.bindKeyboardEvents();
        // Create overlay and tooltip elements when needed (on first tour start)
    }
    
    createTourElements() {
        // Only create if they don't exist
        if (this.overlay && document.body.contains(this.overlay)) {
            return; // Already created
        }
        
        // Overlay - no backdrop-blur, just semi-transparent dark background
        // The highlight box's box-shadow will handle the darkening effect
        this.overlay = document.createElement('div');
        this.overlay.id = 'tour-overlay';
        this.overlay.className = 'fixed inset-0 bg-black/50 z-[9998] transition-opacity duration-300 opacity-0 pointer-events-none';
        document.body.appendChild(this.overlay);
        
        // Highlight box - uses box-shadow to create darkening effect with cutout
        this.highlightBox = document.createElement('div');
        this.highlightBox.id = 'tour-highlight';
        this.highlightBox.className = 'fixed z-[9999] border-4 border-[#18CB96] rounded-xl transition-all duration-300 pointer-events-none bg-transparent';
        this.highlightBox.style.opacity = '0';
        this.highlightBox.style.transform = 'scale(0.95)';
        document.body.appendChild(this.highlightBox);
        
        // Tooltip
        this.tooltip = document.createElement('div');
        this.tooltip.id = 'tour-tooltip';
        this.tooltip.className = 'fixed z-[10000] bg-gradient-to-b from-white via-[#F6FFFB] to-[#ECFFF9] dark:from-[#1E1E1E] dark:via-[#1E1E1E] dark:to-[#1E1E1E] rounded-2xl shadow-2xl p-6 max-w-sm transition-all duration-300 pointer-events-auto';
        this.tooltip.style.opacity = '0';
        this.tooltip.style.transform = 'scale(0.9) translateY(-10px)';
        document.body.appendChild(this.tooltip);
    }
    
    loadSettings() {
        const saved = localStorage.getItem('wereplay_tour_settings');
        if (saved) {
            try {
                return JSON.parse(saved);
            } catch (e) {
                return {};
            }
        }
        return {};
    }
    
    saveSettings() {
        localStorage.setItem('wereplay_tour_settings', JSON.stringify(this.settings));
    }
    
    hasSeenTour(tourKey) {
        return this.settings[tourKey] === true;
    }
    
    markTourAsSeen(tourKey) {
        this.settings[tourKey] = true;
        this.saveSettings();
    }
    
    startTour(tourName = 'main') {
        const tour = this.tours[tourName];
        if (!tour) return;
        
        if (this.hasSeenTour(tour.key) && !this.settings.forceShowTour) {
            return; // Don't show if already seen
        }
        
        // Ensure DOM elements are created
        if (!this.overlay || !document.body.contains(this.overlay)) {
            this.createTourElements();
        }
        
        // Filter steps - only include those with valid targets or center modals
        this.steps = [];
        for (let step of tour.steps) {
            if (!step.target) {
                // Center modal - always include
                this.steps.push(step);
            } else {
                const element = document.querySelector(step.target);
                if (element) {
                    this.steps.push(step);
                } else if (step.fallback) {
                    const fallbackElement = document.querySelector(step.fallback);
                    if (fallbackElement) {
                        step.target = step.fallback;
                        this.steps.push(step);
                    }
                }
                // Skip step if no element found and no fallback
            }
        }
        
        if (this.steps.length === 0) return;
        
        this.currentStep = 0;
        this.isActive = true;
        document.body.style.overflow = 'hidden';
        this.showStep(0);
    }
    
    showStep(stepIndex) {
        if (stepIndex < 0 || stepIndex >= this.steps.length) {
            this.endTour();
            return;
        }
        
        this.currentStep = stepIndex;
        const step = this.steps[stepIndex];
        
        // Show overlay
        this.overlay.classList.remove('opacity-0', 'pointer-events-none');
        this.overlay.classList.add('opacity-100');
        
        // If center modal (no target)
        if (!step.target) {
            this.hideHighlight();
            this.showCenterModal(step);
            return;
        }
        
        // Find target element
        const targetElement = document.querySelector(step.target);
        if (!targetElement) {
            // Skip this step if element not found
            this.showStep(stepIndex + 1);
            return;
        }
        
        // Scroll to element smoothly
        targetElement.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'nearest' });
        
        // Wait for scroll, then show highlight and tooltip
        setTimeout(() => {
            this.showHighlight(targetElement);
            this.showTooltip(targetElement, step, stepIndex);
        }, 300);
    }
    
    showHighlight(element) {
        const rect = element.getBoundingClientRect();
        const padding = 12;
        
        // Calculate position (fixed positioning relative to viewport)
        const left = rect.left - padding;
        const top = rect.top - padding;
        const width = rect.width + padding * 2;
        const height = rect.height + padding * 2;
        
        // Update highlight box position
        this.highlightBox.style.left = `${left}px`;
        this.highlightBox.style.top = `${top}px`;
        this.highlightBox.style.width = `${width}px`;
        this.highlightBox.style.height = `${height}px`;
        this.highlightBox.style.opacity = '1';
        this.highlightBox.style.transform = 'scale(1)';
        this.highlightBox.style.pointerEvents = 'none';
        
        // Use box-shadow to create darkening effect (spotlight effect)
        // The shadow spreads outward, creating darkness everywhere except inside the highlight
        const shadowSpread = Math.max(window.innerWidth, window.innerHeight) * 2;
        this.highlightBox.style.boxShadow = `
            0 0 0 ${shadowSpread}px rgba(0, 0, 0, 0.75),
            0 0 40px rgba(24, 203, 150, 0.8),
            inset 0 0 20px rgba(24, 203, 150, 0.15)
        `;
        
        // Pulse animation for border
        this.highlightBox.style.animation = 'tourPulse 2s ease-in-out infinite';
        
        // Ensure element is visible above overlay and highlight
        // The box-shadow on highlight box creates the darkening effect
        // The element itself needs to be above the overlay (z-9998) and highlight box (z-9999)
        const originalZIndex = element.style.zIndex;
        const originalPosition = window.getComputedStyle(element).position;
        element.setAttribute('data-tour-original-z-index', originalZIndex || '');
        element.setAttribute('data-tour-original-position', originalPosition);
        
        if (originalPosition === 'static') {
            element.style.position = 'relative';
        }
        element.style.zIndex = '10001';
        
        // Store reference for cleanup
        this.currentHighlightedElement = element;
    }
    
    createOverlayCutout(x, y, width, height, padding) {
        // Box-shadow on highlight box handles the darkening
        // Element visibility ensured by z-index
    }
    
    removeOverlayCutout() {
        // No cleanup needed
    }
    
    hideHighlight() {
        this.highlightBox.style.opacity = '0';
        this.highlightBox.style.transform = 'scale(0.95)';
        this.highlightBox.style.animation = 'none';
        this.highlightBox.style.boxShadow = '';
        
        // Reset element styles
        if (this.currentHighlightedElement) {
            const originalZIndex = this.currentHighlightedElement.getAttribute('data-tour-original-z-index');
            const originalPosition = this.currentHighlightedElement.getAttribute('data-tour-original-position');
            
            if (originalZIndex !== null) {
                this.currentHighlightedElement.style.zIndex = originalZIndex || '';
            } else {
                this.currentHighlightedElement.style.zIndex = '';
            }
            
            if (originalPosition && originalPosition === 'static') {
                this.currentHighlightedElement.style.position = '';
            }
            
            this.currentHighlightedElement.removeAttribute('data-tour-original-z-index');
            this.currentHighlightedElement.removeAttribute('data-tour-original-position');
            this.currentHighlightedElement = null;
        }
    }
    
    showTooltip(element, step, stepIndex) {
        const rect = element.getBoundingClientRect();
        // Build tooltip content first to get actual dimensions
        this.tooltip.innerHTML = this.buildTooltipContent(step, stepIndex);
        // Force a reflow to get accurate dimensions
        this.tooltip.style.visibility = 'hidden';
        this.tooltip.style.display = 'block';
        const tooltipRect = this.tooltip.getBoundingClientRect();
        const tooltipWidth = Math.min(tooltipRect.width || 384, window.innerWidth - 40);
        const tooltipHeight = tooltipRect.height || 200;
        this.tooltip.style.visibility = '';
        
        let left, top;
        const padding = 20;
        
        // Position tooltip based on step.position
        switch (step.position) {
            case 'right':
                left = rect.right + padding;
                top = rect.top + (rect.height / 2) - (tooltipHeight / 2);
                // Adjust if off-screen
                if (left + tooltipWidth > window.innerWidth - padding) {
                    left = rect.left - tooltipWidth - padding;
                    if (left < padding) {
                        left = padding;
                        top = rect.bottom + padding;
                        if (top + tooltipHeight > window.innerHeight - padding) {
                            top = rect.top - tooltipHeight - padding;
                        }
                    }
                }
                if (top < padding) top = padding;
                if (top + tooltipHeight > window.innerHeight - padding) {
                    top = window.innerHeight - tooltipHeight - padding;
                }
                break;
            case 'left':
                left = rect.left - tooltipWidth - padding;
                top = rect.top + (rect.height / 2) - (tooltipHeight / 2);
                // Adjust if off-screen
                if (left < padding) {
                    left = rect.right + padding;
                }
                if (top < padding) top = padding;
                if (top + tooltipHeight > window.innerHeight - padding) {
                    top = window.innerHeight - tooltipHeight - padding;
                }
                break;
            case 'top':
                left = rect.left + (rect.width / 2) - (tooltipWidth / 2);
                top = rect.top - tooltipHeight - padding;
                if (left < padding) left = padding;
                if (left + tooltipWidth > window.innerWidth - padding) {
                    left = window.innerWidth - tooltipWidth - padding;
                }
                if (top < padding) {
                    top = rect.bottom + padding;
                }
                break;
            case 'bottom':
                left = rect.left + (rect.width / 2) - (tooltipWidth / 2);
                top = rect.bottom + padding;
                if (left < padding) left = padding;
                if (left + tooltipWidth > window.innerWidth - padding) {
                    left = window.innerWidth - tooltipWidth - padding;
                }
                if (top + tooltipHeight > window.innerHeight - padding) {
                    top = rect.top - tooltipHeight - padding;
                }
                break;
            default:
                left = rect.right + padding;
                top = rect.top;
        }
        
        this.tooltip.style.left = `${left}px`;
        this.tooltip.style.top = `${top}px`;
        this.tooltip.style.maxWidth = `${tooltipWidth}px`;
        
        // Animate in
        setTimeout(() => {
            this.tooltip.style.opacity = '1';
            this.tooltip.style.transform = 'scale(1) translateY(0)';
        }, 100);
    }
    
    showCenterModal(step) {
        const centerX = window.innerWidth / 2;
        const centerY = window.innerHeight / 2;
        
        this.tooltip.innerHTML = this.buildTooltipContent(step, this.currentStep);
        this.tooltip.style.left = `${centerX}px`;
        this.tooltip.style.top = `${centerY}px`;
        this.tooltip.style.transform = 'translate(-50%, -50%) scale(0.9)';
        this.tooltip.style.maxWidth = '500px';
        
        setTimeout(() => {
            this.tooltip.style.opacity = '1';
            this.tooltip.style.transform = 'translate(-50%, -50%) scale(1)';
        }, 100);
    }
    
    buildTooltipContent(step, stepIndex) {
        const totalSteps = this.steps.length;
        const isFirst = stepIndex === 0;
        const isLast = stepIndex === totalSteps - 1;
        
        let buttonsHTML = '';
        
        if (step.buttons) {
            buttonsHTML = '<div class="flex items-center justify-end gap-3 mt-6">';
            
            step.buttons.forEach(btn => {
                switch (btn) {
                    case 'start':
                        buttonsHTML += `<button onclick="window.tour.nextStep()" class="px-6 py-2.5 bg-[#18CB96] hover:bg-[#17635B] text-white rounded-xl font-medium transition-all duration-200 shadow-md hover:shadow-lg hover:-translate-y-0.5">Start Tour</button>`;
                        break;
                    case 'next':
                        buttonsHTML += `<button onclick="window.tour.nextStep()" class="px-6 py-2.5 bg-[#18CB96] hover:bg-[#17635B] text-white rounded-xl font-medium transition-all duration-200 shadow-md hover:shadow-lg hover:-translate-y-0.5">Next →</button>`;
                        break;
                    case 'skip':
                        buttonsHTML += `<button onclick="window.tour.skipTour()" class="px-4 py-2.5 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white rounded-xl font-medium transition-colors">Skip</button>`;
                        break;
                    case 'dashboard':
                        buttonsHTML += `<button onclick="window.tour.endTour()" class="px-6 py-2.5 bg-[#18CB96] hover:bg-[#17635B] text-white rounded-xl font-medium transition-all duration-200 shadow-md hover:shadow-lg hover:-translate-y-0.5">Go to Dashboard</button>`;
                        break;
                    case 'done':
                        buttonsHTML += `<button onclick="window.tour.endTour()" class="px-6 py-2.5 bg-[#18CB96] hover:bg-[#17635B] text-white rounded-xl font-medium transition-all duration-200 shadow-md hover:shadow-lg hover:-translate-y-0.5">Done</button>`;
                        break;
                    case 'dontShow':
                        buttonsHTML += `<label class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-300 cursor-pointer"><input type="checkbox" id="dontShowTour" class="rounded border-gray-300 text-[#18CB96] focus:ring-[#18CB96]"> Don't show this tour again</label>`;
                        break;
                }
            });
            
            buttonsHTML += '</div>';
        }
        
        return `
            <div class="relative">
                ${!isFirst && !isLast ? `<div class="text-xs text-gray-500 dark:text-gray-400 mb-2">Step ${stepIndex + 1} of ${totalSteps - 1}</div>` : ''}
                <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">${step.title}</h3>
                <p class="text-sm text-gray-600 dark:text-gray-300">${step.description}</p>
                ${buttonsHTML}
            </div>
        `;
    }
    
    nextStep() {
        if (this.currentStep < this.steps.length - 1) {
            this.hideCurrentStep();
            setTimeout(() => {
                this.showStep(this.currentStep + 1);
            }, 300);
        } else {
            this.endTour();
        }
    }
    
    previousStep() {
        if (this.currentStep > 0) {
            this.hideCurrentStep();
            setTimeout(() => {
                this.showStep(this.currentStep - 1);
            }, 300);
        }
    }
    
    skipTour() {
        this.endTour();
    }
    
    hideCurrentStep() {
        this.tooltip.style.opacity = '0';
        this.tooltip.style.transform = 'scale(0.9) translateY(-10px)';
        this.hideHighlight();
    }
    
    endTour() {
        const dontShow = document.getElementById('dontShowTour');
        if (dontShow && dontShow.checked) {
            this.markTourAsSeen('hasSeenMainTour');
        }
        
        this.hideCurrentStep();
        this.overlay.classList.remove('opacity-100');
        this.overlay.classList.add('opacity-0', 'pointer-events-none');
        
        setTimeout(() => {
            this.isActive = false;
            document.body.style.overflow = '';
            if (this.currentStep === this.steps.length - 1) {
                // Last step - tour completed
            }
        }, 300);
    }
    
    bindKeyboardEvents() {
        document.addEventListener('keydown', (e) => {
            if (!this.isActive) return;
            
            switch (e.key) {
                case 'ArrowRight':
                case 'ArrowDown':
                    e.preventDefault();
                    this.nextStep();
                    break;
                case 'ArrowLeft':
                case 'ArrowUp':
                    e.preventDefault();
                    this.previousStep();
                    break;
                case 'Escape':
                    e.preventDefault();
                    this.skipTour();
                    break;
            }
        });
    }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes tourPulse {
        0%, 100% {
            box-shadow: 0 0 0 0 rgba(24, 203, 150, 0.7);
        }
        50% {
            box-shadow: 0 0 0 10px rgba(24, 203, 150, 0);
        }
    }
    
    #tour-tooltip::before {
        content: '';
        position: absolute;
        width: 0;
        height: 0;
        border: 12px solid transparent;
    }
    
    #tour-tooltip.position-right::before {
        left: -24px;
        top: 50%;
        transform: translateY(-50%);
        border-right-color: #ECFFF9;
    }
    
    .dark #tour-tooltip.position-right::before {
        border-right-color: #1E1E1E;
    }
`;
document.head.appendChild(style);

// Initialize tour immediately (elements created lazily)
if (typeof window !== 'undefined') {
    window.tour = new GuidedTour();
    
    // Utility function to reset tour (for testing)
    // Usage: resetTour() in browser console
    window.resetTour = function() {
        localStorage.removeItem('wereplay_tour_settings');
        if (window.tour) {
            window.tour.settings = {};
            window.tour.startTour('main');
        }
    };
}

