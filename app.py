from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "fichas.db")

app = Flask(__name__)

def init_db():
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS entradas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_hora TEXT NOT NULL,
                quantidade INTEGER NOT NULL
            )
        """)
        conn.commit()

def registrar_ficha(qtd=1):
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO entradas (data_hora, quantidade) VALUES (?, ?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), int(qtd))
        )
        conn.commit()

@app.route("/api/ficha", methods=["POST"])
def api_ficha():
    data = request.get_json(silent=True) or {}
    qtd = data.get("fichas", 1)
    try:
        qtd = int(qtd)
        if qtd <= 0:
            return jsonify({"status": "erro", "msg": "fichas deve ser > 0"}), 400
    except (TypeError, ValueError):
        return jsonify({"status": "erro", "msg": "fichas inválido"}), 400

    registrar_ficha(qtd)
    return jsonify({"status": "ok", "fichas": qtd})

@app.route("/")
def index():
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()

        # Total de fichas (soma das quantidades)
        c.execute("SELECT COALESCE(SUM(quantidade), 0) FROM entradas")
        total = c.fetchone()[0] or 0

        # Últimos 10 registros (mostrando data e quantidade)
        c.execute("SELECT data_hora, quantidade FROM entradas ORDER BY id DESC LIMIT 10")
        ultimas = [{"data_hora": r[0], "quantidade": r[1]} for r in c.fetchall()]

        # Agrupado por dia (somatório)
        c.execute("""
            SELECT substr(data_hora,1,10) AS dia, COALESCE(SUM(quantidade), 0) AS total
            FROM entradas
            GROUP BY dia
            ORDER BY dia
        """)
        dados = [{"dia": r[0], "total": r[1]} for r in c.fetchall()]

    return render_template("index.html", total=total, ultimas=ultimas, resumo=dados)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
