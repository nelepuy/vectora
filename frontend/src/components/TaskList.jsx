import React, { useState, useMemo, memo } from "react";
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

const SortableTask = memo(({ task, onStatusChange, onDeleteTask, onEditTask }) => {
  const {
    attributes,
    listeners,
    setNodeRef,
    setActivatorNodeRef,
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

  // Иконка категории
  const getCategoryIcon = (category) => {
    if (!category) return '📁';
    const categoryLower = category.toLowerCase();
    if (categoryLower.includes('работ')) return '💼';
    if (categoryLower.includes('личн')) return '👤';
    if (categoryLower.includes('учеб') || categoryLower.includes('образован')) return '📚';
    if (categoryLower.includes('дом') || categoryLower.includes('быт')) return '🏠';
    if (categoryLower.includes('здоров') || categoryLower.includes('спорт')) return '💪';
    if (categoryLower.includes('покуп') || categoryLower.includes('магазин')) return '🛒';
    if (categoryLower.includes('финанс') || categoryLower.includes('деньг')) return '💰';
    if (categoryLower.includes('путеш') || categoryLower.includes('поездк')) return '✈️';
    if (categoryLower.includes('хобби') || categoryLower.includes('творч')) return '🎨';
    if (categoryLower.includes('семь')) return '👨‍👩‍👧‍👦';
    return '📁';
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

  const handleEdit = (e) => {
    e.stopPropagation();
    onEditTask(task);
  };

  const blockDndForInteractive = (e) => {
    const target = e.target;
    if (
      target.closest?.('.task-checkbox') ||
      target.closest?.('.delete-btn') ||
      target.closest?.('.edit-btn') ||
      target.closest?.('.task-actions')
    ) {
      e.stopPropagation();
    }
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={`tg-task-item ${task.status ? 'completed' : ''} ${isDragging ? 'dragging' : ''}`}
      onPointerDownCapture={blockDndForInteractive}
      onMouseDownCapture={blockDndForInteractive}
    >
      <div 
        className="task-drag-handle"
        ref={setActivatorNodeRef}
        {...attributes}
        {...listeners}
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
  <div className="task-content" onPointerDownCapture={blockDndForInteractive} onMouseDownCapture={blockDndForInteractive}>
        {/* Чекбокс — изолирован от DnD */}
        <div className="task-checkbox-container">
          <input
            type="checkbox"
            checked={!!task.status}
            onChange={handleCheckboxChange}
            className="task-checkbox"
            onClick={(e) => e.stopPropagation()}
            onPointerDown={(e) => e.stopPropagation()}
            onMouseDown={(e) => e.stopPropagation()}
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
          
          {/* Категория */}
          {task.category && (
            <div className="task-meta">
              <span className="task-category">
                {getCategoryIcon(task.category)} {task.category}
              </span>
            </div>
          )}
        </div>

        {/* Действия — изолированы от DnD */}
        <div className="task-actions">
          <button
            className="edit-btn"
            onClick={handleEdit}
            onPointerDown={(e) => e.stopPropagation()}
            onMouseDown={(e) => e.stopPropagation()}
            title="Редактировать задачу"
          >
            ✏️
          </button>
          <button
            className="delete-btn"
            onClick={handleDelete}
            onPointerDown={(e) => e.stopPropagation()}
            onMouseDown={(e) => e.stopPropagation()}
            title="Удалить задачу"
          >
            🗑️
          </button>
        </div>
      </div>
    </div>
  );
});

function TaskList({ theme, tasks = [], onTaskMove, onStatusChange, onDeleteTask, onEditTask }) {
  const [activeId, setActiveId] = useState(null);
  
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
        delay: 120,
        tolerance: 5,
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

  // Группировка задач по дням (мемоизированная)
  const groupedTasks = useMemo(() => {
    const groups = {};
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    tasks.forEach(task => {
      let groupKey;
      let groupLabel;
      let sortOrder;
      
      if (!task.date_time) {
        groupKey = 'no-date';
        groupLabel = '📌 Без срока';
        sortOrder = new Date(8640000000000000); // Максимальная дата
      } else {
        const taskDate = new Date(task.date_time);
        taskDate.setHours(0, 0, 0, 0);
        sortOrder = taskDate;
        
        if (taskDate.getTime() === today.getTime()) {
          groupKey = 'today';
          groupLabel = '🔥 Сегодня';
        } else if (taskDate.getTime() === tomorrow.getTime()) {
          groupKey = 'tomorrow';
          groupLabel = '⭐ Завтра';
        } else if (taskDate < today) {
          groupKey = 'overdue';
          groupLabel = '⚠️ Просрочено';
        } else {
          groupKey = taskDate.toISOString();
          groupLabel = `📅 ${taskDate.toLocaleDateString('ru-RU', { weekday: 'long', day: 'numeric', month: 'long' })}`;
        }
      }

      if (!groups[groupKey]) {
        groups[groupKey] = { label: groupLabel, tasks: [], sortOrder: sortOrder };
      }
      groups[groupKey].tasks.push(task);
    });

    // Сортируем группы: просрочено, сегодня, завтра, будущие даты, без срока
    const sortedGroups = Object.entries(groups).sort(([keyA, groupA], [keyB, groupB]) => {
      if (keyA === 'overdue') return -1;
      if (keyB === 'overdue') return 1;
      if (keyA === 'today') return -1;
      if (keyB === 'today') return 1;
      if (keyA === 'tomorrow') return -1;
      if (keyB === 'tomorrow') return 1;
      if (keyA === 'no-date') return 1;
      if (keyB === 'no-date') return -1;
      return groupA.sortOrder - groupB.sortOrder;
    });

    return sortedGroups;
  }, [tasks]);

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
        {groupedTasks.map(([groupKey, group]) => (
          <div key={groupKey} className="task-group">
            <h3 className="task-group-header">{group.label}</h3>
            <SortableContext items={group.tasks.map(t => t.id)} strategy={verticalListSortingStrategy}>
              {group.tasks.map((task) => (
                <SortableTask
                  key={task.id}
                  task={task}
                  onStatusChange={onStatusChange}
                  onDeleteTask={onDeleteTask}
                  onEditTask={onEditTask}
                />
              ))}
            </SortableContext>
          </div>
        ))}
        
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
