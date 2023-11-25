import logging 
from telegram import Update
from bot.application import application 
from bot.handlers import handlers



logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)


    
def main() -> None:
    """Start the bot."""
    application.add_handlers(handlers)
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    

if __name__ == "__main__":
    main()