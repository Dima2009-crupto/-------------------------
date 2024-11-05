from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect('tours.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        tour TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

init_db()  


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tours')
def tours():
    tours_list = [
        {"name": "Тур в Карпати", "description": "Неймовірна подорож до Карпат", "price": "5000 грн"},
        {"name": "Тур до Львова", "description": "Вихідні у Львові", "price": "3000 грн"}
    ]
    return render_template('tours.html', tours=tours_list)


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        tour = request.form['tour']

        conn = sqlite3.connect('tours.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bookings (name, email, tour) VALUES (?, ?, ?)", (name, email, tour))
        conn.commit()
        conn.close()

        return redirect(url_for('confirm'))

    selected_tour = request.args.get('tour', 'Тур не обрано')
    return render_template('booking.html', tour=selected_tour)


@app.route('/confirm')
def confirm():
    return render_template('confirm.html')

if __name__ == '__main__':
    app.run(debug=True)
