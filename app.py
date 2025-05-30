# app.py
from flask import Flask, request, render_template, redirect, url_for
import sqlite3, os, pickle
import config
from utils import insecure_hash

app = Flask(__name__)

# ——————————————————————————————
# Inicialización de la base de datos
# ——————————————————————————————
def init_db():
    import os as _os
    _os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect(config.DB_PATH)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
    # ► Inserta credenciales sin sanitizar
    c.execute(f"INSERT INTO users VALUES('{config.ADMIN_USER}', '{config.ADMIN_PASS}')")
    conn.commit()
    conn.close()

init_db()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect(config.DB_PATH)
    c = conn.cursor()
    # ► SQL Injection: construye la query directamente con f-string
    c.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
    user = c.fetchone()
    conn.close()
    if user:
        return redirect(url_for('dashboard', user=username))
    else:
        return "Invalid credentials", 401


@app.route('/dashboard')
def dashboard():
    user = request.args.get('user')
    # ► XSS: inserta sin escapar
    return render_template('result.html', user=user)


@app.route('/ping')
def ping_host():
    host = request.args.get('host', '')
    # ► Command Injection: shell=True implícito al usar os.popen
    output = os.popen('ping -c 4 ' + host).read()
    return f"<pre>{output}</pre>"


@app.route('/calc', methods=['POST'])
def calculate():
    expr = request.form['expr']
    # ► Code Injection: eval() sobre input del usuario
    result = eval(expr)
    return f"Result: {result}"


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    # ► Deserialización insegura: pickle.load() de archivo subido
    data = pickle.load(file)
    return f"Unpickled data: {data}"


if __name__ == '__main__':
    # ► debug=True activa recarga automática (pero también expone detalles en caso de error)
    app.run(debug=True)