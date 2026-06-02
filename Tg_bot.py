from telegram.ext import Application, MessageHandler, CommandHandler, CallbackQueryHandler, filters
import logging
import os
from handlers import start_command, callback_handler, message_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

bot_token = os.environ.get('BOT_TOKEN')
if not bot_token:
    raise ValueError("❌ BOT_TOKEN не задан в переменных окружения")

def main():
    application = Application.builder().token(bot_token).build()
    
    application.add_handler(CommandHandler("start", start_command))
    
    application.add_handler(CallbackQueryHandler(callback_handler))
    
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        message_handler
    ))
    
    logger.info("🤖 Бот запущен и готов к работе")
    
    application.run_polling(allowed_updates=["message", "callback_query"])

if __name__ == '__main__':
    main()
