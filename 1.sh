#!/bin/bash

# 1. Покупка валюты (Наличка)
python3 -B main.py add "Покупка 2000 ¥ (курс 11.93)" 23860 -t TRANSFER -p "Наличка" -d "2025-10-14" --tags "Notion,БТ-Отдых"
python3 -B main.py add "Покупка 4000 ¥ (курс 11.7)" 46800 -t TRANSFER -p "Наличка" -d "2025-10-15" --tags "Notion,БТ-Отдых"

# 2. Снятие/Покупка валюты (РСХБ)
python3 -B main.py add "Покупка-снятие 5000 ¥" 60007 -t TRANSFER -p "РСХБ" -d "2025-11-01" --tags "Notion,БТ-Отдых"
python3 -B main.py add "Покупка 200 HKD" 2381 -t TRANSFER -p "РСХБ" -d "2025-11-04" --tags "Notion,БТ-Отдых"

# 3. Отели и билеты (Основные траты)
python3 -B main.py add "Отели Макао, Гонконг, Шеньжень" 8962 -t SPEND -p "Сбер" --cat "Hotels" -d "2025-11-07" --tags "Notion,БТ-Отдых,Логистика"
python3 -B main.py add "Покупка 1 билета" 124334 -t SPEND -p "Альфа" --cat "Travel" -d "2025-10-09" --tags "Notion,БТ 2025"
python3 -B main.py add "Покупка отеля Intercontinental" 40246.08 -t SPEND -p "РСХБ" --cat "Hotels" -d "2025-10-09" --tags "Notion,БТ 2025"
python3 -B main.py add "1 отель (3150 RMB)" 37730.7 -t SPEND -p "РСХБ" --cat "Hotels" -d "2025-10-09" --tags "Notion,БТ 2025"

# 4. Внутренние переводы между счетами (Пары)
# Входящий на РСХБ
python3 -B main.py add "Перевод на 1 покупку отелей со сбера" 78330 -t TRANSFER -p "РСХБ" -d "2025-10-09" --tags "Notion,БТ 2025"
# Исходящий со Сбера
python3 -B main.py add "Перевод на 1 покупку отелей на юнион пей" 78330 -t TRANSFER -p "Сбер" -d "2025-10-09" --tags "Notion,БТ 2025"

# Входящий на Альфу
python3 -B main.py add "Перевод на покупку 1 билета со сбера" 150000 -t TRANSFER -p "Альфа" -d "2025-10-09" --tags "Notion,БТ 2025"
# Исходящий со Сбера
python3 -B main.py add "Перевел на покупку первого билета БТ на альфу" 150000 -t TRANSFER -p "Сбер" -d "2025-10-09" --tags "Notion,БТ 2025"

# 5. Аванс (Приход)
python3 -B main.py add "Аванс на БТ" 614303 -t INCOME -p "Сбер" -d "2025-10-08" --tags "Notion,БТ 2025"

# 6. Логистика (Поезда и Самолеты)
python3 -B main.py add "Поезд Шанхай-Шанжао" 4520 -t SPEND -p "Тинькофф" --cat "Transportation" -d "2025-10-25" --tags "Notion,БТ-Отдых,Логистика"
python3 -B main.py add "Поезд Шанжао-Ханчжоу" 2043 -t SPEND -p "Тинькофф" --cat "Transportation" -d "2025-10-24" --tags "Notion,БТ-Отдых,Логистика"
python3 -B main.py add "Поезд Ханчжо-Шанхай" 1057 -t SPEND -p "Тинькофф" --cat "Transportation" -d "2025-10-24" --tags "Notion,БТ-Отдых,Логистика"
python3 -B main.py add "Самолет Шанхай-Макао" 8879 -t SPEND -p "Тинькофф" --cat "Transportation" -d "2025-10-29" --tags "Notion,БТ-Отдых,Логистика"
python3 -B main.py add "Самолет Гонконг-Шанхай" 7028 -t SPEND -p "Тинькофф" --cat "Transportation" -d "2025-10-29" --tags "Notion,БТ-Отдых,Логистика"

# 7. Траты в RMB (Записаны как рублевый эквивалент с места "RMB Наличка")
python3 -B main.py add "Пекин (534 RMB)" 6343 -t SPEND -p "RMB Наличка" --cat "Travel" -d "2025-10-15" --tags "Notion,БТ-Отдых"
python3 -B main.py add "Симка (200 RMB)" 2375 -t SPEND -p "RMB Наличка" --cat "Communications" -d "2025-10-15" --tags "Notion,БТ-Отдых"

# Перевод (видимо, пополнение RMB налички)
python3 -B main.py add "Наличка RMB 5000" 59394 -t TRANSFER -p "RMB Наличка" -d "2025-10-15" --tags "Notion,БТ-Отдых"

# Покупки и прочее
python3 -B main.py add "UNIQLO (RMB 160)" 1900 -t SPEND -p "RMB Наличка" --cat "Shopping" -d "2025-11-09" --tags "Notion,БТ-Отдых"
python3 -B main.py add "Траты на остальное - Сводка остатка налички RMB (30270)" 18506 -t SPEND -p "RMB Наличка" --cat "General" -d "2025-11-12" --tags "Notion,БТ-Отдых"

# Перевод на Alipay
python3 -B main.py add "Alipay RMB 6000" 71272 -t TRANSFER -p "Alipay" -d "2025-10-15" --tags "Notion,БТ-Отдых"

python3 -B main.py add "Никита (Маша) вернул Хайкоу" 31.20 -t RETURNED -p "Alipay" -c CNY -r 11.8788 -d "2025-10-13 15:28:00" --tags "Возврат мне,import"

