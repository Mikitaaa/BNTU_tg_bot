"""
Основной модуль телеграм бота помощника по общежитию БНТУ
"""
from telegram.ext import Application, MessageHandler, CommandHandler, CallbackQueryHandler, filters
import logging
import os
from handlers import start_command, callback_handler, message_handler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получение токена из переменных окружения
bot_token = os.environ.get('BOT_TOKEN')
if not bot_token:
    raise ValueError("❌ BOT_TOKEN не задан в переменных окружения")

def main():
    """Основная функция запуска бота"""
    # Создание приложения
    application = Application.builder().token(bot_token).build()
    
    # Регистрация обработчиков
    # Команды
    application.add_handler(CommandHandler("start", start_command))
    
    # Callback кнопки
    application.add_handler(CallbackQueryHandler(callback_handler))
    
    # Текстовые сообщения (последний обработчик)
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        message_handler
    ))
    
    logger.info("🤖 Бот запущен и готов к работе")
    
    # Запуск полинга
    application.run_polling(allowed_updates=["message", "callback_query"])

if __name__ == '__main__':
    main()
