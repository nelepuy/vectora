import React, { useState } from "react";
import { 
  DndContext, 
  closestCenter, 
  useSensor, 
  useSensors, 
  PointerSensor, 
  DragOverlay 
} from '@dnd-kit/core';
import { 
  SortableContext, 
  verticalListSortingStrategy, 
  useSortable 
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import "./TaskList.css";

const SortableTask = ({ task, onStatusChange, onDeleteTask }) => {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ 
    id: task.id,
    disabled: false
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  // Форматирование даты для отображения
  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(today.getDate() + 1);
    
    // Формат времени
  // Важно: dateStr приходит без Z, это локальное время; отображаем по локали пользователя
  const time = date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
    
    if (date.toDateString() === today.toDateString()) {
      return `Сегодня ${time}`;
    } else if (date.toDateString() === tomorrow.toDateString()) {
      return `Завтра ${time}`;
    } else {
      return `${date.toLocaleDateString('ru-RU')} ${time}`;
    }
  };

  // Иконка приоритета
  const getPriorityIcon = (priority) => {
    switch (priority) {
      case 'high': return '🔥';
      case 'medium': return '⚡';
      case 'low': return '💎';
      default: return '📋';
    }
  };

  // Цвет приоритета
  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return '#ff3366';
      case 'medium': return '#ffaa00';
      case 'low': return '#00ff88';
      default: return '#666';
    }
  };

  // Чекбокс — не связан с перетаскиванием
  const handleCheckboxChange = (e) => {
    e.stopPropagation();
    onStatusChange(task.id);
  };

  const handleDelete = (e) => {
    e.stopPropagation();
    onDeleteTask(task.id);
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={`tg-task-item ${task.status === 'completed' ? 'completed' : ''} ${isDragging ? 'dragging' : ''}`}
    >
      <div 
        className="task-drag-handle"
        {...listeners}
        {...attributes}
        title="Перетащить задачу"
      >
        <div className="drag-dots">
          <div className="dot"></div>
          <div className="dot"></div>
          <div className="dot"></div>
          <div className="dot"></div>
          <div className="dot"></div>
          <div className="dot"></div>
        </div>
      </div>

      {/* Основной контент — не перетаскивается */}
      <div className="task-content">
        {/* Чекбокс — изолирован от DnD */}
        <div className="task-checkbox-container">
          <input
            type="checkbox"
            checked={task.status === 'completed'}
            onChange={handleCheckboxChange}
            className="task-checkbox"
            onClick={(e) => e.stopPropagation()}
          />
        </div>

        {/* Информация о задаче */}
        <div className="task-info">
          <div className="task-header">
            <h3 className="task-title">
              <span 
                className="priority-icon"
                style={{ color: getPriorityColor(task.priority) }}
              >
                {getPriorityIcon(task.priority)}
              </span>
              {task.title}
            </h3>
            <span className="task-priority" style={{ color: getPriorityColor(task.priority) }}>
              {task.priority}
            </span>
          </div>
          
          {task.description && (
            <p className="task-description">{task.description}</p>
          )}
          
          {task.date_time && (
            <div className="task-datetime">
              📅 {formatDate(task.date_time)}
            </div>
          )}
        </div>

        {/* Удаление — изолировано от DnD */}
        <div className="task-actions">
          <button
            className="delete-btn"
            onClick={handleDelete}
            title="Удалить задачу"
          >
            🗑️
          </button>
        </div>
      </div>
    </div>
  );
};

function TaskList({ theme, tasks = [], onTaskMove, onStatusChange, onDeleteTask }) {
  const [activeId, setActiveId] = useState(null);
  
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    })
  );

  const handleDragStart = (event) => {
    setActiveId(event.active.id);
  };

  const handleDragEnd = (event) => {
    const { active, over } = event;
    
    if (active.id !== over?.id) {
      onTaskMove(active.id, over.id);
    }
    
    setActiveId(null);
  };

  const handleDragCancel = () => {
    setActiveId(null);
  };

  // Активная задача для DragOverlay
  const activeTask = tasks.find(task => task.id === activeId);

  return (
    <div className={`tg-task-list tg-task-list-${theme}`}>
      <h2>Список задач</h2>
      <DndContext
        sensors={sensors}
        collisionDetection={closestCenter}
        onDragStart={handleDragStart}
        onDragEnd={handleDragEnd}
        onDragCancel={handleDragCancel}
      >
        <SortableContext items={tasks.map(t => t.id)} strategy={verticalListSortingStrategy}>
          {tasks.map((task) => (
            <SortableTask
              key={task.id}
              task={task}
              onStatusChange={onStatusChange}
              onDeleteTask={onDeleteTask}
            />
          ))}
        </SortableContext>
        
        {/* Визуальный оверлей при перетаскивании */}
        <DragOverlay>
          {activeTask ? (
            <div className="tg-task-item dragging-overlay">
              <div className="task-drag-handle">
                <div className="drag-dots">
                  <div className="dot"></div>
                  <div className="dot"></div>
                  <div className="dot"></div>
                  <div className="dot"></div>
                  <div className="dot"></div>
                  <div className="dot"></div>
                </div>
              </div>
              <div className="task-content">
                <div className="task-info">
                  <div className="task-header">
                    <h3 className="task-title">{activeTask.title}</h3>
                  </div>
                </div>
              </div>
            </div>
          ) : null}
        </DragOverlay>
      </DndContext>
    </div>
  );
}

export default TaskList;
