from flask import Flask, request, redirect, render_template
import sqlite3
import string
import random
from bs4 import BeautifulSoup

app = Flask(__name__)

def generate_short_id (num_of_chars: int):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=num_of_chars))

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute(''' CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY,  original_url TEXT NOT NULL, short_id TEXT NOT NULL UNIQUE)''')

    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        short_id = generate_short_id(6)

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO urls (original_url, short_id) VALUES (?, ?)", (url, short_id))
        conn.commit()
        conn.close()

        # Abre arquivo HTML
        with open('templates/index.html', 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # Encontra o elemento onde será acrescentada informação
        elemento = soup.find('body')

        # Adiciona novo conteúdo ao elemento
        new_url = soup.new_tag('a')
        new_url['href'] = f"/{short_id}"
        new_url.string = f'http://localhost:5000/{short_id}'

        # Insere o link no elemento pai
        elemento.append(new_url)
        elemento.append(soup.new_tag('br'))
        
        # Salvas alterações
        with open('templates/index.html', 'w') as f:
            f.write(soup.prettify())

    
    return render_template('index.html')

@app.route('/<short_id>')
def riderect_url(short_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('SELECT original_url FROM urls WHERE short_id = ?', (short_id,))
    row = cursor.fetchone()
    conn.close

    if row:
        return redirect(row[0])
    else:
        return '<h1>URL não encontrada</h1>'
    
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
