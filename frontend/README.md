# Vectora Frontend

React frontend for Vectora task management system with Telegram Mini App integration.

## Features

- Task management (CRUD operations)
- Calendar view
- Task filters and sorting
- Telegram WebApp theming
- Responsive design

## Stack

- React
- Telegram WebApp API
- React Icons
- CSS Modules

## Setup

```bash
npm install
```

## Configuration

Create `.env.production`:
```
REACT_APP_API_URL=https://vectora-backend.up.railway.app
```

## Development

```bash
npm start
```

Runs on `http://localhost:3000`

## Build

```bash
npm run build
```

## Deploy to GitHub Pages

```bash
npm run deploy
```

## Project Structure

```
src/
  App.jsx                  # Main application component
  components/
    AddTaskModal.jsx       # Create task modal
    EditTaskModal.jsx      # Edit task modal
    TaskList.jsx           # Task list view
    CalendarView.jsx       # Calendar view
    ThemeSwitcher.jsx      # Theme toggle
  hooks/
    useTelegramWebApp.js   # Telegram WebApp hook
```

## Telegram Integration

The app uses Telegram WebApp API for:
- Authentication (initData)
- Theme detection
- Native popups and alerts
