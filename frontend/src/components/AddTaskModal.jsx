import React, { useState } from "react";
import { FaTimes } from "react-icons/fa";
import useTelegramWebApp from "../hooks/useTelegramWebApp";

function AddTaskModal({ onSubmit, open, setOpen }) {
  const { webApp } = useTelegramWebApp();
  const [taskData, setTaskData] = useState({
    title: "",
    description: "",
    date: new Date().toISOString().split("T")[0],
    time: "12:00",
    priority: "normal",
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const [hours, minutes] = taskData.time.split(":");
      const dateTime = new Date(taskData.date);
      dateTime.setHours(parseInt(hours), parseInt(minutes));

      await onSubmit({
        ...taskData,
        dateTime: dateTime.toISOString(),
      });

      // Закрываем модалку
      setOpen(false);
      
      // Сбрасываем форму
      setTaskData({
        title: "",
        description: "",
        date: new Date().toISOString().split("T")[0],
        time: "12:00",
        priority: "normal",
      });
    } catch (error) {
      console.error("Ошибка при создании задачи:", error);
      webApp?.showPopup({
        title: "Ошибка",
        message: "Не удалось создать задачу",
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
                  <label htmlFor="date">Дата</label>
                  <input
                    type="date"
                    id="date"
                    name="date"
                    value={taskData.date}
                    onChange={handleChange}
                    required
                    className="input-field"
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="time">Время</label>
                  <input
                    type="time"
                    id="time"
                    name="time"
                    value={taskData.time}
                    onChange={handleChange}
                    required
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
