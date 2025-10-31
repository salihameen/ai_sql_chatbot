from flask import Flask, request, jsonify
import sqlite3
from nlp_to_sql import text_to_sql

DB_PATH = "data/chatbot.db"

app = Flask(__name__)

@app.route("/query", methods=["POST"])
def query():
    data = request.get_json() or {}
    text = data.get("text")
    if not text:
        return jsonify({"error":"No 'text' provided"}), 400

    sql = text_to_sql(text)

    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cols = [description[0] for description in cur.description] if cur.description else []
        results = [dict(zip(cols, row)) for row in rows]
        conn.commit()
        conn.close()
        return jsonify({"sql": sql, "results": results})
    except Exception as e:
        return jsonify({"error": str(e), "sql": sql}), 500

if __name__ == "__main__":
    app.run(debug=True)
