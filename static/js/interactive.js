// Typing effect for hero title
function typeWriter() {
    const heroTitle = document.getElementById('typing-title');
    if (heroTitle) {
        const text = heroTitle.textContent;
        heroTitle.textContent = '';
        let i = 0;
        function type() {
            if (i < text.length) {
                heroTitle.textContent += text.charAt(i);
                i++;
                setTimeout(type, 100);
            }
        }
        type();
    }
}

// Animate value function
function animateValue(obj, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Smooth scrolling for navigation links
function setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
}

// Parallax effect for hero section
function setupParallax() {
    window.addEventListener('scroll', function () {
        const parallax = document.querySelector('.hero-section');
        if (parallax) {
            let scrollPosition = window.pageYOffset;
            parallax.style.backgroundPositionY = scrollPosition * 0.5 + 'px';
        }
    });
}

// Animate elements on scroll
function setupScrollAnimation() {
    const animateOnScroll = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                observer.unobserve(entry.target);
            }
        });
    };

    const observer = new IntersectionObserver(animateOnScroll, {
        root: null,
        threshold: 0.1
    });

    document.querySelectorAll('.icon, .testimonial-card').forEach(el => {
        observer.observe(el);
    });
}

// Glow effect for buttons
function setupGlowEffect() {
    document.querySelectorAll('.glow-button').forEach(button => {
        button.addEventListener('mousemove', (e) => {
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            button.style.setProperty('--x', `${x}px`);
            button.style.setProperty('--y', `${y}px`);
        });
    });
}

// Scroll to Top FAB
function setupScrollToTop() {
    const scrollToTopButton = document.getElementById('scrollToTop');
    if (scrollToTopButton) {
        window.addEventListener('scroll', () => {
            scrollToTopButton.style.display = window.pageYOffset > 100 ? 'block' : 'none';
        });

        scrollToTopButton.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

// Dark Mode Toggle
function setupDarkMode() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const body = document.body;
    if (darkModeToggle) {
        darkModeToggle.addEventListener('change', () => {
            body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', body.classList.contains('dark-mode'));
        });

        // Check for saved dark mode preference
        if (localStorage.getItem('darkMode') === 'true') {
            body.classList.add('dark-mode');
            darkModeToggle.checked = true;
        }
    }
}

function initializeCharts() {
    if (typeof Chart === 'undefined' || typeof window.djangoData === 'undefined') return;

    // Application Status Chart
    const statusCtx = document.getElementById('statusChart');
    if (statusCtx) {
        new Chart(statusCtx.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: window.djangoData.statusLabels,
                datasets: [{
                    data: window.djangoData.statusData,
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'right' },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${context.parsed} applications`;
                            }
                        }
                    }
                },
                animation: {
                    animateScale: true,
                    animateRotate: true
                }
            }
        });
    }

    // Application Trend Chart
    const trendCtx = document.getElementById('trendChart');
    if (trendCtx) {
        new Chart(trendCtx.getContext('2d'), {
            type: 'line',
            data: {
                labels: window.djangoData.trendLabels,
                datasets: [{
                    label: 'Applications',
                    data: window.djangoData.trendData,
                    borderColor: '#36A2EB',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 1 }
                    }
                },
                plugins: {
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                    }
                },
                hover: {
                    mode: 'nearest',
                    intersect: true
                },
                animation: {
                    duration: 2000,
                    easing: 'easeOutQuart'
                }
            }
        });
    }

// Application Funnel Chart
const funnelCtx = document.getElementById('funnelChart');
if (funnelCtx) {
    new Chart(funnelCtx, {
        type: 'bar',
        data: {
            labels: ['Applied', 'Reviewed', 'Interviewed', 'Offered'],
            datasets: [{
                data: [
                    window.djangoData.funnelData.applied,
                    window.djangoData.funnelData.reviewed,
                    window.djangoData.funnelData.interviewed,
                    window.djangoData.funnelData.offered
                ],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)'
                ]
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Application Funnel'
                }
            }
        }
    });
}

    // Skills Progression Chart
    const skillsCtx = document.getElementById('skillsChart');
    if (skillsCtx) {
        new Chart(skillsCtx.getContext('2d'), {
            type: 'radar',
            data: {
                labels: window.djangoData.skillsData.labels,
                datasets: [{
                    label: 'Skill Level',
                    data: window.djangoData.skillsData.data,
                    fill: true,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgb(54, 162, 235)',
                    pointBackgroundColor: 'rgb(54, 162, 235)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(54, 162, 235)'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    r: {
                        angleLines: { display: false },
                        suggestedMin: 0,
                        suggestedMax: 100
                    }
                },
                animation: {
                    duration: 2000,
                    easing: 'easeOutQuart'
                }
            }
        });
    }
}

// Setup achievements hover effect
function setupAchievements() {
    document.querySelectorAll('.achievement').forEach(achievement => {
        achievement.addEventListener('mouseenter', () => {
            if (achievement.classList.contains('unlocked')) {
                achievement.style.transform = 'scale(1.1)';
            }
        });
        achievement.addEventListener('mouseleave', () => {
            achievement.style.transform = 'scale(1)';
        });
    });
}

// Animate progress bars on scroll
function setupProgressBars() {
    const animateProgressBars = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.width = entry.target.getAttribute('data-width');
                observer.unobserve(entry.target);
            }
        });
    };

    const progressObserver = new IntersectionObserver(animateProgressBars, {
        root: null,
        threshold: 0.1
    });

    document.querySelectorAll('.progress, .company-bar, .quest-progress').forEach(bar => {
        bar.style.width = '0';
        bar.setAttribute('data-width', bar.style.width);
        progressObserver.observe(bar);
    });
}

function displayJobLocations() {
    const locationsContainer = document.getElementById('jobLocations');
    if (locationsContainer && window.djangoData.jobLocations) {
        const locationsList = document.createElement('ul');
        window.djangoData.jobLocations.forEach(job => {
            const listItem = document.createElement('li');
            listItem.textContent = `${job.company}: ${job.location}`;
            locationsList.appendChild(listItem);
        });
        locationsContainer.appendChild(locationsList);
    }
}

function createJobSearchTimeline() {
    const timeline = document.getElementById('jobSearchTimeline');
    if (timeline && window.djangoData.timelineData) {
        window.djangoData.timelineData.forEach((event, index) => {
            const item = document.createElement('div');
            item.className = 'timeline-item';
            item.innerHTML = `
                <div class="timeline-content">
                    <h3>${event.date}</h3>
                    <p>${event.description}</p>
                </div>
            `;
            timeline.appendChild(item);
        });
    }
}

// Main initialization function
function initializeAll() {
    typeWriter();
    setupSmoothScrolling();
    setupParallax();
    setupScrollAnimation();
    setupGlowEffect();
    setupScrollToTop();
    setupDarkMode();
    initializeCharts();
    setupAchievements();
    setupProgressBars();
    initializeCharts();
    createJobSearchTimeline();
    initializeJobMap();
    generateInsights();
    displayJobLocations();
    createJobSearchTimeline();

    // Animate stat numbers
    document.querySelectorAll('.stat-number').forEach(el => {
        const value = parseInt(el.innerText);
        animateValue(el, 0, value, 1500);
    });
}

// Run initialization when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeAll);

// Initialize particles if the function exists
if (typeof particlesJS !== 'undefined') {
    particlesJS('particles-js', {
        particles: {
            number: { value: 80, density: { enable: true, value_area: 800 } },
            color: { value: '#ffffff' },
            shape: { type: 'circle' },
            opacity: { value: 0.5, random: false },
            size: { value: 3, random: true },
            line_linked: { enable: true, distance: 150, color: '#ffffff', opacity: 0.4, width: 1 },
            move: { enable: true, speed: 6, direction: 'none', random: false, straight: false, out_mode: 'out', bounce: false }
        },
        interactivity: {
            detect_on: 'canvas',
            events: { onhover: { enable: true, mode: 'repulse' }, onclick: { enable: true, mode: 'push' }, resize: true },
            modes: { grab: { distance: 400, line_linked: { opacity: 1 } }, bubble: { distance: 400, size: 40, duration: 2, opacity: 8, speed: 3 }, repulse: { distance: 200, duration: 0.4 }, push: { particles_nb: 4 }, remove: { particles_nb: 2 } }
        },
        retina_detect: true
    });
}