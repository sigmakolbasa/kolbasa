import telebot
from telebot import types
import database2 as db
import traceback

API_TOKEN = '6845936606:AAFXoqExHdThpMpXeJ2fJ06saERdS1fkIaw'
bot = telebot.TeleBot(API_TOKEN)

def create_main_menu():
    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(text="Клієнти", callback_data="clients_menu"),
        types.InlineKeyboardButton(text="Працівники", callback_data="employees_menu"),
        types.InlineKeyboardButton(text="Замовлення", callback_data="orders_menu"),
        types.InlineKeyboardButton(text="Оплати", callback_data="payments_menu"),
        types.InlineKeyboardButton(text="Тарифи", callback_data="tariffs_menu")
    ]
    markup.add(*buttons)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    show_main_menu(message)

def show_main_menu(message):
    markup = create_main_menu()
    bot.send_message(message.chat.id, "Виберіть категорію:", reply_markup=markup)

# Підменю для клієнтів
def create_clients_menu():
    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(text="Список клієнтів", callback_data="list_clients"),
        types.InlineKeyboardButton(text="Додати клієнта", callback_data="add_client"),
        types.InlineKeyboardButton(text="Видалити клієнта", callback_data="delete_client"),
        types.InlineKeyboardButton(text="Оновити дані клієнта", callback_data="update_client"),
        types.InlineKeyboardButton(text="Назад", callback_data="main_menu")
    ]
    markup.add(*buttons)
    return markup

@bot.callback_query_handler(func=lambda call: call.data == 'clients_menu')
def callback_clients_menu(call):
    markup = create_clients_menu()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Меню клієнтів:", reply_markup=markup)

# Підменю для працівників
def create_employees_menu():
    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(text="Список працівників", callback_data="list_employees"),
        types.InlineKeyboardButton(text="Додати працівника", callback_data="add_employee"),
        types.InlineKeyboardButton(text="Видалити працівника", callback_data="delete_employee"),
        types.InlineKeyboardButton(text="Оновити дані працівника", callback_data="update_employee"),
        types.InlineKeyboardButton(text="Назад", callback_data="main_menu")
    ]
    markup.add(*buttons)
    return markup

@bot.callback_query_handler(func=lambda call: call.data == 'employees_menu')
def callback_employees_menu(call):
    markup = create_employees_menu()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Меню працівників:", reply_markup=markup)

# Підменю для замовлень
def create_orders_menu():
    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(text="Список замовлень", callback_data="list_orders"),
        types.InlineKeyboardButton(text="Додати замовлення", callback_data="add_order"),
        types.InlineKeyboardButton(text="Видалити замовлення", callback_data="delete_order"),
        types.InlineKeyboardButton(text="Оновити дані замовлення", callback_data="update_order"),
        types.InlineKeyboardButton(text="Назад", callback_data="main_menu")
    ]
    markup.add(*buttons)
    return markup

@bot.callback_query_handler(func=lambda call: call.data == 'orders_menu')
def callback_orders_menu(call):
    markup = create_orders_menu()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Меню замовлень:", reply_markup=markup)

# Підменю для оплат
def create_payments_menu():
    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(text="Список оплат", callback_data="list_payments"),
        types.InlineKeyboardButton(text="Додати оплату", callback_data="add_payment"),
        types.InlineKeyboardButton(text="Видалити оплату", callback_data="delete_payment"),
        types.InlineKeyboardButton(text="Назад", callback_data="main_menu")
    ]
    markup.add(*buttons)
    return markup

@bot.callback_query_handler(func=lambda call: call.data == 'payments_menu')
def callback_payments_menu(call):
    markup = create_payments_menu()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Меню оплат:", reply_markup=markup)

# Підменю для тарифів
def create_tariffs_menu():
    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(text="Список тарифів", callback_data="list_tariffs"),
        types.InlineKeyboardButton(text="Додати тариф", callback_data="add_tariff"),
        types.InlineKeyboardButton(text="Видалити тариф", callback_data="delete_tariff"),
        types.InlineKeyboardButton(text="Оновити дані тарифу", callback_data="update_tariff"),
        types.InlineKeyboardButton(text="Назад", callback_data="main_menu")
    ]
    markup.add(*buttons)
    return markup

@bot.callback_query_handler(func=lambda call: call.data == 'tariffs_menu')
def callback_tariffs_menu(call):
    markup = create_tariffs_menu()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Меню тарифів:", reply_markup=markup)

# Обробники для кожної з функцій меню

# Клієнти
@bot.callback_query_handler(func=lambda call: call.data == 'list_clients')
def list_clients(call):
    clients = db.get_clients()
    response = "\n".join([f"ID: {client[0]}, Ім'я: {client[1]}, Адреса: {client[2]}, Телефон: {client[3]}" for client in clients])
    bot.send_message(call.message.chat.id, response if response else "Немає клієнтів.", reply_markup=create_main_menu())

@bot.callback_query_handler(func=lambda call: call.data == 'add_client')
def add_client(call):
    msg = bot.send_message(call.message.chat.id, "Введіть ім'я клієнта:")
    bot.register_next_step_handler(msg, process_add_client_name_step)

def process_add_client_name_step(message):
    name = message.text
    msg = bot.send_message(message.chat.id, "Введіть адресу клієнта:")
    bot.register_next_step_handler(msg, lambda m: process_add_client_address_step(m, name))

def process_add_client_address_step(message, name):
    address = message.text
    msg = bot.send_message(message.chat.id, "Введіть телефон клієнта:")
    bot.register_next_step_handler(msg, lambda m: process_add_client_phone_step(m, name, address))

def process_add_client_phone_step(message, name, address):
    phone = message.text
    db.add_client(name, address, phone)
    bot.send_message(message.chat.id, "Клієнт доданий.", reply_markup=create_main_menu())

@bot.callback_query_handler(func=lambda call: call.data == 'delete_client')
def delete_client(call):
    msg = bot.send_message(call.message.chat.id, "Введіть ID клієнта для видалення:")
    bot.register_next_step_handler(msg, process_delete_client_step)

def process_delete_client_step(message):
    client_id = int(message.text)
    db.delete_client(client_id)
    bot.send_message(message.chat.id, "Клієнт видалений.", reply_markup=create_main_menu())

@bot.callback_query_handler(func=lambda call: call.data == 'update_client')
def update_client(call):
    msg = bot.send_message(call.message.chat.id, "Введіть ID клієнта для оновлення:")
    bot.register_next_step_handler(msg, process_update_client_id_step)

def process_update_client_id_step(message):
    client_id = int(message.text)
    msg = bot.send_message(message.chat.id, "Введіть нове ім'я клієнта:")
    bot.register_next_step_handler(msg, lambda m: process_update_client_name_step(m, client_id))

def process_update_client_name_step(message, client_id):
    name = message.text
    msg = bot.send_message(message.chat.id, "Введіть нову адресу клієнта:")
    bot.register_next_step_handler(msg, lambda m: process_update_client_address_step(m, client_id, name))

def process_update_client_address_step(message, client_id, name):
    address = message.text
    msg = bot.send_message(message.chat.id, "Введіть новий телефон клієнта:")
    bot.register_next_step_handler(msg, lambda m: process_update_client_phone_step(m, client_id, name, address))

def process_update_client_phone_step(message, client_id, name, address):
    phone = message.text
    db.update_client(client_id, name, address, phone)
    bot.send_message(message.chat.id, "Дані клієнта оновлені.", reply_markup=create_main_menu())

# Працівники
@bot.callback_query_handler(func=lambda call: call.data == 'list_employees')
def list_employees(call):
    employees = db.get_employees()
    response = "\n".join([f"ID: {employee[0]}, Ім'я: {employee[1]}, Посада: {employee[2]}, Зарплата: {employee[3]}" for employee in employees])
    bot.send_message(call.message.chat.id, response if response else "Немає працівників.", reply_markup=create_main_menu())

@bot.callback_query_handler(func=lambda call: call.data == 'add_employee')
def add_employee(call):
    msg = bot.send_message(call.message.chat.id, "Введіть ім'я працівника:")
    bot.register_next_step_handler(msg, process_add_employee_name_step)

def process_add_employee_name_step(message):
    name = message.text
    msg = bot.send_message(message.chat.id, "Введіть посаду працівника:")
    bot.register_next_step_handler(msg, lambda m: process_add_employee_position_step(m, name))

def process_add_employee_position_step(message, name):
    position = message.text
    msg = bot.send_message(message.chat.id, "Введіть зарплату працівника:")
    bot.register_next_step_handler(msg, lambda m: process_add_employee_salary_step(m, name, position))

def process_add_employee_salary_step(message, name, position):
    salary = message.text
    db.add_employee(name, position, salary)
    bot.send_message(message.chat.id, "Працівник доданий.", reply_markup=create_main_menu())

@bot.callback_query_handler(func=lambda call: call.data == 'delete_employee')
def delete_employee(call):
    msg = bot.send_message(call.message.chat.id, "Введіть ID працівника для видалення:")
    bot.register_next_step_handler(msg, process_delete_employee_step)

def process_delete_employee_step(message):
    employee_id = int(message.text)
    db.delete_employee(employee_id)
    bot.send_message(message.chat.id, "Працівник видалений.", reply_markup=create_main_menu())

@bot.callback_query_handler(func=lambda call: call.data == 'update_employee')
def update_employee(call):
    msg = bot.send_message(call.message.chat.id, "Введіть ID працівника для оновлення:")
    bot.register_next_step_handler(msg, process_update_employee_id_step)

def process_update_employee_id_step(message):
    employee_id = int(message.text)
    msg = bot.send_message(message.chat.id, "Введіть нове ім'я працівника:")
    bot.register_next_step_handler(msg, lambda m: process_update_employee_name_step(m, employee_id))

def process_update_employee_name_step(message, employee_id):
    name = message.text
    msg = bot.send_message(message.chat.id, "Введіть нову посаду працівника:")
    bot.register_next_step_handler(msg, lambda m: process_update_employee_position_step(m, employee_id, name))

def process_update_employee_position_step(message, employee_id, name):
    position = message.text
    msg = bot.send_message(message.chat.id, "Введіть нову зарплату працівника:")
    bot.register_next_step_handler(msg, lambda m: process_update_employee_salary_step(m, employee_id, name, position))

def process_update_employee_salary_step(message, employee_id, name, position):
    salary = message.text
    db.update_employee(employee_id, name, position, salary)
    bot.send_message(message.chat.id, "Дані працівника оновлені.", reply_markup=create_main_menu())

# Замовлення
@bot.callback_query_handler(func=lambda call: call.data == 'list_orders')
def list_orders(call):
    orders = db.get_orders()
    response = "\n".join([f"ID: {order[0]}, Опис: {order[1]}, Клієнт: {order[2]}, Сума: {order[3]}" for order in orders])
    bot.send_message(call.message.chat.id, response if response else "Немає замовлень.", reply_markup=create_main_menu())

@bot.callback_query_handler(func=lambda call: call.data == 'add_order')
def add_order(call):
    msg = bot.send_message(call.message.chat.id, "Введіть опис замовлення:")
    bot.register_next_step_handler(msg, process_add_order_description_step)

def process_add_order_description_step(message):
    description = message.text
    msg = bot.send_message(message.chat.id, "Введіть ID клієнта:")
    bot.register_next_step_handler(msg, lambda m: process_add_order_client_id_step(m, description))

def process_add_order_client_id_step(message, description):
    client_id = message.text
    msg = bot.send_message(message.chat.id, "Введіть суму замовлення:")
    bot.register_next_step_handler(msg, lambda m: process_add_order_amount_step(m, description, client_id))

def process_add_order_amount_step(message, description, client_id):
    amount = message.text
    db.add_order(description, client_id, amount)
    bot.send_message(message.chat.id, "Замовлення додано.", reply_markup=create_main_menu())

@bot.callback_query_handler(func=lambda call: call.data == 'delete_order')
def delete_order(call):
    msg = bot.send_message(call.message.chat.id, "Введіть ID замовлення для видалення:")
    bot.register_next_step_handler(msg, process_delete_order_step)

def process_delete_order_step(message):
    order_id = int(message.text)
    db.delete_order(order_id)
    bot.send_message(message.chat.id, "Замовлення видалено.", reply_markup=create_main_menu())

@bot.callback_query_handler(func=lambda call: call.data == 'update_order')
def update_order(call):
    msg = bot.send_message(call.message.chat.id, "Введіть ID замовлення для оновлення:")
    bot.register_next_step_handler(msg, process_update_order_id_step)

def process_update_order_id_step(message):
    order_id = int(message.text)
    msg = bot.send_message(message.chat.id, "Введіть новий опис замовлення:")
    bot.register_next_step_handler(msg, lambda m: process_update_order_description_step(m, order_id))

def process_update_order_description_step(message, order_id):
    description = message.text
    msg = bot.send_message(message.chat.id, "Введіть новий ID клієнта:")
    bot.register_next_step_handler(msg, lambda m: process_update_order_client_id_step(m, order_id, description))

def process_update_order_client_id_step(message, order_id, description):
    client_id = message.text
    msg = bot.send_message(message.chat.id, "Введіть нову суму замовлення:")
    bot.register_next_step_handler(msg, lambda m: process_update_order_amount_step(m, order_id, description, client_id))

def process_update_order_amount_step(message, order_id, description, client_id):
    amount = message.text
    db.update_order(order_id, description, client_id, amount)
    bot.send_message(message.chat.id, "Дані замовлення оновлено.", reply_markup=create_main_menu())

# Оплати
@bot.callback_query_handler(func=lambda call: call.data == 'list_payments')
def list_payments(call):
    payments = db.get_payments()
    response = "\n".join([f"ID: {payment[0]}, Замовлення: {payment[1]}, Сума: {payment[2]}, Дата: {payment[3]}" for payment in payments])
    bot.send_message(call.message.chat.id, response if response else "Немає оплат.", reply_markup=create_main_menu())

@bot.callback_query_handler(func=lambda call: call.data == 'add_payment')
def add_payment(call):
    msg = bot.send_message(call.message.chat.id, "Введіть ID замовлення:")
    bot.register_next_step_handler(msg, process_add_payment_order_id_step)

def process_add_payment_order_id_step(message):
    order_id = message.text
    msg = bot.send_message(message.chat.id, "Введіть суму оплати:")
    bot.register_next_step_handler(msg, lambda m: process_add_payment_amount_step(m, order_id))

def process_add_payment_amount_step(message, order_id):
    amount = message.text
    db.add_payment(order_id, amount)
    bot.send_message(message.chat.id, "Оплату додано.", reply_markup=create_main_menu())

@bot.callback_query_handler(func=lambda call: call.data == 'delete_payment')
def delete_payment(call):
    msg = bot.send_message(call.message.chat.id, "Введіть ID оплати для видалення:")
    bot.register_next_step_handler(msg, process_delete_payment_step)

def process_delete_payment_step(message):
    payment_id = int(message.text)
    db.delete_payment(payment_id)
    bot.send_message(message.chat.id, "Оплату видалено.", reply_markup=create_main_menu())

# Тарифи
@bot.callback_query_handler(func=lambda call: call.data == 'list_tariffs')
def list_tariffs(call):
    tariffs = db.get_tariffs()
    response = "\n".join([f"ID: {tariff[0]}, Назва: {tariff[1]}, Ціна: {tariff[2]}, Опис: {tariff[3]}" for tariff in tariffs])
    bot.send_message(call.message.chat.id, response if response else "Немає тарифів.", reply_markup=create_main_menu())

@bot.callback_query_handler(func=lambda call: call.data == 'add_tariff')
def add_tariff(call):
    msg = bot.send_message(call.message.chat.id, "Введіть назву тарифу:")
    bot.register_next_step_handler(msg, process_add_tariff_name_step)

def process_add_tariff_name_step(message):
    name = message.text
    msg = bot.send_message(message.chat.id, "Введіть ціну тарифу:")
    bot.register_next_step_handler(msg, lambda m: process_add_tariff_price_step(m, name))

def process_add_tariff_price_step(message, name):
    price = message.text
    msg = bot.send_message(message.chat.id, "Введіть опис тарифу:")
    bot.register_next_step_handler(msg, lambda m: process_add_tariff_description_step(m, name, price))

def process_add_tariff_description_step(message, name, price):
    description = message.text
    db.add_tariff(name, price, description)
    bot.send_message(message.chat.id, "Тариф додано.", reply_markup=create_main_menu())

@bot.callback_query_handler(func=lambda call: call.data == 'delete_tariff')
def delete_tariff(call):
    msg = bot.send_message(call.message.chat.id, "Введіть ID тарифу для видалення:")
    bot.register_next_step_handler(msg, process_delete_tariff_step)

def process_delete_tariff_step(message):
    tariff_id = int(message.text)
    db.delete_tariff(tariff_id)
    bot.send_message(message.chat.id, "Тариф видалено.", reply_markup=create_main_menu())

@bot.callback_query_handler(func=lambda call: call.data == 'update_tariff')
def update_tariff(call):
    msg = bot.send_message(call.message.chat.id, "Введіть ID тарифу для оновлення:")
    bot.register_next_step_handler(msg, process_update_tariff_id_step)

def process_update_tariff_id_step(message):
    tariff_id = int(message.text)
    msg = bot.send_message(message.chat.id, "Введіть нову назву тарифу:")
    bot.register_next_step_handler(msg, lambda m: process_update_tariff_name_step(m, tariff_id))

def process_update_tariff_name_step(message, tariff_id):
    name = message.text
    msg = bot.send_message(message.chat.id, "Введіть нову ціну тарифу:")
    bot.register_next_step_handler(msg, lambda m: process_update_tariff_price_step(m, tariff_id, name))

def process_update_tariff_price_step(message, tariff_id, name):
    price = message.text
    msg = bot.send_message(message.chat.id, "Введіть новий опис тарифу:")
    bot.register_next_step_handler(msg, lambda m: process_update_tariff_description_step(m, tariff_id, name, price))

def process_update_tariff_description_step(message, tariff_id, name, price):
    description = message.text
    db.update_tariff(tariff_id, name, price, description)
    bot.send_message(message.chat.id, "Дані тарифу оновлено.", reply_markup=create_main_menu())

try:
    bot.infinity_polling()
except Exception as e:
    traceback.print_exc()
