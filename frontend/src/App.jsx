import React, { useState, useEffect, useCallback, useMemo } from "react";
import { FaCalendarDay, FaListUl, FaCog, FaPlus } from "react-icons/fa";
import TaskList from "./components/TaskList";
import CalendarView from "./components/CalendarView";
import ThemeSwitcher from "./components/ThemeSwitcher";
import AddTaskModal from "./components/AddTaskModal";
import EditTaskModal from "./components/EditTaskModal";
import TaskFilters from "./components/TaskFilters";
import TaskStats from "./components/TaskStats";
import TaskSorter from "./components/TaskSorter";
import useTelegramWebApp from "./hooks/useTelegramWebApp";
import "./App.css";

const API_BASE = process.env.REACT_APP_API_URL || "/api";

const MODES = [
  { key: "calendar", label: "Календарь", icon: <FaCalendarDay /> },
  { key: "tasks", label: "Задачи", icon: <FaListUl /> },
  { key: "settings", label: "Настройки", icon: <FaCog /> },
];

function App() {
  const [mode, setMode] = useState("tasks");
  const [theme, setTheme] = useState(() => {
    try {
      return localStorage.getItem('vectora_theme') || 'dark';
    } catch {
      return 'dark';
    }
  });
  const [tasks, setTasks] = useState([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [filters, setFilters] = useState({ search: "", status: "all", priority: "all", category: "", tag: "" });
  const [sortBy, setSortBy] = useState("position");
  const { webApp, user } = useTelegramWebApp();

  // Мемоизированная функция загрузки задач
  const fetchTasks = useCallback(async (currentFilters = filters, currentSort = sortBy) => {
    try {
      // Строим query-параметры
      const params = new URLSearchParams();
      if (currentFilters.search) params.append('search', currentFilters.search);
      if (currentFilters.status !== 'all') params.append('status', currentFilters.status);
      if (currentFilters.priority !== 'all') params.append('priority', currentFilters.priority);
      if (currentFilters.category) params.append('category', currentFilters.category);
      if (currentFilters.tag) params.append('tag', currentFilters.tag);
      if (currentSort) params.append('sort_by', currentSort);
      
      const url = `${API_BASE}/tasks/?${params.toString()}`;
      const response = await fetch(url, {
        headers: {
          'Accept': 'application/json',
        },
      });
      const data = await response.json();
      setTasks(data);
    } catch (error) {
      console.error('Ошибка загрузки задач:', error);
    }
  }, [filters, sortBy]);

  const handleFilterChange = useCallback((newFilters) => {
    setFilters(newFilters);
    fetchTasks(newFilters, sortBy);
  }, [fetchTasks, sortBy]);

  const handleSortChange = useCallback((newSort) => {
    setSortBy(newSort);
    fetchTasks(filters, newSort);
  }, [fetchTasks, filters]);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  useEffect(() => {
    try {
      localStorage.setItem('vectora_theme', theme);
    } catch {}
  }, [theme]);

  const handleTaskMove = useCallback((sourceId, targetId) => {
    setTasks(prevTasks => {
      const newTasks = [...prevTasks];
      const sourceIndex = prevTasks.findIndex(t => t.id === sourceId);
      const targetIndex = prevTasks.findIndex(t => t.id === targetId);
      
      const [removed] = newTasks.splice(sourceIndex, 1);
      newTasks.splice(targetIndex, 0, removed);
      
      return newTasks;
    });
  }, []);

  const handleAddTask = useCallback(async (taskData) => {
    try {
      const response = await fetch(API_BASE + '/tasks/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          title: taskData.title,
          description: taskData.description,
          date_time: taskData.dateTime,
          priority: taskData.priority,
          category: taskData.category || null,
          status: false,
          position: tasks.length
        }),
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(error || 'Ошибка при создании задачи');
      }

      await fetchTasks();

      webApp?.showPopup({
        title: 'Готово',
        message: 'Задача создана',
        buttons: [{ type: 'close' }],
      });
    } catch (error) {
      console.error('Ошибка создания задачи:', error);
      webApp?.showPopup({
        title: 'Ошибка',
        message: error.message || 'Не удалось создать задачу',
        buttons: [{ type: 'close' }],
      });
      throw error;
    }
  }, [tasks.length, fetchTasks, webApp]);

  const handleStatusChange = useCallback(async (taskId) => {
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;

    // Оптимистичное обновление UI
    const prevTasks = tasks;
    setTasks(prevTasks.map(t => t.id === taskId ? { ...t, status: !t.status } : t));

    try {
      const response = await fetch(`${API_BASE}/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({ status: !task.status }),
      });

      if (!response.ok) {
        const text = await response.text();
        console.error('Ошибка ответа сервера:', response.status, text);
        // Откат UI при ошибке
        setTasks(prevTasks);
        try {
          webApp?.showPopup({ title: 'Ошибка', message: 'Не удалось изменить статус', buttons: [{ type: 'close' }] });
        } catch {}
      }
    } catch (error) {
      console.error('Ошибка обновления статуса:', error);
      // Откат UI при ошибке сети
      setTasks(prevTasks);
      try {
        webApp?.showPopup({ title: 'Ошибка', message: 'Проблема с сетью', buttons: [{ type: 'close' }] });
      } catch {}
    }
  }, [tasks, webApp]);

  const handleDeleteTask = useCallback(async (taskId) => {
    try {
      const response = await fetch(`${API_BASE}/tasks/${taskId}`, {
        method: 'DELETE',
        headers: {
          'Accept': 'application/json',
        },
      });

      if (response.ok) {
        setTasks(tasks.filter(t => t.id !== taskId));
        webApp?.showPopup({
          title: 'Готово',
          message: 'Задача удалена',
          buttons: [{ type: 'close' }],
        });
      }
    } catch (error) {
      console.error('Ошибка удаления задачи:', error);
      webApp?.showPopup({
        title: 'Ошибка',
        message: 'Не удалось удалить задачу',
        buttons: [{ type: 'close' }],
      });
    }
  }, [tasks, webApp]);

  const handleEditTask = useCallback((task) => {
    setEditingTask(task);
    setShowEditModal(true);
  }, []);

  const handleUpdateTask = useCallback(async (taskId, taskData) => {
    try {
      const response = await fetch(`${API_BASE}/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          title: taskData.title,
          description: taskData.description,
          date_time: taskData.dateTime,
          priority: taskData.priority,
          category: taskData.category,
        }),
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(error || 'Ошибка при обновлении задачи');
      }

      await fetchTasks();

      webApp?.showPopup({
        title: 'Готово',
        message: 'Задача обновлена',
        buttons: [{ type: 'close' }],
      });
    } catch (error) {
      console.error('Ошибка обновления задачи:', error);
      webApp?.showPopup({
        title: 'Ошибка',
        message: error.message || 'Не удалось обновить задачу',
        buttons: [{ type: 'close' }],
      });
      throw error;
    }
  }, [fetchTasks, webApp]);

  return (
    <div className={`tg-webapp theme-${theme}`}>
      <header className="tg-header">
        <h1 className="tg-title">Планер задач</h1>
        <ThemeSwitcher theme={theme} setTheme={setTheme} />
      </header>

      <main className="tg-main">
        {mode === "calendar" && (
          <CalendarView
            theme={theme}
            tasks={tasks}
            onTaskMove={handleTaskMove}
            onEditTask={handleEditTask}
          />
        )}
        {mode === "tasks" && (
          <>
            <TaskStats tasks={tasks} />
            <TaskFilters onFilterChange={handleFilterChange} initialFilters={filters} />
            <TaskSorter sortBy={sortBy} onSortChange={handleSortChange} />
            <TaskList
              theme={theme}
              tasks={tasks}
              onTaskMove={handleTaskMove}
              onStatusChange={handleStatusChange}
              onDeleteTask={handleDeleteTask}
              onEditTask={handleEditTask}
            />
          </>
        )}
        {mode === "settings" && (
          <div className="tg-settings">
            <h2>Настройки</h2>
            <ThemeSwitcher theme={theme} setTheme={setTheme} />
          </div>
        )}
      </main>

      <AddTaskModal 
        onSubmit={handleAddTask} 
        open={showAddModal} 
        setOpen={setShowAddModal} 
      />
      <EditTaskModal 
        task={editingTask} 
        onSubmit={handleUpdateTask} 
        open={showEditModal} 
        setOpen={setShowEditModal} 
      />
      <button className="tg-fab" onClick={() => setShowAddModal(true)}>
        <FaPlus />
      </button>

      <nav className="tg-bottom-nav">
        {MODES.map((m) => (
          <button
            key={m.key}
            className={`tg-nav-btn${mode === m.key ? " active" : ""}`}
            onClick={() => setMode(m.key)}
          >
            {m.icon}
            <span>{m.label}</span>
          </button>
        ))}
      </nav>
    </div>
  );
}

export default App;
