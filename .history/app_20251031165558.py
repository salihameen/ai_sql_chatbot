from flask import Flask, request, jsonify
import sqlite3
from nlp_to_sql import text_to_sql
from nlp_to_sql import question_to_sql, summarize_result
import pandas as pd

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


@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')

    sql_query = question_to_sql(question)

    try:
        conn = sqlite3.connect("data/company.db")
        df = pd.read_sql_query(sql_query, conn)
        conn.close()

        summary = summarize_result(question, df)

        return jsonify({
            "sql_query": sql_query,
            "columns": df.columns.tolist(),
            "data": df.values.tolist(),
            "summary": summary
        })
    except Exception as e:
        return jsonify({"error": str(e), "sql_query": sql_query})
