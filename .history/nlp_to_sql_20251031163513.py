import os

"""
Simple translator from natural language -> SQL.
- If OPENAI_API_KEY is set it will try to use OpenAI's completion API and return the model output (best-effort).
- Otherwise it falls back to a tiny rule-based mapper for a demo `employees` table.

Contract (simple):
- input: free-text question about the DB (string)
- output: a single SQL SELECT statement (string)

This is intentionally minimal. For production use, validate/parameterize SQL to avoid injection and ensure only read-only queries are executed.
"""

DB_SCHEMA_HINT = "employees(id INTEGER PRIMARY KEY, name TEXT, role TEXT, salary INTEGER, hired_date TEXT)"


def text_to_sql(text: str) -> str:
    """Return a SQL statement (best-effort) for the given natural-language text."""
    text = (text or "").strip()
    if not text:
        return "SELECT * FROM employees LIMIT 10;"

    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            import openai
            openai.api_key = openai_key
            prompt = (
                f"You are an assistant that converts a natural language question into a single SQL SELECT query. "
                f"Only output the SQL query and nothing else. Table schema: {DB_SCHEMA_HINT}\nQuestion: {text}\nSQL:"
            )
            # Use the Completion API if available, fallback gracefully
            resp = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=150,
                temperature=0,
                n=1,
            )
            sql = resp.choices[0].text.strip().strip('`')
            return sql
        except Exception:
            # If OpenAI call fails for any reason, fall back to rule-based mapper below
            pass

    # --- fallback simple rules ---
    t = text.lower()
    if "count" in t and "employee" in t:
        return "SELECT COUNT(*) AS count FROM employees;"
    if ("average" in t or "avg" in t) and "salary" in t:
        return "SELECT AVG(salary) AS avg_salary FROM employees;"
    if "names" in t or "list" in t or ("employees" in t and "who" in t):
        return "SELECT id, name, role, salary FROM employees;"
    if "highest salary" in t or ("max" in t and "salary" in t):
        return "SELECT * FROM employees ORDER BY salary DESC LIMIT 1;"
    if "hired" in t and "2020" in t:
        return "SELECT * FROM employees WHERE hired_date LIKE '2020-%';"

    # generic fallback
    return "SELECT * FROM employees LIMIT 10;"
