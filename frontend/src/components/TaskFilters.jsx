import React, { useState, useEffect } from "react";
import { FaSearch, FaTimes } from "react-icons/fa";
import "./TaskFilters.css";

function TaskFilters({ onFilterChange, initialFilters = {} }) {
  const [filters, setFilters] = useState({
    search: initialFilters.search || "",
    status: initialFilters.status || "all",
    priority: initialFilters.priority || "all",
    category: initialFilters.category || "",
  });

  // Дебаунс для поиска (не отправляем запрос при каждом символе)
  useEffect(() => {
    const timer = setTimeout(() => {
      onFilterChange(filters);
    }, 300);

    return () => clearTimeout(timer);
  }, [filters]);

  const handleSearchChange = (e) => {
    setFilters((prev) => ({ ...prev, search: e.target.value }));
  };

  const handleStatusChange = (e) => {
    setFilters((prev) => ({ ...prev, status: e.target.value }));
  };

  const handlePriorityChange = (e) => {
    setFilters((prev) => ({ ...prev, priority: e.target.value }));
  };

  const handleCategoryChange = (e) => {
    setFilters((prev) => ({ ...prev, category: e.target.value }));
  };

  const clearFilters = () => {
    const clearedFilters = { search: "", status: "all", priority: "all", category: "" };
    setFilters(clearedFilters);
    onFilterChange(clearedFilters);
  };

  const hasActiveFilters =
    filters.search || filters.status !== "all" || filters.priority !== "all" || filters.category;

  return (
    <div className="task-filters">
      {/* Поиск */}
      <div style={{ flex: "1", minWidth: "200px", position: "relative" }}>
        <FaSearch
          style={{
            position: "absolute",
            left: "12px",
            top: "50%",
            transform: "translateY(-50%)",
            color: "var(--tg-gray)",
            fontSize: "0.9rem",
          }}
        />
        <input
          type="text"
          className="filter-input"
          placeholder="Поиск задач..."
          value={filters.search}
          onChange={handleSearchChange}
          style={{ paddingLeft: "38px" }}
        />
      </div>

      {/* Статус */}
      <select
        className="filter-select"
        value={filters.status}
        onChange={handleStatusChange}
      >
        <option value="all">Все задачи</option>
        <option value="false">Активные</option>
        <option value="true">Завершённые</option>
      </select>

      {/* Приоритет */}
      <select
        className="filter-select"
        value={filters.priority}
        onChange={handlePriorityChange}
      >
        <option value="all">Любой приоритет</option>
        <option value="low">💎 Низкий</option>
        <option value="normal">⚡ Средний</option>
        <option value="high">🔥 Высокий</option>
      </select>

      {/* Категория */}
      <input
        type="text"
        className="filter-input"
        placeholder="📁 Категория..."
        value={filters.category}
        onChange={handleCategoryChange}
        list="filter-categories-list"
      />
      <datalist id="filter-categories-list">
        <option value="Работа" />
        <option value="Личное" />
        <option value="Учеба" />
        <option value="Дом" />
        <option value="Здоровье" />
      </datalist>

      {/* Очистить фильтры */}
      {hasActiveFilters && (
        <button className="clear-filters-btn" onClick={clearFilters}>
          <FaTimes style={{ marginRight: "6px" }} />
          Очистить
        </button>
      )}
    </div>
  );
}

export default TaskFilters;
