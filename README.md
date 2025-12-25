# 59_school — локальный проект

Инструкции для запуска разработки и админки.

Запуск сервисов (Windows PowerShell):

1) Откройте PowerShell в корне репозитория и выполните:

```
.\run-dev.ps1
```

Это откроет два отдельных окна PowerShell: одно запустит фронтенд (в папке `front`) с `npm run dev`, другое — бэкенд (в папке `backend`) активирует виртуальное окружение `venv` и запустит `python manage.py runserver`.

2) Если вы хотите запускать вручную:
- Backend:
```
cd backend
.\venv\Scripts\Activate
python manage.py runserver
```
- Frontend:
```
cd front
npm install
npm run dev
```

Админ-панель Django доступна по адресу: http://127.0.0.1:8000/admin/ (создайте суперпользователя: `python manage.py createsuperuser`).

API:
- Certificates (achievements): http://127.0.0.1:8000/api/achievements/certificates/
- Content endpoints (новые): http://127.0.0.1:8000/api/content/
  - `hero-slides`, `stats`, `about`, `director`, `headers`, `contact`, `footers`, `pages`, `image-blocks`.

Примечания:
- Я не трогал приложение `achievements` и компонент `CertificateModal`.
- Для загрузки изображений используйте админку; медиа файлы обслуживаются Django в режиме DEBUG: `MEDIA_URL` = `/media/`, `MEDIA_ROOT` = `backend/media/`.

Если нужно — могу добавить примеры использования API на фронте или настроить более удобный WYSIWYG-редактор для страниц в админке.

