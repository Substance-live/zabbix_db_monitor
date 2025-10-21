import csv
import psycopg2
import os

# ==============================
#  Настройки подключения
# ==============================
DB_HOST = "127.0.0.1"
DB_PORT = 5432
DB_NAME = "kurs_db"        # твоя база приложения
DB_USER = "admin"          # пользователь PostgreSQL
DB_PASS = "admin"          # пароль

# Определяем путь к текущему файлу (.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Указываем путь к CSV, который лежит рядом
CSV_FILE = os.path.join(BASE_DIR, "questions.csv")

BATCH_SIZE = 5000  # каждые N строк выводим лог

# ==============================
#  Подключение к базе
# ==============================
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)
cur = conn.cursor()

# ==============================
#  Создание таблицы
# ==============================
cur.execute("""
CREATE TABLE IF NOT EXISTS stackoverflow_questions (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP,
    link TEXT UNIQUE,
    question TEXT,
    tags TEXT[]
)
""")
conn.commit()
print("Таблица создана (или уже существует)")

# ==============================
#  Загрузка CSV с логированием
# ==============================
with open(CSV_FILE, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    count = 0
    for row in reader:
        datetime_val = row['date'].strip()
        if datetime_val.lower() == 'date' or not datetime_val:
            continue  # пропускаем строку с заголовком или пустую
        link_val = row['links']
        question_val = row['questions']
        tags_val = row['tags'].split(',') if row['tags'] else None

        cur.execute("""
        INSERT INTO stackoverflow_questions (datetime, link, question, tags)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (link) DO NOTHING
        """, (datetime_val, link_val, question_val, tags_val))

        count += 1
        if count % BATCH_SIZE == 0:
            conn.commit()  # фиксируем изменения пакетами
            print(f"{count} строк импортировано...")

# Финальный коммит
conn.commit()
cur.close()
conn.close()

print(f"Импорт CSV завершён! Всего импортировано строк: {count}")
