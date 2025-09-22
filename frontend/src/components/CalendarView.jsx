import React, { useState } from 'react';
import { Calendar, dateFnsLocalizer } from 'react-big-calendar';
import { DndContext, closestCenter, useSensor, useSensors, PointerSensor } from '@dnd-kit/core';
import { format, parse, startOfWeek, getDay } from 'date-fns';
import { ru } from 'date-fns/locale';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import './CalendarView.css';

const locales = {
  'ru': ru,
};

const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
});

function CalendarView({ theme, tasks = [], onTaskMove }) {
  const [view, setView] = useState('week');
  const [date, setDate] = useState(new Date());

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    })
  );

  const events = tasks.map(task => {
    const start = new Date(task.date_time);
    // Устанавливаем конец события на час позже начала
    const end = new Date(start);
    end.setHours(end.getHours() + 1);
    
    return {
      id: task.id,
      title: task.title,
      start,
      end,
      isDone: task.status,
      priority: task.priority
    };
  });

  const handleDragEnd = (event) => {
    const { active, over } = event;
    if (active && over) {
      onTaskMove(active.id, over.id);
    }
  };

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCenter}
      onDragEnd={handleDragEnd}
    >
      <div className={`tg-calendar tg-calendar-${theme}`}>
        <Calendar
          localizer={localizer}
          events={events}
          startAccessor="start"
          endAccessor="end"
          view={view}
          onView={setView}
          date={date}
          onNavigate={setDate}
          className={`calendar-${theme}`}
          messages={{
            next: "Вперед",
            previous: "Назад",
            today: "Сегодня",
            month: "Месяц",
            week: "Неделя",
            day: "День",
            agenda: "Список"
          }}
          eventPropGetter={(event) => ({
            className: `event-${event.priority || 'normal'}${event.isDone ? ' event-done' : ''}`
          })}
        />
      </div>
    </DndContext>
  );
}

export default CalendarView;
