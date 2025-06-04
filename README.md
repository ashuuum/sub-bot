## Установка и запуск бота

Скачать проект:
```
git clone https://github.com/ashuuum/sub-bot.git
```

Установить виртуальное окружение и активировать его:
```
python3 -m venv .venv
source .venv/bin/activate
```

Установить зависимотсти:
```
pip install -r requirements.txt
```

Скопировать пример файла с переменной окружения:
```
сp .env.example .env
```

Вставить токен своего бота в файл .env:
```
echo "API_TOKEN=<your_token>" > .env
```

Запустить бота:
```
python3 main.py
```
