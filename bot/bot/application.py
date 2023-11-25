import os
from telegram.ext import Application
BOT_TOKEN = os.environ.get("BOT_TOKEN")
application = Application.builder().token(BOT_TOKEN).build()