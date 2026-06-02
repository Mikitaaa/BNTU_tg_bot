"""
Модуль обработчиков команд и callback кнопок
"""
import logging
from telegram import Update
from telegram.ext import CallbackContext
from keyboards import get_main_menu, get_dormitory_menu, get_back_button, get_yes_no_keyboard
from database import get_dormitory_info
from Text_generator import getTextResponse

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Маппинг callback данных на информацию
CALLBACK_MAPPING = {
    "dormitory_info": ("🏠 Информация об общежитии", get_dormitory_menu),
    "rules": ("📋 Правила и регламент", None),
    "payment": ("💳 Оплата и счета", None),
    "maintenance": ("🔧 Техническое обслуживание", None),
    "contacts": ("👨‍💼 Контакты администрации", None),
    "faq": ("❓ Часто задаваемые вопросы", None),
    "room_numbers": ("🚪 Номера комнат", None),
    "location": ("📍 Местоположение", None),
    "conditions": ("🛏️ Условия проживания", None),
    "dining": ("🍽️ Столовая и питание", None),
    "sports": ("🎾 Спортивные объекты", None),
    "free_question": ("💬 Свободный вопрос", None),
}

async def start_command(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /start"""
    chat_id = update.effective_chat.id
    user = update.effective_user
    
    welcome_text = f"👋 Привет, {user.first_name}!\n\n🤖 Я помощник по информации об общежитии БНТУ.\n\nЧто ты хочешь узнать?"
    
    await context.bot.send_message(
        chat_id=chat_id,
        text=welcome_text,
        reply_markup=get_main_menu()
    )

async def callback_handler(update: Update, context: CallbackContext) -> None:
    """Обработчик всех inline кнопок"""
    query = update.callback_query
    await query.answer()  # Закрыть loading анимацию
    
    callback_data = query.data
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    
    # Обработка кнопки возврата
    if callback_data == "back_to_main":
        text = "🏠 Главное меню. Выбери раздел:"
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=get_main_menu()
        )
        return
    
    # Обработка кнопки свободного вопроса
    if callback_data == "free_question":
        text = "💬 Напиши свой вопрос, и я постараюсь помочь:"
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=get_back_button()
        )
        # Переводим бота в режим ожидания текстового ввода
        context.user_data['waiting_for_question'] = True
        return
    
    # Обработка кнопки информации об общежитии (подменю)
    if callback_data == "dormitory_info":
        text = "🏠 Выбери интересующую информацию:"
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=get_dormitory_menu()
        )
        return
    
    # Получение информации из базы данных
    if callback_data in CALLBACK_MAPPING:
        title, submenu = CALLBACK_MAPPING[callback_data]
        info = get_dormitory_info(callback_data)
        
        text = f"{title}\n\n{info}"
        
        # Если есть подменю, показываем его
        reply_markup = submenu() if submenu else get_back_button()
        
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )

async def message_handler(update: Update, context: CallbackContext) -> None:
    """Обработчик текстовых сообщений"""
    chat_id = update.effective_chat.id
    user_message = update.message.text
    
    # Если бот ожидает вопроса в режиме свободного вопроса
    if context.user_data.get('waiting_for_question'):
        context.user_data['waiting_for_question'] = False
        
        # Показываем "печатает"
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")
        
        try:
            # Отправляем вопрос в Gemini AI
            response = getTextResponse(user_message)
            await context.bot.send_message(chat_id=chat_id, text=response)
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            await context.bot.send_message(chat_id=chat_id, text="❌ Извините, произошла ошибка при обработке вашего вопроса.")
        
        # Возвращаем меню
        await context.bot.send_message(
            chat_id=chat_id,
            text="Что еще ты хочешь узнать?",
            reply_markup=get_main_menu()
        )
    else:
        # Обработка обычных сообщений с меню
        await context.bot.send_message(
            chat_id=chat_id,
            text="👋 Пожалуйста, используй кнопки меню для навигации:",
            reply_markup=get_main_menu()
        )
