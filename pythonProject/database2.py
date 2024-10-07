import sqlite3

# Функція для створення таблиць у базі даних
def create_tables():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY,
                name TEXT,
                address TEXT,
                phone TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT,
                position TEXT,
                phone TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                client_id INTEGER,
                description TEXT,
                status TEXT,
                FOREIGN KEY(client_id) REFERENCES clients(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY,
                client_id INTEGER,
                amount REAL,
                date TEXT,
                FOREIGN KEY(client_id) REFERENCES clients(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS tariffs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                speed TEXT,
                price REAL)''')

    conn.commit()
    conn.close()

# Функції для роботи з клієнтами
def add_client(name, address, phone):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO clients (name, address, phone) VALUES (?, ?, ?)", (name, address, phone))
    conn.commit()
    conn.close()

def get_clients():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM clients")
    clients = c.fetchall()
    conn.close()
    return clients

def update_client(client_id, name, address, phone):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE clients SET name=?, address=?, phone=? WHERE id=?", (name, address, phone, client_id))
    conn.commit()
    conn.close()

def delete_client(client_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM clients WHERE id=?", (client_id,))
    conn.commit()
    conn.close()

# Функції для роботи зі співробітниками
def add_employee(name, position, phone):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO employees (name, position, phone) VALUES (?, ?, ?)", (name, position, phone))
    conn.commit()
    conn.close()

def get_employees():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM employees")
    employees = c.fetchall()
    conn.close()
    return employees

def update_employee(employee_id, name, position, phone):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE employees SET name=?, position=?, phone=? WHERE id=?", (name, position, phone, employee_id))
    conn.commit()
    conn.close()

def delete_employee(employee_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM employees WHERE id=?", (employee_id,))
    conn.commit()
    conn.close()

# Функції для роботи з замовленнями
def add_order(client_id, description, status):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO orders (client_id, description, status) VALUES (?, ?, ?)", (client_id, description, status))
    conn.commit()
    conn.close()

def get_orders():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM orders")
    orders = c.fetchall()
    conn.close()
    return orders

def update_order(order_id, client_id, description, status):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE orders SET client_id=?, description=?, status=? WHERE id=?", (client_id, description, status, order_id))
    conn.commit()
    conn.close()

def delete_order(order_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM orders WHERE id=?", (order_id,))
    conn.commit()
    conn.close()

# Функції для роботи з оплатами
def add_payment(client_id, amount, date):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO payments (client_id, amount, date) VALUES (?, ?, ?)", (client_id, amount, date))
    conn.commit()
    conn.close()

def get_payments():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM payments")
    payments = c.fetchall()
    conn.close()
    return payments

def delete_payment(payment_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM payments WHERE id=?", (payment_id,))
    conn.commit()
    conn.close()

# Функції для роботи з тарифами
def add_tariff(name, speed, price):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO tariffs (name, speed, price) VALUES (?, ?, ?)", (name, speed, price))
    conn.commit()
    conn.close()

def get_tariffs():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tariffs")
    tariffs = c.fetchall()
    conn.close()
    return tariffs

def update_tariff(tariff_id, name, speed, price):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE tariffs SET name=?, speed=?, price=? WHERE id=?", (name, speed, price, tariff_id))
    conn.commit()
    conn.close()

def delete_tariff(tariff_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM tariffs WHERE id=?", (tariff_id,))
    conn.commit()
    conn.close()

# Ініціалізація таблиць при імпорті файлу
create_tables()
