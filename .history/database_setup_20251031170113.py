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


# Departments table
cursor.execute("""
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dept_name TEXT
)
""")

# Projects table
cursor.execute("""
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    department_id INTEGER,
    budget INTEGER,
    FOREIGN KEY(department_id) REFERENCES departments(id)
)
""")

# Sample Data
departments = [('IT',), ('HR',), ('Finance',), ('Marketing',)]
cursor.executemany("INSERT INTO departments (dept_name) VALUES (?)", departments)

projects = [
    ('AI Chatbot', 1, 100000),
    ('Recruitment System', 2, 50000),
    ('Expense Tracker', 3, 75000),
    ('Campaign Analyzer', 4, 60000)
]
cursor.executemany("INSERT INTO projects (name, department_id, budget) VALUES (?, ?, ?)", projects)

employees = [
    ('Aisha', 1, 'Developer', 60000, '2022-04-15'),
    ('Rahul', 2, 'Manager', 75000, '2021-08-20'),
    ('Deepa', 3, 'Analyst', 55000, '2023-02-01'),
    ('Salih', 1, 'Data Engineer', 70000, '2022-01-10'),
    ('Ananya', 4, 'Executive', 50000, '2023-03-11'),
]
cursor.executemany("INSERT INTO employees (name, department_id, role, salary, joining_date) VALUES (?, ?, ?, ?, ?)", employees)

conn.commit()
conn.close()

print("✅ Extended database with departments and projects tables!")
