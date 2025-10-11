import React from 'react';
import { FaSortAmountDown, FaSortAmountUp, FaCalendar, FaFont, FaExclamationCircle } from 'react-icons/fa';
import './TaskSorter.css';

const TaskSorter = ({ sortBy, onSortChange }) => {
  const sortOptions = [
    { value: 'position', label: 'По порядку', icon: <FaSortAmountDown /> },
    { value: 'date', label: 'По дате', icon: <FaCalendar /> },
    { value: 'priority', label: 'По приоритету', icon: <FaExclamationCircle /> },
    { value: 'title', label: 'По алфавиту', icon: <FaFont /> },
  ];

  return (
    <div className="task-sorter">
      <div className="sorter-label">Сортировка:</div>
      <div className="sorter-buttons">
        {sortOptions.map((option) => (
          <button
            key={option.value}
            className={`sort-btn ${sortBy === option.value ? 'active' : ''}`}
            onClick={() => onSortChange(option.value)}
            title={option.label}
          >
            {option.icon}
            <span className="sort-label">{option.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
};

export default TaskSorter;
