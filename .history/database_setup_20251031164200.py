import sqlite3

# Create DB connection
conn = sqlite3.connect("data/company.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    department TEXT,
    role TEXT,
    salary INTEGER,
    joining_date TEXT
)
""")

# Insert sample data
sample_data = [
    ('Aisha', 'IT', 'Developer', 60000, '2022-04-15'),
    ('Rahul', 'HR', 'Manager', 75000, '2021-08-20'),
    ('Deepa', 'Finance', 'Analyst', 55000, '2023-02-01'),
    ('Salih', 'IT', 'Data Engineer', 70000, '2022-01-10'),
    ('Ananya', 'Marketing', 'Executive', 50000, '2023-03-11'),
]

cursor.executemany("INSERT INTO employees (name, department, role, salary, joining_date) VALUES (?, ?, ?, ?, ?)", sample_data)

conn.commit()
conn.close()

print("✅ Database setup complete: data/company.db")
