/**
 * Sistema de Dark Mode
 * Salva preferência do usuário em localStorage
 */

class ThemeManager {
    constructor() {
        this.STORAGE_KEY = 'neuroai_theme';
        this.DARK_CLASS = 'dark-mode';
        this.init();
    }

    init() {
        // Carrega tema salvo ou usa preferência do sistema
        const savedTheme = localStorage.getItem(this.STORAGE_KEY);
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        const isDark = savedTheme ? savedTheme === 'dark' : prefersDark;
        
        if (isDark) {
            this.enableDarkMode();
        } else {
            this.disableDarkMode();
        }
    }

    enableDarkMode() {
        document.documentElement.classList.add(this.DARK_CLASS);
        localStorage.setItem(this.STORAGE_KEY, 'dark');
        this.updateToggleIcon();
    }

    disableDarkMode() {
        document.documentElement.classList.remove(this.DARK_CLASS);
        localStorage.setItem(this.STORAGE_KEY, 'light');
        this.updateToggleIcon();
    }

    toggle() {
        if (document.documentElement.classList.contains(this.DARK_CLASS)) {
            this.disableDarkMode();
        } else {
            this.enableDarkMode();
        }
    }

    isDark() {
        return document.documentElement.classList.contains(this.DARK_CLASS);
    }

    updateToggleIcon() {
        const toggle = document.getElementById('themeToggle');
        if (toggle) {
            toggle.textContent = this.isDark() ? '☀️' : '🌙';
            toggle.title = this.isDark() ? 'Ativar modo claro' : 'Ativar modo escuro';
        }
    }
}

// Inicializa ao carregar
const themeManager = new ThemeManager();

// Se precisar acessar globalmente
window.toggleTheme = () => themeManager.toggle();
