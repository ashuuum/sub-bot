## Установка и запуск бота

Скачать проект:
```
git clone https://github.com/ashuuum/sub-bot.git
```

Установить виртуальное окружение:
```
python3 -m venv .venv
```

Активировать виртуальное окружение:
```
source .venv/bin/activate
```

Установить зависимотсти:
```
pip install -r requirements.txt
```

Создать файл *.env*, записав в него API токен своего бота (для привязки к проекту):
```
echo "API_TOKEN=<your_token>" > .env
```

Запустить бота:
```
python3 bot.py
```


## Подключение базы данных

В случае, если имеется база данных, положить ее перед запуском бота в каталог **./core**.

База данных должна называться **sub.db**