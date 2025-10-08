import React, { useMemo } from "react";
import "./TaskStats.css";

function TaskStats({ tasks }) {
  const stats = useMemo(() => {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    
    return {
      total: tasks.length,
      completed: tasks.filter(t => t.status).length,
      active: tasks.filter(t => !t.status).length,
      
      // Приоритеты
      highPriority: tasks.filter(t => t.priority === 'high' && !t.status).length,
      normalPriority: tasks.filter(t => t.priority === 'normal' && !t.status).length,
      lowPriority: tasks.filter(t => t.priority === 'low' && !t.status).length,
      
      // Сегодняшние задачи
      todayTasks: tasks.filter(t => {
        if (!t.date_time) return false;
        const taskDate = new Date(t.date_time);
        return taskDate.toDateString() === today.toDateString();
      }).length,
      
      // Просроченные задачи
      overdue: tasks.filter(t => {
        if (!t.date_time || t.status) return false;
        const taskDate = new Date(t.date_time);
        return taskDate < now;
      }).length,
    };
  }, [tasks]);

  const completionRate = stats.total > 0 
    ? Math.round((stats.completed / stats.total) * 100) 
    : 0;

  return (
    <div className="task-stats">
      <div className="stats-grid">
        {/* Общая статистика */}
        <div className="stat-card total">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <div className="stat-value">{stats.total}</div>
            <div className="stat-label">Всего задач</div>
          </div>
        </div>

        <div className="stat-card active">
          <div className="stat-icon">⚡</div>
          <div className="stat-content">
            <div className="stat-value">{stats.active}</div>
            <div className="stat-label">Активные</div>
          </div>
        </div>

        <div className="stat-card completed">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <div className="stat-value">{stats.completed}</div>
            <div className="stat-label">Завершено</div>
          </div>
        </div>

        <div className="stat-card completion">
          <div className="stat-icon">📈</div>
          <div className="stat-content">
            <div className="stat-value">{completionRate}%</div>
            <div className="stat-label">Выполнено</div>
          </div>
        </div>

        {/* Приоритеты */}
        {stats.highPriority > 0 && (
          <div className="stat-card priority-high">
            <div className="stat-icon">🔥</div>
            <div className="stat-content">
              <div className="stat-value">{stats.highPriority}</div>
              <div className="stat-label">Высокий приоритет</div>
            </div>
          </div>
        )}

        {/* Сегодняшние задачи */}
        {stats.todayTasks > 0 && (
          <div className="stat-card today">
            <div className="stat-icon">📅</div>
            <div className="stat-content">
              <div className="stat-value">{stats.todayTasks}</div>
              <div className="stat-label">На сегодня</div>
            </div>
          </div>
        )}

        {/* Просроченные */}
        {stats.overdue > 0 && (
          <div className="stat-card overdue">
            <div className="stat-icon">⚠️</div>
            <div className="stat-content">
              <div className="stat-value">{stats.overdue}</div>
              <div className="stat-label">Просрочено</div>
            </div>
          </div>
        )}
      </div>

      {/* Прогресс-бар */}
      {stats.total > 0 && (
        <div className="progress-section">
          <div className="progress-label">
            <span>Прогресс выполнения</span>
            <span className="progress-percentage">{completionRate}%</span>
          </div>
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${completionRate}%` }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default TaskStats;
