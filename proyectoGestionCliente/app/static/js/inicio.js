(function () {
  const STORAGE_KEY = 'theme_preference';

  function setTheme(theme) {
    // theme: 'dark' | 'light'
    const body = document.body;
    body.classList.remove('theme-dark', 'theme-light');
    body.classList.add(theme === 'dark' ? 'theme-dark' : 'theme-light');
    body.dataset.theme = theme;

    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch (e) {
      // ignore
    }
  }

  function getPreferredTheme() {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved === 'dark' || saved === 'light') return saved;
    } catch (e) {
      // ignore
    }

    // default: match OS
    return (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)
      ? 'dark'
      : 'light';
  }

  document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('theme-toggle');
    if (toggle) {
      toggle.addEventListener('click', (e) => {
        e.preventDefault();
        const current = document.body.dataset.theme || 'light';
        setTheme(current === 'dark' ? 'light' : 'dark');
      });
    }

    setTheme(getPreferredTheme());
  });
})();

