// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initNavigation();
    initTypingAnimation();
    initScrollAnimations();
    initDemoInterface();
    initSmoothScrolling();
    initParallaxEffects();
});

// Navigation Functionality
function initNavigation() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    // Toggle mobile menu
    hamburger.addEventListener('click', function() {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });

    // Close mobile menu when clicking on links
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
        if (!hamburger.contains(e.target) && !navMenu.contains(e.target)) {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        }
    });

    // Navbar scroll effect
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(12, 12, 12, 0.98)';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.3)';
        } else {
            navbar.style.background = 'rgba(12, 12, 12, 0.95)';
            navbar.style.boxShadow = 'none';
        }
    });
}

// Typing Animation
function initTypingAnimation() {
    const typingElements = document.querySelectorAll('.typing-text');
    
    typingElements.forEach(element => {
        const text = element.getAttribute('data-text');
        element.textContent = '';
        
        let i = 0;
        const typeSpeed = 100;
        
        function typeWriter() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, typeSpeed);
            } else {
                // Start blinking cursor animation
                element.style.borderRight = '3px solid #ffd700';
                element.style.animation = 'blink-caret 0.75s step-end infinite';
            }
        }
        
        // Start typing animation after a delay
        setTimeout(typeWriter, 500);
    });
}

// Scroll Animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                
                // Add stagger animation for cards
                if (entry.target.classList.contains('about-card')) {
                    const cards = document.querySelectorAll('.about-card');
                    cards.forEach((card, index) => {
                        setTimeout(() => {
                            card.style.animationDelay = `${index * 0.2}s`;
                            card.classList.add('animate-in');
                        }, index * 100);
                    });
                }
            }
        });
    }, observerOptions);

    // Observe elements for scroll animations
    const animateElements = document.querySelectorAll('.about-card, .demo-container, .section-header');
    animateElements.forEach(el => {
        el.classList.add('scroll-reveal');
        observer.observe(el);
    });

    // Parallax scroll effect for hero section
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.floating-icon');
        
        parallaxElements.forEach(element => {
            const speed = 0.5;
            element.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });
}

// Demo Interface
function initDemoInterface() {
    const microphoneBtn = document.getElementById('microphoneBtn');
    const micStatus = document.getElementById('micStatus');
    const recognizedText = document.getElementById('recognizedText');
    const animationArea = document.getElementById('animationArea');
    const tryDemoBtn = document.getElementById('tryDemoBtn');
    const learnMoreBtn = document.getElementById('learnMoreBtn');

    let isListening = false;
    let recognition;

    // Available phrases and their corresponding GIF files
    const signLanguageDict = {
        'hello': 'hello.gif',
        'thank you': 'Thank you.gif',
        'i like you': 'I like you.gif',
        'happy': 'happy.gif',
        'nice to meet you': 'nice_to_meet_you.gif',
        'no': 'no.gif'
    };

    // Check if browser supports Speech Recognition
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = function() {
            isListening = true;
            microphoneBtn.classList.add('active');
            micStatus.textContent = 'Listening... Speak now!';
            micStatus.style.color = '#50c878';
        };

        recognition.onresult = function(event) {
            const spokenText = event.results[0][0].transcript.toLowerCase().trim();
            recognizedText.textContent = spokenText;
            
            // Check if spoken text matches any supported phrase
            if (signLanguageDict[spokenText]) {
                showSignLanguageAnimation(spokenText, signLanguageDict[spokenText]);
            } else {
                // Find partial matches
                const partialMatch = findPartialMatch(spokenText);
                if (partialMatch) {
                    showSignLanguageAnimation(partialMatch, signLanguageDict[partialMatch]);
                } else {
                    showNoMatchMessage(spokenText);
                }
            }
        };

        recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
            micStatus.textContent = 'Error occurred. Try again.';
            micStatus.style.color = '#ff6b6b';
            resetMicrophoneState();
        };

        recognition.onend = function() {
            resetMicrophoneState();
        };
    } else {
        // Fallback for browsers without speech recognition
        microphoneBtn.addEventListener('click', function() {
            showDemoFallback();
        });
    }

    // Microphone button click handler
    microphoneBtn.addEventListener('click', function() {
        if (recognition) {
            if (!isListening) {
                try {
                    recognition.start();
                } catch (error) {
                    console.error('Error starting recognition:', error);
                    showDemoFallback();
                }
            } else {
                recognition.stop();
            }
        } else {
            showDemoFallback();
        }
    });

    // Try Demo button - scroll to demo section
    tryDemoBtn.addEventListener('click', function() {
        document.getElementById('demo').scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    });

    // Learn More button - scroll to about section
    learnMoreBtn.addEventListener('click', function() {
        document.getElementById('about').scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    });

    function resetMicrophoneState() {
        isListening = false;
        microphoneBtn.classList.remove('active');
        micStatus.textContent = 'Click to start listening';
        micStatus.style.color = '#b8b8b8';
    }

    function findPartialMatch(spokenText) {
        const phrases = Object.keys(signLanguageDict);
        for (let phrase of phrases) {
            if (spokenText.includes(phrase) || phrase.includes(spokenText)) {
                return phrase;
            }
        }
        return null;
    }

    function showSignLanguageAnimation(phrase, gifFile) {
        animationArea.innerHTML = `
            <div class="animation-success">
                <h5>✅ Recognized: "${phrase}"</h5>
                <div class="gif-container">
                    <img src="${gifFile}" alt="${phrase} sign language" class="sign-gif" 
                         onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
                    <div class="gif-error" style="display:none; color: #ff6b6b; padding: 1rem;">
                        <i class="fas fa-exclamation-triangle"></i>
                        <p>GIF file not found: ${gifFile}</p>
                        <small>Please check if the file exists in the project directory</small>
                    </div>
                </div>
                <p>Sign language animation for "${phrase}"</p>
            </div>
        `;
        
        // Add loading indicator and error handling for the image
        const img = animationArea.querySelector('.sign-gif');
        img.onload = function() {
            console.log(`Successfully loaded GIF: ${gifFile}`);
        };
        
        // Add success animation
        animationArea.style.background = 'rgba(80, 200, 120, 0.1)';
        animationArea.style.borderColor = 'rgba(80, 200, 120, 0.5)';
        
        setTimeout(() => {
            animationArea.style.background = 'rgba(255, 255, 255, 0.03)';
            animationArea.style.borderColor = 'rgba(255, 215, 0, 0.3)';
        }, 3000);
    }

    function showNoMatchMessage(spokenText) {
        animationArea.innerHTML = `
            <div class="animation-error">
                <h5>❌ Not recognized</h5>
                <p>Sorry, "${spokenText}" is not in our database.</p>
                <p>Try one of these phrases:</p>
                <div class="suggestion-tags">
                    ${Object.keys(signLanguageDict).map(phrase => 
                        `<span class="suggestion-tag">${phrase}</span>`
                    ).join('')}
                </div>
            </div>
        `;
        
        animationArea.style.background = 'rgba(255, 107, 107, 0.1)';
        animationArea.style.borderColor = 'rgba(255, 107, 107, 0.5)';
        
        setTimeout(() => {
            animationArea.style.background = 'rgba(255, 255, 255, 0.03)';
            animationArea.style.borderColor = 'rgba(255, 215, 0, 0.3)';
        }, 5000);
    }

    function showDemoFallback() {
        recognizedText.textContent = 'hello';
        showSignLanguageAnimation('hello', 'hello.gif');
        micStatus.textContent = 'Demo mode - showing "hello"';
        micStatus.style.color = '#ffd700';
    }

    // Add phrase tag click functionality
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('phrase-tag')) {
            const phrase = e.target.textContent.toLowerCase();
            if (signLanguageDict[phrase]) {
                recognizedText.textContent = phrase;
                showSignLanguageAnimation(phrase, signLanguageDict[phrase]);
            }
        }
    });
}

// Smooth Scrolling for Navigation Links
function initSmoothScrolling() {
    const navLinks = document.querySelectorAll('.nav-link[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Scroll indicator
    const scrollIndicator = document.querySelector('.scroll-indicator');
    if (scrollIndicator) {
        scrollIndicator.addEventListener('click', function() {
            document.getElementById('about').scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        });
    }
}

// Parallax Effects
function initParallaxEffects() {
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset;
        
        // Hero parallax
        const heroVisual = document.querySelector('.hero-visual');
        if (heroVisual) {
            heroVisual.style.transform = `translateY(${scrollTop * 0.3}px)`;
        }
        
        // Floating icons parallax
        const micIcon = document.querySelector('.microphone-icon');
        const handIcon = document.querySelector('.hand-icon');
        
        if (micIcon && handIcon) {
            micIcon.style.transform = `translateY(${scrollTop * 0.2}px)`;
            handIcon.style.transform = `translateY(${scrollTop * -0.2}px)`;
        }
    });
}

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add loading animation for images
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('load', function() {
            this.style.opacity = '1';
            this.style.transform = 'scale(1)';
        });
    });
});

// Add hover effects for interactive elements
document.addEventListener('DOMContentLoaded', function() {
    // Button hover sound effect (visual feedback)
    const buttons = document.querySelectorAll('.btn, .microphone-btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px) scale(1.02)';
        });
        
        button.addEventListener('mouseleave', function() {
            if (!this.classList.contains('active')) {
                this.style.transform = 'translateY(0) scale(1)';
            }
        });
    });
    
    // Card hover effects
    const cards = document.querySelectorAll('.about-card, .info-card, .demo-note');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
});

// Performance optimization - throttled scroll
const throttledScroll = debounce(function() {
    // Any scroll-intensive operations can go here
}, 16); // ~60fps

window.addEventListener('scroll', throttledScroll);

// Add CSS for dynamic styles
const style = document.createElement('style');
style.textContent = `
    .animation-success, .animation-error {
        text-align: center;
        padding: 1rem;
    }
    
    .animation-success h5 {
        color: #50c878;
        margin-bottom: 1rem;
        font-size: 1.1rem;
    }
    
    .animation-error h5 {
        color: #ff6b6b;
        margin-bottom: 1rem;
        font-size: 1.1rem;
    }
    
    .gif-container {
        margin: 1rem 0;
        border-radius: 10px;
        overflow: hidden;
        background: rgba(255, 215, 0, 0.1);
        padding: 1rem;
    }
    
    .sign-gif {
        max-width: 100%;
        height: auto;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .suggestion-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        justify-content: center;
        margin-top: 1rem;
    }
    
    .suggestion-tag {
        background: rgba(255, 215, 0, 0.2);
        color: #ffd700;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .suggestion-tag:hover {
        background: rgba(255, 215, 0, 0.4);
        transform: scale(1.05);
    }
    
    .phrase-tag {
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .phrase-tag:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3);
    }
    
    @keyframes fadeInScale {
        from {
            opacity: 0;
            transform: scale(0.8);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .sign-gif {
        animation: fadeInScale 0.5s ease-out;
    }
`;

document.head.appendChild(style);
