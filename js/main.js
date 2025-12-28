document.addEventListener('DOMContentLoaded', () => {

    // --- Theme Toggler ---
    const themeToggle = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement;

    // Function to set theme
    const setTheme = (theme) => {
        htmlElement.classList.remove('light', 'dark');
        htmlElement.classList.add(theme);
        localStorage.setItem('theme', theme);
    };

    // Load saved theme from localStorage or default to light
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);

    themeToggle.addEventListener('click', () => {
        const currentTheme = htmlElement.classList.contains('dark') ? 'dark' : 'light';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
    });

    // --- Single-Page Application (SPA) Navigation ---
    const navItems = document.querySelectorAll('.nav-item');
    const contentSections = document.querySelectorAll('.content-section');

    // Function to handle navigation
    const navigateTo = (targetId) => {
        // Update active state on nav items
        navItems.forEach(item => {
            item.classList.toggle('active', item.dataset.target === targetId);
        });

        // Show/hide content sections
        contentSections.forEach(section => {
            section.classList.toggle('active', section.id === targetId);
        });

        // Scroll to top of content area
        document.querySelector('.main-content').scrollTop = 0;
    };

    // Add click event listeners to nav items
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const targetId = item.dataset.target;
            navigateTo(targetId);
        });
    });

    // Activate the first section by default
    navigateTo('home');

    // --- Feather Icons Replacement ---
    // This is called again in case of dynamic content later
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
});
