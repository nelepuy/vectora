# Vectora Frontend (React)

Фронтенд Telegram Mini App на React 18. Поддерживает drag & drop, тёмную/светлую темы и интеграцию с Telegram Web App.

## Возможности

- Список задач и календарный режим
- Перетаскивание задач (dnd-kit)
- Приоритеты, даты/время, статусы
- Интеграция с Telegram (hook `useTelegramWebApp`)

## Быстрый старт

```powershell
cd frontend
npm install
npm start
```

Откроется: http://localhost:3000

## Переменные окружения (`frontend/.env`)
# Vectora Frontend (React)

Фронтенд Telegram Mini App на React 18. Поддерживает drag & drop, светлую/тёмную темы и интеграцию с Telegram Web App.

## Запуск

```powershell
cd frontend
npm install
npm start
```

Откроется: http://localhost:3000

## Переменные окружения (`frontend/.env`)

```
# Для разработки можно указать прямой URL API
REACT_APP_API_URL=http://localhost:8000

# В продакшене лучше проксировать /api через тот же домен
```

## Структура

```
frontend/
├─ public/
└─ src/
  ├─ components/
  ├─ hooks/
  ├─ App.jsx
  └─ App.css
```

## Сборка

```powershell
npm run build
```

Готовый билд обслуживается Nginx (см. Dockerfile и nginx.conf).

# Serve locally for testing

npx serve -s build│   │

```

│   ├── utils/               # Utility functions   ```

### Performance Optimizations

- Code splitting by route│   │   ├── api.js           # API client

- Lazy loading of components

- Image optimization│   │   └── helpers.js       # Helper functions### Темы

- Bundle analysis and optimization

│   │

## 🤝 Contributing

│   ├── App.jsx              # Main app component3. **Set up environment variables**

1. Follow React best practices

2. Use functional components with hooks│   ├── App.css              # Global styles

3. Maintain consistent styling with CSS custom properties

4. Write tests for new components│   └── index.js             # App entry point   ```bashПриложение поддерживает несколько тем:

5. Follow the established file structure

│

## 📄 Dependencies

├── Dockerfile               # Development container   cp .env.example .env- Light (светлая)

### Production Dependencies

- `react`: ^18.2.0├── Dockerfile.prod          # Production container

- `react-dom`: ^18.2.0

- `@dnd-kit/core`: ^6.0.8├── package.json             # Dependencies and scripts   ```- Dark (тёмная)

- `@dnd-kit/sortable`: ^7.0.2

- `lucide-react`: ^0.263.1└── README.md               # This file



### Development Dependencies```   Edit `.env` and set:- Blue (синяя)

- `@testing-library/react`: ^13.4.0

- `@testing-library/jest-dom`: ^5.16.4

- `@testing-library/user-event`: ^14.4.3

- `react-scripts`: 5.0.1## 🎨 Design System   ```- Purple (фиолетовая)



## 🙏 Acknowledgments



- **React Team** - Amazing framework and ecosystem### Color Palette   REACT_APP_API_URL=http://localhost:8000

- **dnd-kit** - Excellent drag-and-drop library

- **Lucide** - Beautiful icon system```css

- **Create React App** - Development tooling and build system

:root {   ```Темы автоматически синхронизируются с настройками Telegram.

---

  /* Neon Colors */

<div align="center">

  --neon-blue: #00D4FF;      /* Primary accent */

**Part of the Vectora cyberpunk task management ecosystem**

  --neon-purple: #8A2BE2;    /* Secondary accent */

</div>
  --neon-green: #00FF88;     /* Success states */4. **Start development server**### Календарь

  --neon-red: #FF3366;       /* Error states */

  --neon-orange: #FFAA00;    /* Warning states */   ```bash



  /* Dark Theme */   npm start- Неделя/День/Месяц представления

  --bg-primary: #0A0A0A;     /* Main background */

  --bg-secondary: #1A1A1A;   /* Card backgrounds */   ```- Drag-and-drop задач

  --text-primary: #FFFFFF;   /* Primary text */

  --text-secondary: #B0B0B0; /* Secondary text */- Цветовая индикация приоритета

}

```5. **Open your browser**- Поддержка русской локализации



### Typography   Navigate to `http://localhost:3000`

- **Primary Font**: Orbitron (futuristic, sci-fi feel)

- **Fallback**: Sans-serif system fonts### Список задач

- **Sizes**: Responsive scaling with clamp()

### Docker Development

### Components

- Сортировка перетаскиванием

#### TaskList Component

- Drag and drop functionality1. **Build the container**- Статус выполнения

- Priority visual indicators

- Checkbox interactions   ```bash- Приоритеты с цветовой индикацией

- Status-based styling

   docker build -t singularityapp-frontend .- Адаптивный дизайн

#### AddTaskModal Component

- Form validation   ```

- Date/time picker

- Priority selection### Добавление задач

- Responsive modal design

2. **Run the container**

#### ThemeSwitcher Component

- Dark/Light mode toggle   ```bash- Форма с валидацией

- Smooth transitions

- Theme persistence   docker run -p 3000:80 singularityapp-frontend- Выбор даты и времени



## ⚙️ Configuration   ```- Установка приоритета



### Environment Variables- Интеграция с Telegram уведомлениями

## 🏗️ Project Structure

Create `.env` file in frontend directory:

```

```envfrontend/

# API Configuration├── public/                 # Static assets

REACT_APP_API_URL=http://localhost:8000├── src/

REACT_APP_TELEGRAM_BOT_TOKEN=your_bot_token_here│   ├── components/        # React components

│   │   ├── TaskList.jsx   # Main task list with drag&drop

# Development│   │   ├── AddTaskModal.jsx # Task creation modal

REACT_APP_DEBUG=true│   │   ├── CalendarView.jsx # Calendar interface

REACT_APP_VERSION=1.0.0│   │   └── ThemeSwitcher.jsx # Theme toggle

```│   ├── hooks/             # Custom React hooks

│   │   └── useTelegramWebApp.js # Telegram integration

### Build Configuration│   ├── App.jsx            # Main application component

│   ├── App.css            # Global cyberpunk styles

The project uses Create React App with custom optimizations:│   └── index.js           # Application entry point

- Bundle splitting├── Dockerfile             # Docker configuration

- Tree shaking├── package.json           # Dependencies and scripts

- Code optimization└── README.md             # This file

- Asset optimization```



## 🧪 Testing## 🎨 Styling & Theme



```bash### Cyberpunk Design System

# Run all tests

npm testThe application features a futuristic cyberpunk aesthetic with:



# Run tests in watch mode- **Neon Colors**: Electric blue (#00D4FF), neon purple (#8A2BE2), neon green (#00FF88)

npm run test:watch- **Typography**: Orbitron font for headers, clean sans-serif for body text

- **Effects**: Glowing borders, gradient backgrounds, subtle animations

# Generate coverage report- **Dark Theme**: Deep blacks and dark greys with neon accents

npm run test:coverage- **Light Theme**: Clean whites with colored accents

```

### CSS Architecture

## 📱 Browser Support

- **Global styles** in `App.css` define theme variables and base styles

- Chrome (90+)- **Component styles** in individual CSS files for modularity

- Firefox (88+)- **CSS Custom Properties** for theme switching

- Safari (14+)- **Responsive design** with mobile-first approach

- Edge (90+)

## 🔧 Component Guide

## 🚀 Production Deployment

### TaskList Component

### Build Process

```bashThe main task management interface featuring:

# Create optimized build

npm run build```jsx

<TaskList

# Serve locally for testing  theme={theme}

npx serve -s build  tasks={tasks}

```  onTaskMove={handleTaskMove}

  onStatusChange={handleStatusChange}

### Performance Optimizations  onDeleteTask={handleDeleteTask}

- Code splitting by route/>

- Lazy loading of components```

- Image optimization

- Bundle analysis and optimization**Features:**

- Drag handle for reordering tasks

## 🤝 Contributing- Checkbox for task completion

- Priority icons and colors

1. Follow React best practices- Delete button with confirmation

2. Use functional components with hooks- Visual feedback during drag operations

3. Maintain consistent styling with CSS custom properties

4. Write tests for new components### AddTaskModal Component

5. Follow the established file structure

Task creation modal with form validation:

## 📄 Dependencies

```jsx

### Production Dependencies<AddTaskModal

- `react`: ^18.2.0  onSubmit={handleAddTask}

- `react-dom`: ^18.2.0  open={showAddModal}

- `@dnd-kit/core`: ^6.0.8  setOpen={setShowAddModal}

- `@dnd-kit/sortable`: ^7.0.2/>

- `lucide-react`: ^0.263.1```



### Development Dependencies**Features:**

- `@testing-library/react`: ^13.4.0- Title and description input

- `@testing-library/jest-dom`: ^5.16.4- Date and time picker

- `@testing-library/user-event`: ^14.4.3- Priority selection

- `react-scripts`: 5.0.1- Form validation

- Success/error feedback

## 🙏 Acknowledgments

## 🌐 API Integration

- **React Team** - Amazing framework and ecosystem

- **dnd-kit** - Excellent drag-and-drop libraryThe frontend communicates with a FastAPI backend:

- **Lucide** - Beautiful icon system

- **Create React App** - Development tooling and build system### API Endpoints



---- `GET /tasks` - Fetch all tasks

- `POST /tasks` - Create new task

<div align="center">- `PUT /tasks/{id}` - Update task

- `DELETE /tasks/{id}` - Delete task

**Part of the Vectora cyberpunk task management ecosystem**

### Request/Response Format

</div>
```javascript
// Task Object
{
  id: 1,
  title: "Task title",
  description: "Task description",
  date_time: "2023-12-01T12:00:00Z",
  priority: "high|medium|low",
  status: true|false,
  position: 0
}
```

## 📱 Telegram Integration

The app includes Telegram Web App integration:

- Access to Telegram user data
- Native Telegram UI elements
- Haptic feedback
- Popup notifications
- Theme detection from Telegram

## 🔒 Environment Variables

```env
# API Configuration
REACT_APP_API_URL=http://localhost:8000

# Optional: Telegram Bot Token for development
REACT_APP_TELEGRAM_BOT_TOKEN=your_bot_token_here
```

## 🚀 Deployment

### Production Build

```bash
npm run build
```

### Docker Production

```bash
# Build production image
docker build -f Dockerfile.prod -t singularityapp-frontend:prod .

# Run production container
docker run -p 80:80 singularityapp-frontend:prod
```

### Nginx Configuration

The Docker image includes an optimized Nginx configuration for serving the React app with:

- Gzip compression
- Proper caching headers
- SPA routing support
- Security headers

## 🧪 Testing

```bash
# Run tests
npm test

# Run tests with coverage
npm test -- --coverage
```

## 🔍 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **SingularityNET** - Design inspiration
- **dnd-kit** - Excellent drag-and-drop library
- **React Team** - Amazing framework
- **FastAPI Team** - Great backend framework