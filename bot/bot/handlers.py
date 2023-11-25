import json,datetime,requests,logging
from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import CommandHandler,ContextTypes,CallbackQueryHandler
from bot.conf import HOST,BASE_URL
from bot.persaindate import get_today_in_persian
from food.order import order 
from food.menu import get_menu_json,get_menu_markup


logger = logging.getLogger(__name__)

async def start(update :Update, context : ContextTypes.DEFAULT_TYPE):
    welcome_message = """
سلام👋👋

به باساناهار خوش‌اومدی 😎
این یه پروژه شخصی و تفریحیه که فعلا مختص شرکت باسا است و شاید بعدا در مقیاس بزرگتری استفاده بشه

اینجا میتونی با زدن /menu منو روزانه رو ببینی و غذاهای هر روز  رو چک کنی و سفارش بدی 😍
""" 
    await update.message.reply_text(welcome_message)


    

async def menu(update :Update, context : ContextTypes.DEFAULT_TYPE):
    await send_menu(update,context)
    
    
async def send_menu(update :Update, context : ContextTypes.DEFAULT_TYPE):
    menu_markup = get_menu_markup()
    today = get_today_in_persian()
    reply_message = f" سلام صبح بخیر😁 .\n منوی روز {today}📅.\n لطفا غذای و دورچین مورد نظر خود را انتخاب کنید👇👇👇"
    await update.message.reply_text(reply_message,reply_markup=menu_markup)
    

async def food_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try :
        food_id = int(query.data.split('-')[2])
        user = update.effective_user
        order(user,'food',food_id)
        await query.answer('ثبت شد')
    except Exception as e:
            await query.answer("متاسفانه سفارش شما ثبت نشد. لطفا مجددا تلاش کنید.",show_alert=True)
            
async def show_desserts(update :Update, context : ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    menu = get_menu_json()
    keyboard = [[InlineKeyboardButton(dessert['name'],callback_data=f"order-dessert-{dessert['id']}")] for dessert in menu['desserts']]
    keyboard.append([InlineKeyboardButton("منوی اصلی ⬅️",callback_data="main-menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("لطفا دسر مورد نظر خود را انتخاب کنید👇👇👇",reply_markup=reply_markup)
    
async def show_beverages(update :Update, context : ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    menu = get_menu_json()
    keyboard = [[InlineKeyboardButton(beverage['name'],callback_data=f"order-beverage-{beverage['id']}")] for beverage in menu['beverages']]
    keyboard.append([InlineKeyboardButton("منوی اصلی ⬅️",callback_data="main-menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("لطفا نوشیدنی مورد نظر خود را انتخاب کنید👇👇👇",reply_markup=reply_markup)
    
    
async def main_menu(update :Update, context : ContextTypes.DEFAULT_TYPE):  
    query = update.callback_query
    await query.edit_message_text("لطفا غذای و دورچین مورد نظر خود را انتخاب کنید👇👇👇",reply_markup=get_menu_markup())
    

def desserts_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try :
        dessert_id = int(query.data.split('-')[2])
        user = update.effective_user
        order(user,'dessert',dessert_id)
        query.answer('ثبت شد')
    except Exception as e:
            query.answer("متاسفانه سفارش شما ثبت نشد. لطفا مجددا تلاش کنید.",show_alert=True)
            
def beverages_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try :
        beverage_id = int(query.data.split('-')[2])
        user = update.effective_user
        order(user,'beverage',beverage_id)
        query.answer('ثبت شد')
    except Exception as e:
            query.answer("متاسفانه سفارش شما ثبت نشد. لطفا مجددا تلاش کنید.",show_alert=True)
        



    
        
 

handlers =[
    CommandHandler("start",start),
    CommandHandler("menu",menu),
    CallbackQueryHandler(food_button,pattern='^order-food-\d+$'),
    CallbackQueryHandler(show_desserts,pattern='^show-desserts$'),
    CallbackQueryHandler(show_beverages,pattern='^show-beverages$'),
    CallbackQueryHandler(main_menu,pattern='^main-menu$'),
    CallbackQueryHandler(desserts_button,pattern='^order-dessert-\d+$'),
    CallbackQueryHandler(beverages_button,pattern='^order-beverage-\d+$'),
    
    
    
    
]