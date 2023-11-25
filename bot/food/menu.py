from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import datetime
from bot.conf import BASE_URL


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
    keyboard = [[InlineKeyboardButton(food['name'],callback_data=f"order-food-{food['id']}")] for food in menu['foods']]
    keyboard.append([InlineKeyboardButton("نوشیدنی‌ها 🥤",callback_data="show-beverages")])
    keyboard.append([InlineKeyboardButton("دسر ها 🍧",callback_data="show-desserts")])
    

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup