import logging
from datetime import time
from telegram import Update
from telegram.ext import JobQueue
from bot.application import application 
from bot.handlers import handlers
from food.menu import get_menu_text





logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)


def send_menu(context):
    chat_id = 1002037948543
    menu_text = get_menu_text()
    context.bot.send_message(chat_id=chat_id, text=menu_text)

def setup_queue():
    job_queue = JobQueue()
    job_queue.set_dispatcher(application.dispatcher)
    job_queue.run_daily(send_menu, time(hour=23, minute=57, second=0))
    job_queue.start()

    
def main() -> None:
    """Start the bot."""
    application.add_handlers(handlers)
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    

if __name__ == "__main__":
    main()