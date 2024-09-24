# Подсчёт корейских слов в выгруженных карточках Anki.

## Установка

1. Создай и активируй виртуальное окружение 
```bash
python3 -m venv .venv
. ./.venv/bin/activate.sh
```

2. Установи зависимости
```bash
pip3 -r requirements.txt
```

## Запуск
1. Выгрузи карточки из Anki в текстовом формате.

2. Запусти скрипт`count.py deck1.txt dec2.txt ...`

Скрипт выведет, сколько в каточках найдено различных слов с учётом морфологии.

# Примечание

Вообще говоря, этот скрипт работает с любыми тестовыми файлами, не только с выгруженными карточками Анки.
Например, можно посчитать все уникальные слова в корейском переводе "Гарри Поттера" ;)

# Примечание 2

Дефолтный анализатор `Hannanum` работает медленно и сильно ошибается. Поэтому результаты получаются 
сильно приблизительные. Анализатор `mecab` считает гораздо лучше, но у него сложная настройка. 
Пока в ветке `dev/use-mecab`.