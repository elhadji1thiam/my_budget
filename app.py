from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db():
    db = sqlite3.connect('budget.db')
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS expenses
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT,
                   amount REAL,
                   date TEXT)''')
    db.execute('''CREATE TABLE IF NOT EXISTS incomes
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT,
                   amount REAL,
                   date TEXT)''')
    db.commit()

@app.route('/')
def index():
    db = get_db()
    expenses = db.execute("SELECT * FROM expenses ORDER BY date DESC").fetchall()
    incomes = db.execute("SELECT * FROM incomes ORDER BY date DESC").fetchall()
    
    total_expenses = sum(expense['amount'] for expense in expenses)
    total_incomes = sum(income['amount'] for income in incomes)
    balance = total_incomes - total_expenses
    
    return render_template('index.html', expenses=expenses, incomes=incomes,
                           total_expenses=total_expenses, total_incomes=total_incomes,
                           balance=balance)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    title = request.form['title']
    amount = float(request.form['amount'])
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    db = get_db()
    db.execute("INSERT INTO expenses (title, amount, date) VALUES (?, ?, ?)",
               (title, amount, date))
    db.commit()
    return redirect(url_for('index'))

@app.route('/add_income', methods=['POST'])
def add_income():
    title = request.form['title']
    amount = float(request.form['amount'])
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    db = get_db()
    db.execute("INSERT INTO incomes (title, amount, date) VALUES (?, ?, ?)",
               (title, amount, date))
    db.commit()
    return redirect(url_for('index'))

@app.route('/delete_expense/<int:id>', methods=['POST'])
def delete_expense(id):
    db = get_db()
    db.execute("DELETE FROM expenses WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for('index'))

@app.route('/delete_income/<int:id>', methods=['POST'])
def delete_income(id):
    db = get_db()
    db.execute("DELETE FROM incomes WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for('index'))

@app.route('/add_expense_page')
def add_expense_page():
    return render_template('add_expense_page.html')

@app.route('/add_income_page')
def add_income_page():
    return render_template('add_income_page.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
