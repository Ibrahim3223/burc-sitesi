/**
 * Theme Toggle System
 * Supports dark/light mode with localStorage persistence
 */

(function() {
    'use strict';

    const THEME_KEY = 'burc-theme';
    const DARK_THEME = 'dark';
    const LIGHT_THEME = 'light';

    // Get saved theme or default to dark
    function getSavedTheme() {
        const saved = localStorage.getItem(THEME_KEY);
        if (saved === LIGHT_THEME || saved === DARK_THEME) {
            return saved;
        }
        // Check system preference
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
            return LIGHT_THEME;
        }
        return DARK_THEME; // Default to dark theme
    }

    // Apply theme to document
    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem(THEME_KEY, theme);
        
        // Update toggle button if it exists
        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            const icon = toggleBtn.querySelector('.theme-icon');
            const text = toggleBtn.querySelector('.theme-text');
            
            if (theme === LIGHT_THEME) {
                if (icon) icon.textContent = '🌙';
                if (text) text.textContent = 'Karanlık Mod';
                toggleBtn.setAttribute('aria-label', 'Karanlık moda geç');
            } else {
                if (icon) icon.textContent = '☀️';
                if (text) text.textContent = 'Aydınlık Mod';
                toggleBtn.setAttribute('aria-label', 'Aydınlık moda geç');
            }
        }
    }

    // Toggle between themes
    function toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme') || DARK_THEME;
        const newTheme = currentTheme === DARK_THEME ? LIGHT_THEME : DARK_THEME;
        applyTheme(newTheme);
        
        // Add ripple effect to toggle button
        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            toggleBtn.classList.add('theme-toggle-active');
            setTimeout(() => {
                toggleBtn.classList.remove('theme-toggle-active');
            }, 600);
        }
    }

    // Initialize theme on page load
    function initTheme() {
        const savedTheme = getSavedTheme();
        applyTheme(savedTheme);
    }

    // Initialize immediately (before DOM loads) to prevent flash
    initTheme();

    // Set up toggle button after DOM loads
    document.addEventListener('DOMContentLoaded', function() {
        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', toggleTheme);
            
            // Keyboard support
            toggleBtn.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    toggleTheme();
                }
            });
        }

        // Listen for system theme changes
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', function(e) {
                // Only auto-switch if user hasn't manually set a preference
                const hasManualPreference = localStorage.getItem(THEME_KEY);
                if (!hasManualPreference) {
                    applyTheme(e.matches ? LIGHT_THEME : DARK_THEME);
                }
            });
        }
    });

    // Export for external use
    window.ThemeToggle = {
        toggle: toggleTheme,
        setTheme: applyTheme,
        getTheme: () => document.documentElement.getAttribute('data-theme') || DARK_THEME
    };
})();
