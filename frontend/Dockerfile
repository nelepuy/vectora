FROM node:20-alpine AS development

WORKDIR /app

# Копируем файлы package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем остальные файлы проекта
COPY . .

# Запускаем приложение в режиме разработки
ENV NODE_ENV=development
EXPOSE 3000
CMD ["npm", "start"]

# Сборка для продакшена
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Продакшен стадия
FROM nginx:alpine AS production

# Копируем собранные файлы из build стадии
COPY --from=build /app/build /usr/share/nginx/html

# Копируем конфигурацию nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
