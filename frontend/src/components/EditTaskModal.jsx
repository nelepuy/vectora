import React, { useState, useEffect } from "react";
import { FaTimes } from "react-icons/fa";
import useTelegramWebApp from "../hooks/useTelegramWebApp";

function EditTaskModal({ task, onSubmit, open, setOpen }) {
  const { webApp } = useTelegramWebApp();
  
  const formatLocalDate = (d) => {
    if (!d) return "";
    const date = new Date(d);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  const formatLocalTime = (d) => {
    if (!d) return "";
    const date = new Date(d);
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${hours}:${minutes}`;
  };

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
  });

  // Заполняем форму данными задачи при открытии
  useEffect(() => {
    if (task && open) {
      setTaskData({
        title: task.title || "",
        description: task.description || "",
        date: task.date_time ? formatLocalDate(task.date_time) : "",
        time: task.date_time ? formatLocalTime(task.date_time) : "",
        priority: task.priority || "normal",
        category: task.category || "",
      });
    }
  }, [task, open]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      let dateTimeValue = null;
      
      // Если заполнены дата И время - формируем dateTime
      if (taskData.date && taskData.time) {
        const [hours, minutes] = taskData.time.split(":");
        const dateTime = new Date(taskData.date);
        dateTime.setHours(parseInt(hours), parseInt(minutes), 0, 0);
        dateTimeValue = toLocalISOStringNoTZ(dateTime);
      }

      await onSubmit(task.id, {
        title: taskData.title,
        description: taskData.description,
        priority: taskData.priority,
        category: taskData.category || null,
        dateTime: dateTimeValue,
      });

      setOpen(false);
    } catch (error) {
      console.error("Ошибка при обновлении задачи:", error);
      webApp?.showPopup({
        title: "Ошибка",
        message: "Не удалось обновить задачу",
        buttons: [{ type: "close" }],
      });
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setTaskData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  if (!open || !task) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h2>Редактировать задачу</h2>
          <button onClick={() => setOpen(false)} className="close-button">
            <FaTimes />
          </button>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="edit-title">Название</label>
            <input
              type="text"
              id="edit-title"
              name="title"
              value={taskData.title}
              onChange={handleChange}
              required
              className="input-field"
              placeholder="Введите название задачи"
            />
          </div>
          <div className="form-group">
            <label htmlFor="edit-description">Описание</label>
            <textarea
              id="edit-description"
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
              <label htmlFor="edit-date">Дата (необязательно)</label>
              <input
                type="date"
                id="edit-date"
                name="date"
                value={taskData.date}
                onChange={handleChange}
                className="input-field"
              />
            </div>
            <div className="form-group">
              <label htmlFor="edit-time">Время (необязательно)</label>
              <input
                type="time"
                id="edit-time"
                name="time"
                value={taskData.time}
                onChange={handleChange}
                className="input-field"
              />
            </div>
          </div>
          <div className="form-group">
            <label htmlFor="edit-priority">Приоритет</label>
            <select
              id="edit-priority"
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
            <label htmlFor="edit-category">Категория</label>
            <input
              type="text"
              id="edit-category"
              name="category"
              value={taskData.category}
              onChange={handleChange}
              className="input-field"
              placeholder="Работа, Личное, Учеба..."
              list="edit-categories-list"
            />
            <datalist id="edit-categories-list">
              <option value="Работа" />
              <option value="Личное" />
              <option value="Учеба" />
              <option value="Дом" />
              <option value="Здоровье" />
            </datalist>
          </div>
          <div className="modal-footer">
            <button
              type="button"
              onClick={() => setOpen(false)}
              className="button secondary"
            >
              Отмена
            </button>
            <button type="submit" className="button primary">
              Сохранить
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default EditTaskModal;
