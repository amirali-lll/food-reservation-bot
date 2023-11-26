from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import datetime
from food.order import get_today_orders
from bot.persaindate import get_today_in_persian
from bot.conf import BASE_URL


def get_menu_text():
    today_orders = get_today_orders()
    today = get_today_in_persian()
    starter = f" سلام صبح بخیر😁 .\n منوی روز {today}📅.\n لطفا غذای و دورچین مورد نظر خود را انتخاب کنید"
    text = "\n سفارشات امروز:\n\n"
    for order in today_orders:
        rice = 'با برنج' if order['rice'] else 'بدون برنج'
        food = order['food']['name']
        dessert = order['dessert']['name'] if order['dessert'] else 'بدون دسر'
        beverage = order['beverage']['name'] if order['beverage'] else 'بدون نوشیدنی'
        text += f"👤-سفارش {order['user']}:\n {food}({rice}) - {dessert} - {beverage}\n"
        
    return starter+text



def get_menu_json(day = None):
    if day == None:
        day = datetime.datetime.today().strftime('%a').upper()
    url = f'{BASE_URL}daily_menus/{day}'
    headers = {
        'Content-Type': 'application/json',
        'company':'BASA',
        }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Error: API request unsuccessful.\nresponse status code: " + str(response.status_code)+ "\nresponse: " + str(response.text))
    return response.json()

def get_menu_markup():
    menu = get_menu_json()
    keyboard = [[InlineKeyboardButton("نوشیدنی‌ها 🥤",callback_data="show-beverages"),InlineKeyboardButton("دسر ها 🍧",callback_data="show-desserts"),InlineKeyboardButton('غذا ها 🍛',callback_data="show-foods")]]
    keyboard.append([InlineKeyboardButton("♻️ بازیابی صفحه ♻️",callback_data="refresh-menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup