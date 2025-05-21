from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton


# Главное меню
def get_main_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    buttons = [
        "👁️ Проверить зрение",
        "💡 Советы",
        "🤒 Заболевания",
        "🏥 Запись к врачу",
        "❓ Помощь",
        "📝 Оставить отзыв"
    ]
    for btn in buttons:
        builder.button(text=btn)
    builder.adjust(2, 2, 2)  # 2 кнопки в строке
    return builder.as_markup(resize_keyboard=True)

# Меню тестов зрения
def get_vision_test_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Тест 1", callback_data="test_sivtsev"),
        InlineKeyboardButton(text="Тест 2", callback_data="test_color"),
    )
    builder.row(
        InlineKeyboardButton(text="Тест 3", callback_data="test_astigmatism"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="back_main"),
    )
    return builder.as_markup()

# Клавиатура "Отмена"
def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="❌ Отмена")
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


# Заболевания
def get_diseases_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="Близорукость", callback_data="disease_myopia"),
        InlineKeyboardButton(text="Дальнозоркость", callback_data="disease_hyperopia"),
    )
    
    builder.row(
        InlineKeyboardButton(text="Катаракта", callback_data="disease_cataract"),
        InlineKeyboardButton(text="Глаукома", callback_data="disease_glaucoma"),
    )
    
    builder.row(
        InlineKeyboardButton(text="Конъюнктивит", callback_data="disease_conjunctivitis"),
        InlineKeyboardButton(text="Астигматизм", callback_data="disease_astigmatism"),
    )
    
    builder.row(
        InlineKeyboardButton(text="Дальтонизм", callback_data="disease_colorblindness"),
    )
    
    builder.row(
        InlineKeyboardButton(text="🔙 Назад", callback_data="back_main"),
    )
    
    return builder.as_markup()

def get_back_to_diseases_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 К списку заболеваний", callback_data="back_diseases")
    return builder.as_markup()



# Кнопка назад запись к врачу
def get_clinics_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")
    )
    return builder.as_markup()

# Советы
def get_health_tips_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Упражнения 🧘", callback_data="tips_exercises"),
        InlineKeyboardButton(text="Питание 🥗", callback_data="tips_nutrition"),
    )
    builder.row(
        InlineKeyboardButton(text="Профилактика 🛡️", callback_data="tips_prevention"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="back_main"),
    )
    return builder.as_markup()

def get_back_to_tips_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 К категориям", callback_data="back_tips")
    return builder.as_markup()

# Помощь
def get_help_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")
    )
    return builder.as_markup()
