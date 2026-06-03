import logging
from telegram import Update
from telegram.ext import CallbackContext
from keyboards import get_main_menu, get_dormitory_menu, get_back_button, get_yes_no_keyboard
from database import get_dormitory_info
from Text_generator import getTextResponse
from telegram.error import BadRequest

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
    chat_id = update.effective_chat.id
    user = update.effective_user
    
    welcome_text = f"👋 Привет, {user.first_name}!\n\n🤖 Я помощник по информации об общежитии БНТУ.\n\nЧто ты хочешь узнать?"
    
    sent = await context.bot.send_message(
        chat_id=chat_id,
        text=welcome_text,
        reply_markup=get_main_menu()
    )

    context.user_data["last_bot_message_id"] = sent.message_id
    context.user_data["waiting_for_question"] = False

async def callback_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()  # Закрыть loading анимацию
    
    callback_data = query.data
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    context.user_data["last_bot_message_id"] = message_id
    
    # Обработка кнопки возврата
    if callback_data == "back_to_main":
        text = "🏠 Главное меню. Выбери раздел:"
        msg = await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=get_main_menu()
        )
        context.user_data["last_bot_message_id"] = msg.message_id
        context.user_data["waiting_for_question"] = False
        return
    
    # Обработка кнопки свободного вопроса
    if callback_data == "free_question":
        text = "💬 Напиши свой вопрос, и я постараюсь помочь:"
        msg = await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=get_back_button()
        )
        context.user_data["last_bot_message_id"] = msg.message_id
        context.user_data['waiting_for_question'] = True
        return
    
    # Обработка кнопки информации об общежитии (подменю)
    if callback_data == "dormitory_info":
        text = "🏠 Выбери интересующую информацию:"
        msg = await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=get_dormitory_menu()
        )
        context.user_data["last_bot_message_id"] = msg.message_id
        context.user_data["waiting_for_question"] = False
        return
    
    # Получение информации из базы данных
    if callback_data in CALLBACK_MAPPING:
        title, submenu = CALLBACK_MAPPING[callback_data]
        info = get_dormitory_info(callback_data) or "Информация пока недоступна."
        
        text = f"{title}\n\n{info}"
        
        # Если есть подменю, показываем его
        reply_markup = submenu() if submenu else get_back_button()
        
        msg = await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        context.user_data["last_bot_message_id"] = msg.message_id
        context.user_data["waiting_for_question"] = False

async def message_handler(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    user_message = update.message.text
    user_message_id = update.message.message_id

    if context.user_data.get("is_generating", False):
        try:
            await context.bot.delete_message(chat_id, user_message_id)
        except:
            pass
        return
    
    # Если бот ожидает вопроса в режиме свободного вопроса
    if context.user_data.get('waiting_for_question'):
        import asyncio

        context.user_data['waiting_for_question'] = False
        context.user_data['is_generating'] = True

        async def typing_loop():
            while context.user_data.get("is_generating", False):
                await context.bot.send_chat_action(chat_id, "typing")
                await asyncio.sleep(4)

        typing_task = asyncio.create_task(typing_loop())

        try:
            response = await asyncio.to_thread(getTextResponse, user_message)
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            response = "❌ Извините, произошла ошибка при обработке вашего вопроса."

        context.user_data["is_generating"] = False
        typing_task.cancel()

        await context.bot.send_message(chat_id, text=response)

        # Возвращаем меню
        msg = await context.bot.send_message(
            chat_id=chat_id,
            text="Что еще ты хочешь узнать?",
            reply_markup=get_main_menu()
        )
        context.user_data["last_bot_message_id"] = msg.message_id
        return

    else:
        try:
            await context.bot.delete_message(chat_id, user_message_id)
        except Exception as e:
            logger.warning(f"Не удалось удалить сообщение пользователя: {e}")

        last_bot_msg_id = context.user_data.get("last_bot_message_id")
        # Обработка обычных сообщений с меню
        try:
            msg = await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=last_bot_msg_id,
                text="👋 Пожалуйста, используй кнопки меню для навигации:",
                reply_markup=get_main_menu()
            )
            context.user_data["last_bot_message_id"] = msg.message_id
        except BadRequest as e:
            if "message is not modified" in str(e).lower():
                return
            else:
                raise
