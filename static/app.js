/**
 * ML Platform - Enhanced User Experience JavaScript
 * Modern interactions and animations for improved UX
 */

// ML Platform - Enhanced User Experience
const MLApp = {
  config: {
    animationDuration: 600,
    staggerDelay: 100,
    observerThreshold: 0.1,
    observerRootMargin: '0px 0px -50px 0px',
    navbarSelector: '.ml-navbar',
    navLinkSelector: '.ml-nav-link',
    dropdownSelector: '.ml-dropdown',
    cardSelector: '.card-interactive'
  },

  // Initialize the application
  init() {
    this.setupScrollAnimations();
    this.setupCardInteractions();
    this.setupNavigationEffects();
    this.setupFormEnhancements();
    this.setupLoadingStates();
    this.setupAccessibility();
    this.setupEnhancedValidation();
    this.setupEnhancedLoadingStates();
    console.log('🚀 ML Platform initialized successfully');
  },

  // Scroll-triggered animations
  setupScrollAnimations() {
    const observerOptions = {
      threshold: this.config.observerThreshold,
      rootMargin: this.config.observerRootMargin
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          entry.target.classList.add('animated');
        }
      });
    }, observerOptions);

    // Animate elements with fade-in classes
    document.querySelectorAll('.animate-fade-in-up, .animate-fade-in-left, .animate-fade-in-right').forEach(el => {
      el.style.opacity = '0';
      el.style.transform = this.getTransformForAnimation(el);
      el.style.transition = `all ${this.config.animationDuration}ms ease`;
      observer.observe(el);
    });

    // Stagger animations for card grids
    document.querySelectorAll('.row .col-md-4, .row .col-md-6, .row .col-lg-4').forEach((el, index) => {
      if (el.querySelector('.card')) {
        setTimeout(() => {
          el.style.opacity = '1';
          el.style.transform = 'translateY(0)';
        }, index * this.config.staggerDelay);
        
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = `all ${this.config.animationDuration}ms ease`;
      }
    });
  },
  // Enhanced card interactions
  setupCardInteractions() {
    // Interactive cards
    document.querySelectorAll(this.config.cardSelector).forEach(card => {
      card.addEventListener('mouseenter', () => {
        if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
          card.style.transform = 'translateY(-6px) scale(1.01)';
          card.style.boxShadow = 'var(--shadow-xl)';
        }
      });

      card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0) scale(1)';
        card.style.boxShadow = 'var(--shadow-sm)';
      });

      // Keyboard support
      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          const link = card.querySelector('a');
          if (link) link.click();
        }
      });
    });

    // Regular cards
    document.querySelectorAll('.card:not(.card-interactive)').forEach(card => {
      card.addEventListener('mouseenter', () => {
        if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
          card.style.transform = 'translateY(-2px)';
          card.style.boxShadow = 'var(--shadow-md)';
        }
      });

      card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0)';
        card.style.boxShadow = 'var(--shadow-sm)';
      });
    });
  },
  // Navigation enhancements
  setupNavigationEffects() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
          e.preventDefault();
          targetElement.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      });
    });

    // Enhanced dropdown functionality
    document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
      toggle.addEventListener('click', (e) => {
        e.preventDefault();
        const dropdown = toggle.nextElementSibling;
        if (dropdown) {
          dropdown.classList.toggle('show');
          toggle.setAttribute('aria-expanded', dropdown.classList.contains('show'));
        }
      });
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.dropdown')) {
        document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
          menu.classList.remove('show');
          const toggle = menu.previousElementSibling;
          if (toggle) toggle.setAttribute('aria-expanded', 'false');
        });
      }
    });

    // Navbar scroll effect (subtle)
    let lastScrollY = window.scrollY;
    const navbar = document.querySelector(this.config.navbarSelector);
    
    if (navbar) {
      window.addEventListener('scroll', () => {
        const currentScrollY = window.scrollY;
        
        if (currentScrollY > lastScrollY && currentScrollY > 150) {
          navbar.style.transform = 'translateY(-100%)';
        } else {
          navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollY = currentScrollY;
      });
    }
  },

  // Form enhancements
  setupFormEnhancements() {
    // Enhanced input focus effects
    document.querySelectorAll('.form-control').forEach(input => {
      input.addEventListener('focus', () => {
        input.parentElement.classList.add('focused');
      });

      input.addEventListener('blur', () => {
        input.parentElement.classList.remove('focused');
        if (input.value.trim() !== '') {
          input.parentElement.classList.add('filled');
        } else {
          input.parentElement.classList.remove('filled');
        }
      });

      // Check initial state
      if (input.value.trim() !== '') {
        input.parentElement.classList.add('filled');
      }
    });

    // Button loading states
    document.querySelectorAll('button[type="submit"], .btn-submit').forEach(btn => {
      btn.addEventListener('click', function() {
        if (!this.disabled) {
          this.classList.add('loading');
          const originalText = this.innerHTML;
          this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Procesando...';
          
          // Reset after 3 seconds (adjust based on your needs)
          setTimeout(() => {
            this.classList.remove('loading');
            this.innerHTML = originalText;
          }, 3000);
        }
      });
    });
  },

  // Loading states for navigation
  setupLoadingStates() {
    document.querySelectorAll('a[href]:not([href^="#"]):not([href^="javascript"])').forEach(link => {
      if (link.hostname === window.location.hostname) {
        link.addEventListener('click', function(e) {
          // Only show loading for internal links
          if (!this.hasAttribute('download') && !this.target) {
            MLApp.showPageLoader();
          }
        });
      }
    });

    // Hide loader when page loads
    window.addEventListener('load', () => {
      MLApp.hidePageLoader();
    });
  },

  // Accessibility improvements
  setupAccessibility() {
    // Keyboard navigation for cards
    document.querySelectorAll('.card-interactive').forEach(card => {
      card.setAttribute('tabindex', '0');
      card.setAttribute('role', 'button');
      
      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          card.click();
        }
      });
    });

    // Focus visible indicators
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        document.body.classList.add('keyboard-navigation');
      }
    });

    document.addEventListener('mousedown', () => {
      document.body.classList.remove('keyboard-navigation');
    });

    // Skip to main content link
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = 'Saltar al contenido principal';
    skipLink.className = 'skip-link';
    document.body.insertBefore(skipLink, document.body.firstChild);
  },

  // Enhanced form validation and user feedback
  setupEnhancedValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
      const inputs = form.querySelectorAll('input, select, textarea');
      
      inputs.forEach(input => {
        // Real-time validation feedback
        input.addEventListener('input', this.validateInput.bind(this));
        input.addEventListener('blur', this.validateInput.bind(this));
        
        // Enhanced focus effects for better accessibility
        input.addEventListener('focus', function() {
          this.parentElement.classList.add('form-field-focused');
          
          // Announce to screen readers
          if (this.getAttribute('aria-describedby')) {
            const description = document.getElementById(this.getAttribute('aria-describedby'));
            if (description) {
              description.setAttribute('aria-live', 'polite');
            }
          }
        });
        
        input.addEventListener('blur', function() {
          this.parentElement.classList.remove('form-field-focused');
        });
      });
    });
  },

  // Individual input validation with better UX
  validateInput(event) {
    const input = event.target;
    const value = input.value.trim();
    const type = input.type;
    const required = input.hasAttribute('required');
    
    // Remove previous validation classes
    input.classList.remove('is-valid', 'is-invalid');
    
    // Skip validation if field is empty and not required
    if (!value && !required) return;
    
    let isValid = true;
    let message = '';
    
    // Type-specific validation
    switch (type) {
      case 'number':
        const min = parseFloat(input.min);
        const max = parseFloat(input.max);
        const numValue = parseFloat(value);
        
        if (isNaN(numValue)) {
          isValid = false;
          message = 'Ingresa un número válido';
        } else if (min !== undefined && numValue < min) {
          isValid = false;
          message = `El valor debe ser mayor o igual a ${min}`;
        } else if (max !== undefined && numValue > max) {
          isValid = false;
          message = `El valor debe ser menor o igual a ${max}`;
        }
        break;
        
      case 'email':
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (value && !emailRegex.test(value)) {
          isValid = false;
          message = 'Ingresa un email válido';
        }
        break;
        
      default:
        if (required && !value) {
          isValid = false;
          message = 'Este campo es requerido';
        }
    }
    
    // Apply validation styles
    input.classList.add(isValid ? 'is-valid' : 'is-invalid');
    
    // Update or create feedback element
    this.updateValidationFeedback(input, message, isValid);
  },

  // Update validation feedback with accessibility
  updateValidationFeedback(input, message, isValid) {
    let feedback = input.parentElement.querySelector('.validation-feedback');
    
    if (!feedback) {
      feedback = document.createElement('div');
      feedback.className = 'validation-feedback';
      feedback.setAttribute('role', 'alert');
      feedback.setAttribute('aria-live', 'polite');
      input.parentElement.appendChild(feedback);
    }
    
    feedback.className = `validation-feedback ${isValid ? 'valid-feedback' : 'invalid-feedback'}`;
    feedback.textContent = message;
    feedback.style.display = message ? 'block' : 'none';
  },

  // Enhanced loading states for better perceived performance
  setupEnhancedLoadingStates() {
    const buttons = document.querySelectorAll('button[type="submit"]');
    
    buttons.forEach(button => {
      button.addEventListener('click', function(e) {
        const form = this.closest('form');
        
        // Validate form before showing loading state
        if (form && !form.checkValidity()) {
          return; // Let browser handle validation
        }
        
        // Show loading state
        const originalContent = this.innerHTML;
        this.disabled = true;
        this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Procesando...';
        this.classList.add('loading');
        
        // Store original content for recovery
        this.dataset.originalContent = originalContent;
        
        // Auto-recover after timeout (fallback)
        setTimeout(() => {
          if (this.classList.contains('loading')) {
            this.innerHTML = originalContent;
            this.disabled = false;
            this.classList.remove('loading');
          }
        }, 10000); // 10 second timeout
      });
    });
  },

  // Improved error handling and user feedback
  setupErrorHandling() {
    // Global error handler for better UX
    window.addEventListener('error', function(e) {
      console.error('JavaScript error:', e.error);
      
      // Show user-friendly error message
      MLApp.showNotification('Ha ocurrido un error. Por favor, recarga la página.', 'error');
    });
    
    // Handle form submission errors
    document.addEventListener('submit', function(e) {
      const form = e.target;
      
      // Add timeout for form submissions
      const submitTimeout = setTimeout(() => {
        MLApp.showNotification('La solicitud está tomando más tiempo del esperado...', 'warning');
      }, 5000);
      
      // Clear timeout if page unloads (submission successful)
      window.addEventListener('beforeunload', () => {
        clearTimeout(submitTimeout);
      });
    });
  },

  // User notification system
  showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.setAttribute('role', 'alert');
    notification.setAttribute('aria-live', 'polite');
    
    const icons = {
      success: 'fas fa-check-circle',
      error: 'fas fa-exclamation-triangle',
      warning: 'fas fa-exclamation-circle',
      info: 'fas fa-info-circle'
    };
    
    notification.innerHTML = `
      <i class="${icons[type] || icons.info} me-2"></i>
      <span>${message}</span>
      <button type="button" class="btn-close" aria-label="Cerrar notificación">
        <i class="fas fa-times"></i>
      </button>
    `;
    
    // Style the notification
    Object.assign(notification.style, {
      position: 'fixed',
      top: '20px',
      right: '20px',
      padding: '1rem 1.5rem',
      borderRadius: 'var(--radius-md)',
      backgroundColor: this.getNotificationColor(type),
      color: 'white',
      fontSize: 'var(--font-size-sm)',
      fontWeight: 'var(--font-weight-medium)',
      boxShadow: 'var(--shadow-lg)',
      zIndex: '9999',
      maxWidth: '400px',
      transform: 'translateX(100%)',
      transition: 'transform 0.3s ease'
    });
    
    document.body.appendChild(notification);
    
    // Animate in
    requestAnimationFrame(() => {
      notification.style.transform = 'translateX(0)';
    });
    
    // Close button functionality
    const closeBtn = notification.querySelector('.btn-close');
    closeBtn.addEventListener('click', () => {
      this.removeNotification(notification);
    });
    
    // Auto-remove after duration
    if (duration > 0) {
      setTimeout(() => {
        this.removeNotification(notification);
      }, duration);
    }
  },

  getNotificationColor(type) {
    const colors = {
      success: '#10b981',
      error: '#ef4444', 
      warning: '#f59e0b',
      info: '#3b82f6'
    };
    return colors[type] || colors.info;
  },

  removeNotification(notification) {
    notification.style.transform = 'translateX(100%)';
    setTimeout(() => {
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification);
      }
    }, 300);
  },

  // Utility functions
  getTransformForAnimation(element) {
    if (element.classList.contains('animate-fade-in-left')) {
      return 'translateX(-30px)';
    } else if (element.classList.contains('animate-fade-in-right')) {
      return 'translateX(30px)';
    }
    return 'translateY(30px)';
  },

  showPageLoader() {
    const loader = document.createElement('div');
    loader.id = 'page-loader';
    loader.innerHTML = `
      <div class="loader-content">
        <div class="loader-spinner"></div>
        <p>Cargando...</p>
      </div>
    `;
    document.body.appendChild(loader);
    
    // Force reflow before adding show class
    loader.offsetHeight;
    loader.classList.add('show');
  },

  hidePageLoader() {
    const loader = document.getElementById('page-loader');
    if (loader) {
      loader.classList.remove('show');
      setTimeout(() => loader.remove(), 300);
    }
  },

  // Progressive enhancement for images
  setupLazyLoading() {
    if ('IntersectionObserver' in window) {
      const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            img.classList.remove('lazy');
            imageObserver.unobserve(img);
          }
        });
      });

      document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
      });
    }
  },

  // Error handling
  setupErrorHandling() {
    window.addEventListener('error', (e) => {
      console.error('ML Platform Error:', e.error);
      // You could show a user-friendly error message here
    });

    // Handle unhandled promise rejections
    window.addEventListener('unhandledrejection', (e) => {
      console.error('ML Platform Promise Rejection:', e.reason);
    });
  }
};

// Custom CSS for enhanced interactions
const customStyles = `
  /* Loading States */
  #page-loader {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.95);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
  }

  #page-loader.show {
    opacity: 1;
    visibility: visible;
  }

  .loader-content {
    text-align: center;
  }

  .loader-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid #e2e8f0;
    border-top: 3px solid var(--primary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 1rem;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  /* Navbar scroll effect */
  .navbar {
    transition: transform 0.3s ease;
  }

  /* Skip link for accessibility */
  .skip-link {
    position: absolute;
    top: -40px;
    left: 6px;
    background: var(--primary-color);
    color: white;
    padding: 8px;
    text-decoration: none;
    border-radius: 0 0 4px 4px;
    z-index: 10000;
    transition: top 0.3s ease;
  }

  .skip-link:focus {
    top: 0;
    color: white;
  }

  /* Keyboard navigation styles */
  .keyboard-navigation *:focus {
    outline: 2px solid var(--primary-color) !important;
    outline-offset: 2px !important;
  }

  /* Form enhancements */
  .form-group.focused .form-label {
    color: var(--primary-color);
    transform: translateY(-2px);
  }

  .form-group.filled .form-label {
    color: var(--success-color);
  }

  /* Button loading state */
  .btn.loading {
    opacity: 0.7;
    pointer-events: none;
  }

  /* Enhanced card transitions */
  .card {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  /* Image lazy loading */
  img.lazy {
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  img:not(.lazy) {
    opacity: 1;
  }

  /* Progress bar animations */
  .progress-bar {
    transition: width 1.5s cubic-bezier(0.4, 0, 0.2, 1);
  }

  /* Responsive enhancements */
  @media (max-width: 768px) {
    .animate-fade-in-up {
      animation-delay: 0s !important;
    }
    
    .card-interactive:hover {
      transform: none !important;
    }
    
    .card-interactive:active {
      transform: scale(0.98) !important;
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
    }
    
    .card-interactive:hover {
      transform: none !important;
    }
  }
`;

// Add custom styles to the document
const styleSheet = document.createElement('style');
styleSheet.textContent = customStyles;
document.head.appendChild(styleSheet);

// ========================================
// CROSS-BROWSER COMPATIBILITY & POLYFILLS
// ========================================

// Polyfill for older browsers
const BrowserSupport = {
  init() {
    this.addIntersectionObserverPolyfill();
    this.addCustomEventPolyfill();
    this.addRequestAnimationFramePolyfill();
    this.detectBrowserFeatures();
  },

  // Intersection Observer polyfill for older browsers
  addIntersectionObserverPolyfill() {
    if (!('IntersectionObserver' in window)) {
      // Simple fallback for scroll animations
      const elements = document.querySelectorAll('.animate-fade-in-up, .animate-fade-in-left, .animate-fade-in-right');
      const handleScroll = () => {
        elements.forEach(el => {
          const rect = el.getBoundingClientRect();
          if (rect.top < window.innerHeight && rect.bottom > 0) {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
            el.classList.add('animated');
          }
        });
      };
      
      window.addEventListener('scroll', throttle(handleScroll, 100));
      handleScroll(); // Initial check
    }
  },

  // Custom Event polyfill for IE
  addCustomEventPolyfill() {
    if (typeof window.CustomEvent !== 'function') {
      function CustomEvent(event, params) {
        params = params || { bubbles: false, cancelable: false, detail: undefined };
        const evt = document.createEvent('CustomEvent');
        evt.initCustomEvent(event, params.bubbles, params.cancelable, params.detail);
        return evt;
      }
      CustomEvent.prototype = window.Event.prototype;
      window.CustomEvent = CustomEvent;
    }
  },

  // RequestAnimationFrame polyfill
  addRequestAnimationFramePolyfill() {
    if (!window.requestAnimationFrame) {
      window.requestAnimationFrame = function(callback) {
        return setTimeout(callback, 1000 / 60);
      };
    }
    
    if (!window.cancelAnimationFrame) {
      window.cancelAnimationFrame = function(id) {
        clearTimeout(id);
      };
    }
  },

  // Detect browser features and add classes
  detectBrowserFeatures() {
    const html = document.documentElement;
    const features = {
      'supports-grid': CSS.supports('display', 'grid'),
      'supports-flexbox': CSS.supports('display', 'flex'),
      'supports-custom-properties': CSS.supports('--custom', 'property'),
      'supports-object-fit': CSS.supports('object-fit', 'cover'),
      'supports-sticky': CSS.supports('position', 'sticky'),
      'supports-backdrop-filter': CSS.supports('backdrop-filter', 'blur(10px)'),
      'touch-device': 'ontouchstart' in window || navigator.maxTouchPoints > 0
    };

    Object.entries(features).forEach(([feature, supported]) => {
      html.classList.toggle(feature, supported);
      html.classList.toggle(`no-${feature}`, !supported);
    });

    // Browser detection
    const userAgent = navigator.userAgent.toLowerCase();
    const browsers = {
      'is-chrome': /chrome/.test(userAgent) && !/edge/.test(userAgent),
      'is-firefox': /firefox/.test(userAgent),
      'is-safari': /safari/.test(userAgent) && !/chrome/.test(userAgent),
      'is-edge': /edge/.test(userAgent) || /edg\//.test(userAgent),
      'is-ie': /trident/.test(userAgent) || /msie/.test(userAgent)
    };

    Object.entries(browsers).forEach(([browser, detected]) => {
      if (detected) html.classList.add(browser);
    });
  }
};

// ========================================
// PERFORMANCE MONITORING & OPTIMIZATION
// ========================================

const PerformanceMonitor = {
  metrics: {},
  
  init() {
    this.setupPerformanceObserver();
    this.monitorMemoryUsage();
    this.optimizeImages();
    this.setupResourceHints();
  },

  // Performance Observer for Core Web Vitals
  setupPerformanceObserver() {
    if ('PerformanceObserver' in window) {
      try {
        // Largest Contentful Paint
        const lcpObserver = new PerformanceObserver((entryList) => {
          const entries = entryList.getEntries();
          const lastEntry = entries[entries.length - 1];
          this.metrics.lcp = lastEntry.startTime;
          this.reportMetric('LCP', lastEntry.startTime);
        });
        lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });

        // First Input Delay
        const fidObserver = new PerformanceObserver((entryList) => {
          const entries = entryList.getEntries();
          entries.forEach(entry => {
            this.metrics.fid = entry.processingStart - entry.startTime;
            this.reportMetric('FID', entry.processingStart - entry.startTime);
          });
        });
        fidObserver.observe({ entryTypes: ['first-input'] });

        // Cumulative Layout Shift
        let clsValue = 0;
        const clsObserver = new PerformanceObserver((entryList) => {
          for (const entry of entryList.getEntries()) {
            if (!entry.hadRecentInput) {
              clsValue += entry.value;
            }
          }
          this.metrics.cls = clsValue;
          this.reportMetric('CLS', clsValue);
        });
        clsObserver.observe({ entryTypes: ['layout-shift'] });

      } catch (e) {
        console.warn('Performance Observer not fully supported:', e);
      }
    }
  },

  reportMetric(name, value) {
    const threshold = {
      'LCP': 2500, // ms
      'FID': 100,  // ms
      'CLS': 0.1   // score
    };

    const status = value <= threshold[name] ? 'good' : 'needs-improvement';
    console.log(`${name}: ${value.toFixed(2)} (${status})`);
    
    // Report to analytics if available
    if (typeof gtag !== 'undefined') {
      gtag('event', name, {
        event_category: 'Web Vitals',
        value: Math.round(value),
        custom_parameter_1: status
      });
    }
  },

  // Monitor memory usage
  monitorMemoryUsage() {
    if ('memory' in performance) {
      const memory = performance.memory;
      this.metrics.memory = {
        used: memory.usedJSHeapSize,
        total: memory.totalJSHeapSize,
        limit: memory.jsHeapSizeLimit
      };
      
      const usagePercent = (memory.usedJSHeapSize / memory.jsHeapSizeLimit) * 100;
      if (usagePercent > 80) {
        console.warn('High memory usage detected:', usagePercent.toFixed(2) + '%');
      }
    }
  },

  // Optimize images with lazy loading
  optimizeImages() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
      const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            img.classList.remove('lazy-loading');
            img.classList.add('lazy-loaded');
            imageObserver.unobserve(img);
          }
        });
      });

      images.forEach(img => {
        img.classList.add('lazy-loading');
        imageObserver.observe(img);
      });
    } else {
      // Fallback for older browsers
      images.forEach(img => {
        img.src = img.dataset.src;
      });
    }
  },

  // Add resource hints for better performance
  setupResourceHints() {
    const head = document.head;
    
    // Preconnect to external domains
    const preconnectDomains = ['https://fonts.googleapis.com', 'https://fonts.gstatic.com'];
    preconnectDomains.forEach(domain => {
      const link = document.createElement('link');
      link.rel = 'preconnect';
      link.href = domain;
      link.crossOrigin = 'anonymous';
      head.appendChild(link);
    });

    // DNS prefetch for external resources
    const dnsPrefetchDomains = ['https://www.google-analytics.com'];
    dnsPrefetchDomains.forEach(domain => {
      const link = document.createElement('link');
      link.rel = 'dns-prefetch';
      link.href = domain;
      head.appendChild(link);
    });
  }
};

// ========================================
// ADVANCED ACCESSIBILITY FEATURES
// ========================================

const AccessibilityEnhancer = {
  init() {
    this.setupKeyboardNavigation();
    this.setupAriaLiveRegions();
    this.setupFocusManagement();
    this.setupScreenReaderAnnouncements();
    this.setupColorContrastMode();
  },

  // Enhanced keyboard navigation
  setupKeyboardNavigation() {
    let focusableElements = [];
    let currentFocusIndex = -1;

    const updateFocusableElements = () => {
      focusableElements = Array.from(document.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      )).filter(el => {
        return !el.disabled && !el.hidden && el.offsetWidth > 0 && el.offsetHeight > 0;
      });
    };

    document.addEventListener('keydown', (e) => {
      updateFocusableElements();
      
      // Tab navigation enhancement
      if (e.key === 'Tab') {
        currentFocusIndex = focusableElements.indexOf(document.activeElement);
      }
      
      // Escape key handling
      if (e.key === 'Escape') {
        const modal = document.querySelector('.modal.show');
        const dropdown = document.querySelector('.dropdown-menu.show');
        
        if (modal) {
          modal.querySelector('.btn-close')?.click();
        } else if (dropdown) {
          dropdown.previousElementSibling?.focus();
          dropdown.classList.remove('show');
        }
      }
      
      // Arrow key navigation for custom components
      if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
        this.handleArrowKeyNavigation(e);
      }
    });

    // Skip to main content link
    const skipLink = document.createElement('a');
    skipLink.href = '#main';
    skipLink.textContent = 'Skip to main content';
    skipLink.className = 'skip-link';
    document.body.insertBefore(skipLink, document.body.firstChild);
  },

  handleArrowKeyNavigation(e) {
    const activeElement = document.activeElement;
    const isInGroup = activeElement.closest('[role="group"], [role="radiogroup"], .btn-group');
    
    if (isInGroup) {
      e.preventDefault();
      const groupElements = Array.from(isInGroup.querySelectorAll('[role="button"], button, input[type="radio"]'));
      const currentIndex = groupElements.indexOf(activeElement);
      let nextIndex;
      
      switch (e.key) {
        case 'ArrowUp':
        case 'ArrowLeft':
          nextIndex = currentIndex > 0 ? currentIndex - 1 : groupElements.length - 1;
          break;
        case 'ArrowDown':
        case 'ArrowRight':
          nextIndex = currentIndex < groupElements.length - 1 ? currentIndex + 1 : 0;
          break;
      }
      
      if (nextIndex !== undefined) {
        groupElements[nextIndex].focus();
      }
    }
  },

  // ARIA live regions for dynamic content
  setupAriaLiveRegions() {
    const liveRegion = document.createElement('div');
    liveRegion.setAttribute('aria-live', 'polite');
    liveRegion.setAttribute('aria-atomic', 'true');
    liveRegion.className = 'sr-only announcement-region';
    liveRegion.id = 'live-region';
    document.body.appendChild(liveRegion);

    const assertiveRegion = document.createElement('div');
    assertiveRegion.setAttribute('aria-live', 'assertive');
    assertiveRegion.setAttribute('aria-atomic', 'true');
    assertiveRegion.className = 'sr-only announcement-region';
    assertiveRegion.id = 'assertive-region';
    document.body.appendChild(assertiveRegion);

    // Helper function to announce messages
    window.announceToScreenReader = (message, priority = 'polite') => {
      const region = priority === 'assertive' ? assertiveRegion : liveRegion;
      region.textContent = message;
      
      // Clear after announcement
      setTimeout(() => {
        region.textContent = '';
      }, 1000);
    };
  },

  // Focus management for modals and dynamic content
  setupFocusManagement() {
    let previousFocus = null;

    // Modal focus management
    document.addEventListener('show.bs.modal', (e) => {
      previousFocus = document.activeElement;
      setTimeout(() => {
        const modal = e.target;
        const focusableElement = modal.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
        if (focusableElement) {
          focusableElement.focus();
        }
      }, 100);
    });

    document.addEventListener('hidden.bs.modal', () => {
      if (previousFocus) {
        previousFocus.focus();
        previousFocus = null;
      }
    });

    // Focus trap for modals
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        const modal = document.querySelector('.modal.show');
        if (modal) {
          const focusableElements = Array.from(modal.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
          ));
          
          const firstElement = focusableElements[0];
          const lastElement = focusableElements[focusableElements.length - 1];
          
          if (e.shiftKey && document.activeElement === firstElement) {
            e.preventDefault();
            lastElement.focus();
          } else if (!e.shiftKey && document.activeElement === lastElement) {
            e.preventDefault();
            firstElement.focus();
          }
        }
      }
    });
  },

  // Screen reader announcements for form validation
  setupScreenReaderAnnouncements() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
      form.addEventListener('submit', (e) => {
        const invalidFields = form.querySelectorAll('.is-invalid');
        if (invalidFields.length > 0) {
          const fieldNames = Array.from(invalidFields).map(field => 
            field.getAttribute('aria-label') || field.name || 'field'
          ).join(', ');
          
          announceToScreenReader(
            `Form has ${invalidFields.length} errors in: ${fieldNames}`,
            'assertive'
          );
        }
      });
    });

    // Announce successful form submissions
    document.addEventListener('formSubmissionSuccess', (e) => {
      announceToScreenReader('Form submitted successfully', 'polite');
    });
  },

  // High contrast and color preference support
  setupColorContrastMode() {
    // Detect user's color scheme preference
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    const prefersHighContrast = window.matchMedia('(prefers-contrast: high)');
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

    const updateColorScheme = () => {
      document.documentElement.classList.toggle('dark-mode', prefersDark.matches);
      document.documentElement.classList.toggle('high-contrast', prefersHighContrast.matches);
      document.documentElement.classList.toggle('reduced-motion', prefersReducedMotion.matches);
    };

    prefersDark.addEventListener('change', updateColorScheme);
    prefersHighContrast.addEventListener('change', updateColorScheme);
    prefersReducedMotion.addEventListener('change', updateColorScheme);
    
    updateColorScheme(); // Initial setup
  }
};

// ========================================
// UTILITY FUNCTIONS
// ========================================

// Throttle function for performance
function throttle(func, limit) {
  let inThrottle;
  return function() {
    const args = arguments;
    const context = this;
    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// Debounce function for search and input handling
function debounce(func, wait, immediate) {
  let timeout;
  return function() {
    const context = this;
    const args = arguments;
    const later = function() {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    const callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
}

// ========================================
// INITIALIZATION & ERROR HANDLING
// ========================================

// Enhanced initialization with error boundaries
const initializeApp = () => {
  try {
    // Initialize all modules
    BrowserSupport.init();
    PerformanceMonitor.init();
    AccessibilityEnhancer.init();
    MLApp.init();
    
    // Set up global error handling
    window.addEventListener('error', (e) => {
      console.error('Global error:', e.error);
      announceToScreenReader('An error occurred. Please try again.', 'assertive');
    });

    window.addEventListener('unhandledrejection', (e) => {
      console.error('Unhandled promise rejection:', e.reason);
      announceToScreenReader('A system error occurred. Please refresh the page.', 'assertive');
    });

    // Performance measurement
    if ('performance' in window && 'measure' in performance) {
      performance.mark('app-init-complete');
      performance.measure('app-initialization', 'navigationStart', 'app-init-complete');
    }

    console.log('🎉 ML Platform fully initialized with all enhancements');
    
  } catch (error) {
    console.error('Failed to initialize ML Platform:', error);
    
    // Fallback initialization
    try {
      MLApp.init();
      console.log('🔄 ML Platform initialized with basic features');
    } catch (fallbackError) {
      console.error('Critical initialization failure:', fallbackError);
    }
  }
};

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeApp);
} else {
  initializeApp();
}

// Export for testing and module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    MLApp,
    BrowserSupport,
    PerformanceMonitor,
    AccessibilityEnhancer,
    throttle,
    debounce
  };
}

// Final global assignment with enhanced features
window.MLPlatform = {
  MLApp,
  BrowserSupport,
  PerformanceMonitor,
  AccessibilityEnhancer,
  utils: { throttle, debounce }
};
