import React, { useState } from "react";
import { FaTimes } from "react-icons/fa";
import useTelegramWebApp from "../hooks/useTelegramWebApp";

function AddTaskModal({ onSubmit, open, setOpen }) {
  const { webApp } = useTelegramWebApp();
  // Формат YYYY-MM-DD в локальном времени (для input type=date)
  const formatLocalDate = (d) => {
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  // Локальный ISO без часового пояса (без Z), чтобы сервер сохранил «настенные» часы
  const toLocalISOStringNoTZ = (d) => {
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    const hh = String(d.getHours()).padStart(2, '0');
    const mm = String(d.getMinutes()).padStart(2, '0');
    const ss = String(d.getSeconds()).padStart(2, '0');
    return `${y}-${m}-${day}T${hh}:${mm}:${ss}`;
  };
  const [taskData, setTaskData] = useState({
    title: "",
    description: "",
    date: "",
    time: "",
    priority: "normal",
    category: "",
    recurrence_type: "",
    recurrence_interval: 1,
    reminder_enabled: false,
    reminder_minutes_before: 30,
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    let dateTimeValue = null;
    
    // Если заполнены дата И время - формируем dateTime
    if (taskData.date && taskData.time) {
      const [hours, minutes] = taskData.time.split(":");
      const dateTime = new Date(taskData.date);
      dateTime.setHours(parseInt(hours), parseInt(minutes), 0, 0);
      dateTimeValue = toLocalISOStringNoTZ(dateTime);
    }

    try {
      await onSubmit({
        title: taskData.title,
        description: taskData.description,
        priority: taskData.priority,
        category: taskData.category || null,
        dateTime: dateTimeValue,
        recurrence_type: taskData.recurrence_type || null,
        recurrence_interval: taskData.recurrence_type ? parseInt(taskData.recurrence_interval) : null,
        reminder_enabled: taskData.reminder_enabled,
        reminder_minutes_before: taskData.reminder_enabled ? parseInt(taskData.reminder_minutes_before) : null,
      });
    } catch (error) {
      console.error("Ошибка при создании задачи:", error);
    }

    setOpen(false);
    setTaskData({
      title: "",
      description: "",
      date: "",
      time: "",
      priority: "normal",
      category: "",
      recurrence_type: "",
      recurrence_interval: 1,
      reminder_enabled: false,
      reminder_minutes_before: 30,
    });
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setTaskData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <>
      {open && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h2>Новая задача</h2>
              <button onClick={() => setOpen(false)} className="close-button">
                <FaTimes />
              </button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="title">Название</label>
                <input
                  type="text"
                  id="title"
                  name="title"
                  value={taskData.title}
                  onChange={handleChange}
                  required
                  className="input-field"
                  placeholder="Введите название задачи"
                />
              </div>
              <div className="form-group">
                <label htmlFor="description">Описание</label>
                <textarea
                  id="description"
                  name="description"
                  value={taskData.description}
                  onChange={handleChange}
                  rows="3"
                  className="input-field"
                  placeholder="Введите описание задачи"
                />
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="date">Дата (необязательно)</label>
                  <input
                    type="date"
                    id="date"
                    name="date"
                    value={taskData.date}
                    onChange={handleChange}
                    className="input-field"
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="time">Время (необязательно)</label>
                  <input
                    type="time"
                    id="time"
                    name="time"
                    value={taskData.time}
                    onChange={handleChange}
                    className="input-field"
                  />
                </div>
              </div>
              <div className="form-group">
                <label htmlFor="priority">Приоритет</label>
                <select
                  id="priority"
                  name="priority"
                  value={taskData.priority}
                  onChange={handleChange}
                  className="input-field"
                >
                  <option value="low">Низкий</option>
                  <option value="normal">Средний</option>
                  <option value="high">Высокий</option>
                </select>
              </div>
              <div className="form-group">
                <label htmlFor="category">Категория</label>
                <input
                  type="text"
                  id="category"
                  name="category"
                  value={taskData.category}
                  onChange={handleChange}
                  className="input-field"
                  placeholder="Работа, Личное, Учеба..."
                  list="categories-list"
                />
                <datalist id="categories-list">
                  <option value="Работа" />
                  <option value="Личное" />
                  <option value="Учеба" />
                  <option value="Дом" />
                  <option value="Здоровье" />
                </datalist>
              </div>
              
              <div className="form-group">
                <label htmlFor="recurrence_type">Повторение</label>
                <select
                  id="recurrence_type"
                  name="recurrence_type"
                  value={taskData.recurrence_type}
                  onChange={handleChange}
                  className="input-field"
                >
                  <option value="">Не повторять</option>
                  <option value="daily">Ежедневно</option>
                  <option value="weekly">Еженедельно</option>
                  <option value="monthly">Ежемесячно</option>
                </select>
              </div>

              {taskData.recurrence_type && (
                <div className="form-group">
                  <label htmlFor="recurrence_interval">Интервал</label>
                  <input
                    type="number"
                    id="recurrence_interval"
                    name="recurrence_interval"
                    value={taskData.recurrence_interval}
                    onChange={handleChange}
                    min="1"
                    max="30"
                    className="input-field"
                  />
                </div>
              )}

              <div className="form-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    name="reminder_enabled"
                    checked={taskData.reminder_enabled}
                    onChange={(e) => handleChange({ target: { name: 'reminder_enabled', value: e.target.checked } })}
                  />
                  <span>Напоминание</span>
                </label>
              </div>

              {taskData.reminder_enabled && (
                <div className="form-group">
                  <label htmlFor="reminder_minutes_before">За сколько минут</label>
                  <select
                    id="reminder_minutes_before"
                    name="reminder_minutes_before"
                    value={taskData.reminder_minutes_before}
                    onChange={handleChange}
                    className="input-field"
                  >
                    <option value="5">5 минут</option>
                    <option value="15">15 минут</option>
                    <option value="30">30 минут</option>
                    <option value="60">1 час</option>
                    <option value="1440">1 день</option>
                  </select>
                </div>
              )}

              <div className="modal-footer">
                <button
                  type="button"
                  onClick={() => setOpen(false)}
                  className="button secondary"
                >
                  Отмена
                </button>
                <button type="submit" className="button primary">
                  Добавить
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}

export default AddTaskModal;
