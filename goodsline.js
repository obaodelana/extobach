// --- Add common interaction classes
document.querySelectorAll('.card, .sidebar-item, .tab-button, .comment-bubble, .price-button, .video-link').forEach(item => {
    item.classList.add('no-select');
});

// --- Mobile menu toggle logic
const menuToggle = document.getElementById('menu-toggle');
const sidebar = document.getElementById('sidebar');

menuToggle.addEventListener('click', function() {
    menuToggle.classList.toggle('active');
    sidebar.classList.toggle('active');
});

// Close sidebar when clicking a menu item on mobile
document.querySelectorAll('.sidebar-item').forEach(item => {
    item.addEventListener('click', function() {
        if (window.innerWidth <= 768 && !document.body.classList.contains('layout-fullscreen')) { // Check not fullscreen
            menuToggle.classList.remove('active');
            sidebar.classList.remove('active');
        }
    });
});

// Close sidebar when clicking outside of it
document.addEventListener('click', function(event) {
    if (window.innerWidth <= 768 && 
        !document.body.classList.contains('layout-fullscreen') && // Check not fullscreen
        !sidebar.contains(event.target) && 
        !menuToggle.contains(event.target) && 
        sidebar.classList.contains('active')) {
        menuToggle.classList.remove('active');
        sidebar.classList.remove('active');
    }
});

// --- Intro Animation Logic ---
const introOverlay = document.getElementById('intro-overlay');
const typingTextElement = document.getElementById('typing-text');
const dashboardWrapper = document.querySelector('.dashboard-wrapper');
const bodyElement = document.body;

const textToType = "Analyzing Sentiments. Aggregating Relevancy.";
let charIndex = 0;
const typingSpeed = 50; // Milliseconds per character
const holdDuration = 200; // Milliseconds to hold text after typing

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function() {
        const context = this;
        const args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            func.apply(context, args);
        }, wait);
    };
}

function typeWriter() {
    if (charIndex < textToType.length) {
        typingTextElement.textContent += textToType.charAt(charIndex);
        charIndex++;
        setTimeout(typeWriter, typingSpeed);
    } else {
        typingTextElement.style.borderRight = 'none'; 
        typingTextElement.style.animation = 'none';
        setTimeout(() => {
            introOverlay.classList.add('hidden');
            introOverlay.addEventListener('transitionend', function handleTransitionEnd() {
                introOverlay.style.display = 'none'; 
                dashboardWrapper.style.display = 'flex'; 
                if (!bodyElement.classList.contains('layout-fullscreen')) { // Only allow body scroll if not in fullscreen
                   bodyElement.style.overflowY = 'auto'; 
                }
                bodyElement.style.overflowX = 'hidden'; 
                introOverlay.removeEventListener('transitionend', handleTransitionEnd); 
            }, { once: true }); 
        }, holdDuration);
    }
}

// --- Layout Snapping Logic ---
const FULLSCREEN_THRESHOLD_WIDTH = 1900;
const FULLSCREEN_THRESHOLD_HEIGHT = 900;

function applyLayoutState() {
    const currentWidth = window.innerWidth;
    const currentHeight = window.innerHeight;

    if (currentWidth >= FULLSCREEN_THRESHOLD_WIDTH && currentHeight >= FULLSCREEN_THRESHOLD_HEIGHT) {
        if (!bodyElement.classList.contains('layout-fullscreen')) {
            bodyElement.classList.add('layout-fullscreen');
            bodyElement.style.overflowY = 'hidden'; // Enforce no body scroll in fullscreen
            // If mobile menu was open, close it as it's not used in fullscreen
            if (sidebar.classList.contains('active')) {
                menuToggle.classList.remove('active');
                sidebar.classList.remove('active');
            }
        }
    } else {
        if (bodyElement.classList.contains('layout-fullscreen')) {
            bodyElement.classList.remove('layout-fullscreen');
            if (dashboardWrapper.style.display === 'flex') { // Only if dashboard is visible
                bodyElement.style.overflowY = 'auto'; // Restore body scroll for default layout
            }
        }
    }
}

window.addEventListener('load', () => {
    dashboardWrapper.style.display = 'none';
    applyLayoutState(); // Apply initial layout state based on window size
    setTimeout(typeWriter, 300); 
});

window.addEventListener('resize', debounce(() => {
    applyLayoutState();
    // Existing resize handlers will also be called by their own listeners
    // resizeCanvas(); // Already has its own debounced listener
    // checkSVGTextOverlap(); // Already has its own debounced listener
    // updateRelevancyGraphXAxis(); // Already has its own debounced listener
}, 100)); // Debounce for layout snapping

// --- Tab switching logic ---
const sentimentTab = document.getElementById('sentiment-tab');
const relevancyTab = document.getElementById('relevancy-tab');
const sentimentGraph = document.getElementById('sentiment-graph');
const relevancyGraph = document.getElementById('relevancy-graph');

sentimentTab.addEventListener('click', function() {
    sentimentTab.classList.add('active-tab');
    relevancyTab.classList.remove('active-tab');
    sentimentGraph.classList.remove('hidden');
    relevancyGraph.classList.add('hidden');
});

relevancyTab.addEventListener('click', function() {
    relevancyTab.classList.add('active-tab');
    sentimentTab.classList.remove('active-tab');
    relevancyGraph.classList.remove('hidden');
    sentimentGraph.classList.add('hidden');
});

// --- Ambient Particle Background ---
const canvas = document.getElementById('ambient-canvas');
const ctx = canvas.getContext('2d');
let particlesArray;
let animationFrameId;

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    if (particlesArray && particlesArray.length > 0) { 
        initParticles(); // Re-initialize to adjust particle density if needed
    }
}
// Call resizeCanvas initially and on window resize (debounced)
resizeCanvas(); 
window.addEventListener('resize', debounce(resizeCanvas, 250));

class Particle {
    constructor(x, y, size, speedX, speedY, color) {
        this.x = x;
        this.y = y;
        this.size = size;
        this.speedX = speedX;
        this.speedY = speedY;
        this.color = color;
    }
    draw() {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
    update() {
        if (this.x + this.size > canvas.width || this.x - this.size < 0) {
            this.speedX = -this.speedX;
        }
        if (this.y + this.size > canvas.height || this.y - this.size < 0) {
            this.speedY = -this.speedY;
        }
        this.x += this.speedX;
        this.y += this.speedY;
        this.draw();
    }
}

function initParticles() {
    particlesArray = [];
    let maxParticles = 120, minParticles = 30;
    if (window.innerWidth <= 768) { maxParticles = 60; minParticles = 20; }
    if (window.innerWidth <= 480) { maxParticles = 40; minParticles = 15; }
    const isLowPowerDevice = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) && window.devicePixelRatio > 2;
    if (isLowPowerDevice) { maxParticles = Math.floor(maxParticles / 2); minParticles = Math.floor(minParticles / 2); }
    
    let numberOfParticles = Math.min(maxParticles, Math.max(minParticles, Math.floor((canvas.width * canvas.height) / 15000)));
    const colorLight = getComputedStyle(document.documentElement).getPropertyValue('--particle-color-light').trim();
    const colorDark = getComputedStyle(document.documentElement).getPropertyValue('--particle-color-dark').trim();

    for (let i = 0; i < numberOfParticles; i++) {
        let size = (Math.random() * 1) + 0.3; 
        let x = (Math.random() * ((innerWidth - size * 2) - (size * 2)) + size * 2);
        let y = (Math.random() * ((innerHeight - size * 2) - (size * 2)) + size * 2);
        let speedMultiplier = isLowPowerDevice ? 0.05 : 0.1;
        let speedX = (Math.random() * speedMultiplier) - (speedMultiplier/2); 
        let speedY = (Math.random() * speedMultiplier) - (speedMultiplier/2); 
        let color = Math.random() > 0.5 ? colorLight : colorDark;
        particlesArray.push(new Particle(x, y, size, speedX, speedY, color));
    }
}

if (canvas) { initParticles(); }

function animateParticles() {
    if (!ctx || !particlesArray) return; 
    if (animationFrameId) cancelAnimationFrame(animationFrameId);
    
    ctx.clearRect(0, 0, innerWidth, innerHeight);
    for (let i = 0; i < particlesArray.length; i++) particlesArray[i].update();
    if (!/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || window.innerWidth > 768) connectParticles();
    animationFrameId = requestAnimationFrame(animateParticles);
}

if (canvas && ctx) {
    animateParticles();
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            if (animationFrameId) { cancelAnimationFrame(animationFrameId); animationFrameId = null; }
        } else {
            if (!animationFrameId) animateParticles();
        }
    });
}

function connectParticles() {
    if (!particlesArray) return; 
    const lineColorBase = getComputedStyle(document.documentElement).getPropertyValue('--particle-line-color').trim();
    const connectionDistance = Math.min(canvas.width, canvas.height) / 8;
    const step = window.innerWidth <= 768 ? 2 : 1;
    
    for (let a = 0; a < particlesArray.length; a += step) {
        for (let b = a; b < particlesArray.length; b += step) {
            let distance = ((particlesArray[a].x - particlesArray[b].x) * (particlesArray[a].x - particlesArray[b].x))
                         + ((particlesArray[a].y - particlesArray[b].y) * (particlesArray[a].y - particlesArray[b].y));
            if (distance < connectionDistance * connectionDistance) { 
                let opacityValue = 1 - (distance/(connectionDistance * connectionDistance * 0.5));
                opacityValue = Math.min(0.2, Math.max(0, opacityValue)); 
                let rgbColorMatch = lineColorBase.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)/);
                if (rgbColorMatch) ctx.strokeStyle = `rgba(${rgbColorMatch[1]}, ${rgbColorMatch[2]}, ${rgbColorMatch[3]}, ${opacityValue})`;
                else ctx.strokeStyle = lineColorBase; 
                ctx.lineWidth = 0.3; 
                ctx.beginPath();
                ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
                ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
                ctx.stroke();
            }
        }
    }
}

// --- Card Hover Effect (Mobile-friendly) ---
const cards = document.querySelectorAll('.card');
const maxRotate = 4; 
const scaleFactor = 1.015; 
const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

if (!isTouchDevice) {
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const cardRect = card.getBoundingClientRect();
            const cardCenterX = cardRect.left + cardRect.width / 2;
            const cardCenterY = cardRect.top + cardRect.height / 2;
            const offsetX = (e.clientX - cardCenterX) / (cardRect.width / 2); 
            const offsetY = (e.clientY - cardCenterY) / (cardRect.height / 2); 
            card.style.transform = `perspective(1200px) rotateX(${-offsetY * maxRotate}deg) rotateY(${offsetX * maxRotate}deg) scale(${scaleFactor})`;
            card.classList.add('card-interactive');
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1200px) rotateX(0deg) rotateY(0deg) scale(1)';
            card.classList.remove('card-interactive');
        });
    });
} else {
    cards.forEach(card => {
        card.addEventListener('touchstart', () => { card.style.transform = `scale(${scaleFactor})`; card.classList.add('card-interactive'); }, { passive: true });
        card.addEventListener('touchend', () => { card.style.transform = 'scale(1)'; card.classList.remove('card-interactive'); }, { passive: true });
    });
}

// --- Update Relevancy Graph X-axis Labels ---
function updateRelevancyGraphXAxis() {
    const relevancyXLabels = document.querySelectorAll('#relevancy-graph .relevancy-x-label'); // More specific selector
    const today = new Date();
    const days = [];
    const useShortFormat = window.innerWidth <= 480 && !document.body.classList.contains('layout-fullscreen'); // Check not fullscreen

    for (let i = 6; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(today.getDate() - i);
        const options = useShortFormat ? { month: 'numeric', day: 'numeric' } : { month: 'short', day: 'numeric' };
        days.push(date.toLocaleDateString('en-US', options));
    }
    relevancyXLabels.forEach((label, index) => { if (days[index]) label.textContent = days[index]; });
}
updateRelevancyGraphXAxis();
relevancyTab.addEventListener('click', updateRelevancyGraphXAxis);
window.addEventListener('resize', debounce(updateRelevancyGraphXAxis, 250));

// --- Check SVG text overlap and adjust if needed
function checkSVGTextOverlap() {
    const isSmallScreenNoFullscreen = window.innerWidth <= 480 && !document.body.classList.contains('layout-fullscreen');

    document.querySelectorAll('#relevancy-graph .relevancy-x-label').forEach((label, index) => { // More specific selector
        label.style.display = (isSmallScreenNoFullscreen && index % 2 !== 0) ? 'none' : '';
    });
    
    const sentimentXLabels = sentimentGraph.querySelectorAll('text[text-anchor="middle"]');
    sentimentXLabels.forEach((label, index) => {
         // Only apply this to the year labels, not the Y-axis percentage labels
        if (parseFloat(label.getAttribute('y')) > 370) { // Check if it's an X-axis label by its y-coordinate
            label.style.display = (isSmallScreenNoFullscreen && index % 2 !== 0) ? 'none' : '';
        }
    });
}
checkSVGTextOverlap();
window.addEventListener('resize', debounce(checkSVGTextOverlap, 250));