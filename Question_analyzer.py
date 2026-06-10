import os
from google import genai
from database import get_all_dormitory_data

API_KEY = os.environ.get('GEMINI_API_KEY')

if not API_KEY:
    raise ValueError("Переменная окружения GEMINI_API_KEY не установлена")

client = genai.Client(api_key=API_KEY)

SECTION_KEYWORDS = {
    "room_numbers": ["номер", "комната", "этаж", "размещение", "общие", "двойная", "тройная", "соседи"],
    "location": ["где", "адрес", "как добраться", "транспорт", "метро", "троллейбус", "автобус", "машина"],
    "conditions": ["условия", "удобства", "интернет", "горячая вода", "отопление", "кухня", "прачечная"],
    "dining": ["столовая", "питание", "обед", "завтрак", "ужин", "еда", "меню", "кухня", "стоимость"],
    "sports": ["спорт", "тренажер", "волейбол", "баскетбол", "теннис", "гимнастика", "зал", "физкультура"],
    "rules": ["правила", "запрещено", "разрешено", "комендантский", "тишина", "животные", "курение"],
    "payment": ["оплата", "цена", "стоимость", "деньги", "счет", "банк", "льготы", "скидка", "семестр"],
    "contacts": ["контакты", "телефон", "номер", "почта", "email", "администрация", "комендант", "связь"],
    "faq": ["как", "почему", "можно ли", "вопрос", "ответ"],
    "maintenance": ["поломка", "ремонт", "заявка", "техническое", "проблема", "сломалось"],
}

def find_relevant_section(user_message: str) -> str:
    message_lower = user_message.lower()
    
    for section, keywords in SECTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in message_lower:
                return section
    
    return "faq"

def get_intelligent_response(user_message: str) -> str:
    relevant_section = find_relevant_section(user_message)
    section_info = get_all_dormitory_data().get(relevant_section, "")
    
    clean_info = section_info.replace("🏠", "").replace("📋", "").replace("💳", "").replace("🔧", "").replace("👨‍💼", "").replace("❓", "").replace("💬", "").replace("🏃", "").replace("🍽️", "").replace("🎾", "").replace("📞", "").replace("📍", "").replace("✅", "").replace("📱", "").strip()
    
    prompt = f"""Ты ассистент студентов БНТУ. На основе информации об общежитии, ответь на вопрос студента кратко и понятно своими словами.

Вопрос студента: {user_message}

Информация из базы данных: {clean_info}

Ответь прямо на вопрос, используя информацию выше. Ответ должен быть дружелюбным и понятным для студента."""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Ошибка при запросе к модели: {e}")
        return "Извините, не смог обработать ваш вопрос. Попробуйте позже."
