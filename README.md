# django_sprint4
# Blogicum (Django)

Учебный проект на Django.

## Требования
- Python 3.10+ (у вас может быть 3.13 — тоже ок)
- Git (по желанию, для клонирования)
- SQLite используется по умолчанию (файл `db.sqlite3`)

## Установка и запуск (Windows / Linux / macOS)

### 1 Клонировать репозиторий и перейти в папку проекта
```bash
git clone <ваш_репозиторий>
cd blogicum
2) Создать и активировать виртуальное окружение
Windows (cmd / PowerShell):
Учебный проект на Django.

Требования:

Python 3.10+ (подойдет и 3.13)

SQLite (по умолчанию)

pip

Запуск проекта

Установка зависимостей
Создайте и активируйте виртуальное окружение, затем установите зависимости.

Windows:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Linux/macOS:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Применение миграций
python manage.py migrate

Заполнение базы данных
Загрузка тестовых данных из фикстуры:
python manage.py loaddata blog/fixtures/data.json

Запуск сервера
python manage.py runserver
Открыть в браузере: http://127.0.0.1:8000/

Админка

Создать суперпользователя:
python manage.py createsuperuser
Админка: http://127.0.0.1:8000/admin/

Проверка, что база заполнена
python manage.py shell -c "from blog.models import Post,Category,Comment; print(Post.objects.count(), Category.objects.count(), Comment.objects.count())"

Пересоздание базы (SQLite)
ВНИМАНИЕ: удалит локальную базу данных.

Windows:
del db.sqlite3
python manage.py migrate
python manage.py loaddata blog/fixtures/data.json

Linux/macOS:
rm -f db.sqlite3
python manage.py migrate
python manage.py loaddata blog/fixtures/data.json

Примечание (Windows / кодировка)
Если при создании фикстуры dumpdata появляется ошибка про charmap, используйте:
python -X utf8 manage.py dumpdata --indent 2 --exclude contenttypes --exclude auth.Permission --exclude admin.LogEntry --output blog/fixtures/data.json