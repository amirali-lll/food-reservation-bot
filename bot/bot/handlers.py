import json,datetime,requests,logging
from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import CommandHandler,ContextTypes,CallbackQueryHandler
from bot.conf import HOST,BASE_URL
from food.order import order,order_rice
from food.menu import get_menu_json,get_menu_markup,get_menu_text


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
    menu_text   = get_menu_text()
    await update.message.reply_text(menu_text,reply_markup=menu_markup)
    

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
    # show beverages 2 in a row
    beverages = menu['beverages']
    beverages = [beverages[i:i + 2] for i in range(0, len(beverages), 2)]
    keyboard = [[InlineKeyboardButton(f"{beverage['name']}",callback_data=f"order-beverage-{beverage['id']}") for beverage in beverage_row] for beverage_row in beverages]
    keyboard.append([InlineKeyboardButton("منوی اصلی ⬅️",callback_data="main-menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("لطفا نوشیدنی مورد نظر خود را انتخاب کنید👇👇👇",reply_markup=reply_markup)
    
    
async def main_menu(update :Update, context : ContextTypes.DEFAULT_TYPE):  
    query = update.callback_query
    await query.edit_message_text(get_menu_text(),reply_markup=get_menu_markup())
    

async def desserts_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try :
        dessert_id = int(query.data.split('-')[2])
        user = update.effective_user
        order_response = order(user,'dessert',dessert_id)
        await query.answer('ثبت شد')
    except Exception as e:
        print(e)
        await query.answer(f"سفارش ثبت نشد\n{e}",show_alert=True)
            
async def beverages_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try :
        beverage_id = int(query.data.split('-')[2])
        user = update.effective_user
        order(user,'beverage',beverage_id)
        await query.answer('ثبت شد')
    except Exception as e:
            await query.answer("متاسفانه سفارش شما ثبت نشد. لطفا مجددا تلاش کنید.",show_alert=True)
            
            
async def rice_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try :
        have_rice = query.data.split('-')[2]
        user = update.effective_user
        order_response = order_rice(user,have_rice)
        await query.answer('ثبت شد')
    except Exception as e:
        print(e)
        await query.answer(f"سفارش ثبت نشد\n{e}",show_alert=True)
        
        
async def show_foods(update :Update, context : ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    menu = get_menu_json()
    keyboard = [[InlineKeyboardButton(food['name'],callback_data=f"order-food-{food['id']}")] for food in menu['foods']]
    keyboard.append([InlineKeyboardButton("🍚✅برنج میخوام",callback_data=f"order-rice-True"),InlineKeyboardButton("🍚❎برنج نمیخوام",callback_data=f"order-rice-False")])
    keyboard.append([InlineKeyboardButton("منوی اصلی ⬅️",callback_data="main-menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("غذای خود را انتخاب کنید\nغذاهایی برنجی به صورت پیشفرض با برنج سفارش داده میشوند",reply_markup=reply_markup)
        


from telegram.error import BadRequest

async def refresh_menu(update :Update, context : ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    new_text = get_menu_text()
    new_markup = get_menu_markup()
    try:
        await query.edit_message_text(new_text, reply_markup=new_markup)
    except BadRequest as e:
        pass
    await query.answer('صفحه بازیابی شد')


    
        
 

handlers =[
    CommandHandler("start",start),
    CommandHandler("menu",menu),
    CallbackQueryHandler(food_button,pattern='^order-food-\d+$'),
    CallbackQueryHandler(show_desserts,pattern='^show-desserts$'),
    CallbackQueryHandler(show_beverages,pattern='^show-beverages$'),
    CallbackQueryHandler(main_menu,pattern='^main-menu$'),
    CallbackQueryHandler(desserts_button,pattern='^order-dessert-\d+$'),
    CallbackQueryHandler(beverages_button,pattern='^order-beverage-\d+$'),
    CallbackQueryHandler(rice_button,pattern='^order-rice-.*$'),
    CallbackQueryHandler(show_foods,pattern='^show-foods$'),
    CallbackQueryHandler(refresh_menu,pattern='^refresh-menu$'),
    
    
    
    
    
    
]