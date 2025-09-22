import { useEffect, useState } from 'react';

const useTelegramWebApp = () => {
  const [webApp, setWebApp] = useState(null);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const tg = window.Telegram?.WebApp;
    if (tg) {
      tg.ready();
      setWebApp(tg);
      setUser(tg.initDataUnsafe?.user);

      // Устанавливаем тему в соответствии с темой Telegram
      document.documentElement.className = tg.colorScheme;
      
      // Настраиваем главное меню
      tg.MainButton.setParams({
        text: 'Добавить задачу',
        color: '#0088cc',
      });
    }
  }, []);

  return { webApp, user };
};

export default useTelegramWebApp;