import json,datetime,requests
from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import CommandHandler,ContextTypes


async def start(update :Update, context : ContextTypes.DEFAULT_TYPE):
    welcome_message = "Welcome to LunchBot! \n\nI'am here to help you to order your lunch. \n\nif want to see the menu, please type \n/menu" 
    await update.message.reply_text(welcome_message)

   
    
def get_menu_json(day = None):
    if day == None:
        day = datetime.datetime.today().strftime('%a').upper()
    # url = f'http://localhost:8000/api/v1/daily_menus/{day}'
    url = f'http://localhost:8000/api/v1/daily_menus/MON'
    headers = {
        'Content-Type': 'application/json',
        'company':'BASA',
        }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Error: API request unsuccessful.")
    print(response)
    data = response.json()
    return data

def get_menu_markup():
    menu = get_menu_json()
    keyboard = [[InlineKeyboardButton(food_name,callback_data="1")] for food_name in menu['foods']]
    
    keyboard.append([InlineKeyboardButton("نوشیدنی‌ها",callback_data="Bevarages")])
    keyboard.append([InlineKeyboardButton("دسر",callback_data="Desserts")])
    keyboard.append([InlineKeyboardButton("منوی اصلی ⬅️",callback_data="back")])
    

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup
    

async def menu(update :Update, context : ContextTypes.DEFAULT_TYPE):
    menu_markup = get_menu_markup()
    await update.message.reply_text("menu:", reply_markup=menu_markup)

 

handlers =[
    CommandHandler("start",start),
    CommandHandler("menu",menu),
    
]