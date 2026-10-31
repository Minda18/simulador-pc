/* Control del tema claro/oscuro del simulador. */

(() => {
  const STORAGE_KEY = "simulador-pc-theme";
  const root = document.documentElement;
  const toggle = document.querySelector("[data-theme-toggle]");
  const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");

  const readPreference = () => {
    try {
      const value = window.localStorage.getItem(STORAGE_KEY);
      return value === "dark" || value === "light" ? value : null;
    } catch (error) {
      return null;
    }
  };

  const savePreference = (theme) => {
    try {
      window.localStorage.setItem(STORAGE_KEY, theme);
    } catch (error) {
      /* El navegador puede bloquear localStorage; se ignora. */
    }
  };

  const systemTheme = () => (mediaQuery.matches ? "dark" : "light");

  const currentTheme = () => (root.getAttribute("data-theme") === "dark" ? "dark" : "light");

  const updateToggle = (theme) => {
    if (!toggle) {
      return;
    }
    const isDark = theme === "dark";
    const label = isDark ? "Activar tema claro" : "Activar tema oscuro";
    toggle.setAttribute("aria-pressed", String(isDark));
    toggle.setAttribute("aria-label", label);
    toggle.setAttribute("title", label);
  };

  const applyTheme = (theme, persist = false) => {
    root.setAttribute("data-theme", theme);
    updateToggle(theme);
    if (persist) {
      savePreference(theme);
    }
  };

  const initialTheme = readPreference() || systemTheme();
  if (!root.getAttribute("data-theme")) {
    root.setAttribute("data-theme", initialTheme);
  }
  applyTheme(root.getAttribute("data-theme") || initialTheme);

  if (toggle) {
    toggle.addEventListener("click", () => {
      applyTheme(currentTheme() === "dark" ? "light" : "dark", true);
    });
  }

  const handleSystemChange = () => {
    if (!readPreference()) {
      applyTheme(systemTheme());
    }
  };

  if (typeof mediaQuery.addEventListener === "function") {
    mediaQuery.addEventListener("change", handleSystemChange);
  } else {
    mediaQuery.addListener(handleSystemChange);
  }
})();
