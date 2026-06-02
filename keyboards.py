"""
Модуль для создания клавиатур и кнопок бота
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def get_main_menu():
    """Основное меню с кнопками"""
    keyboard = [
        [InlineKeyboardButton("🏠 Общежитие", callback_data="dormitory_info")],
        [InlineKeyboardButton("📋 Правила и регламент", callback_data="rules")],
        [InlineKeyboardButton("💳 Оплата и счета", callback_data="payment")],
        [InlineKeyboardButton("🔧 Техническое обслуживание", callback_data="maintenance")],
        [InlineKeyboardButton("👨‍💼 Контакты администрации", callback_data="contacts")],
        [InlineKeyboardButton("❓ Часто задаваемые вопросы", callback_data="faq")],
        [InlineKeyboardButton("💬 Свободный вопрос", callback_data="free_question")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_dormitory_menu():
    """Меню с информацией об общежитии"""
    keyboard = [
        [InlineKeyboardButton("🚪 Номера комнат", callback_data="room_numbers")],
        [InlineKeyboardButton("📍 Местоположение", callback_data="location")],
        [InlineKeyboardButton("🛏️ Условия проживания", callback_data="conditions")],
        [InlineKeyboardButton("🍽️ Столовая и питание", callback_data="dining")],
        [InlineKeyboardButton("🎾 Спортивные объекты", callback_data="sports")],
        [InlineKeyboardButton("← Назад", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_button():
    """Кнопка возврата в главное меню"""
    keyboard = [
        [InlineKeyboardButton("← Назад", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_yes_no_keyboard():
    """Клавиатура да/нет"""
    keyboard = [
        [InlineKeyboardButton("✅ Да", callback_data="yes"),
         InlineKeyboardButton("❌ Нет", callback_data="no")],
        [InlineKeyboardButton("← Назад", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)
