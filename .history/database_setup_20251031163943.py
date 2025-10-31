import sqlite3
import os

DB_PATH = "data/chatbot.db"

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS employees(
        id INTEGER PRIMARY KEY,
        name TEXT,
        role TEXT,
        salary INTEGER,
        hired_date TEXT
    )
    """
)

# Clear any existing rows for a reproducible demo
cur.execute("DELETE FROM employees")

sample = [
    ("Alice", "Engineer", 90000, "2020-01-15"),
    ("Bob", "Manager", 120000, "2019-07-23"),
    ("Carol", "Designer", 80000, "2021-05-10"),
    ("Dave", "Engineer", 95000, "2018-11-01"),
]

cur.executemany(
    "INSERT INTO employees(name, role, salary, hired_date) VALUES (?,?,?,?)",
    sample,
)

conn.commit()
conn.close()

print(f"Initialized database at {DB_PATH}")
