import React from "react";

const THEMES = [
  { key: "light", label: "Светлая" },
  { key: "dark", label: "Тёмная" },
  { key: "blue", label: "Синяя" },
  { key: "purple", label: "Фиолетовая" },
];

function ThemeSwitcher({ theme, setTheme }) {
  return (
    <div className="tg-theme-switcher" title="Тема сохранится для следующего визита">
      {THEMES.map((t) => (
        <button
          key={t.key}
          className={`tg-theme-btn${theme === t.key ? " active" : ""}`}
          onClick={() => setTheme(t.key)}
        >
          {t.label}
        </button>
      ))}
    </div>
  );
}

export default ThemeSwitcher;
