## Установка и запуск:
1.Клонировать репозиторий и перейти к проекту:
```
git clone https://github.com/shulikin/api_yatube.git && cd api_yatube
```
```
cd yatube_api
```
2.В корневой директории проекта создайте виртуальное окружение, используя команду:
- Если у вас windows
```
python -m venv venv
```
  или
```
py -3 -m venv venv
```
- Если у вас Linux/macOS
```
python3 -m venv venv.
```
3.Активируйте виртуальное окружение командой:
- Если у вас windows
```
source venv/Scripts/activate
```
- Если у вас Linux/macOS
```
source venv/bin/activate
```
4.Обновите менеджер пакетов:
```
python -m pip install --upgrade pip
```
5.Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
6.Выполнить миграции:
```
python manage.py migrate
```
7.Запустить проект:
```
python manage.py runserver
```