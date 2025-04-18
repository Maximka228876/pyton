from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from config import reminders


# Главное меню (крупные кнопки)
def get_main_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    buttons = [
        "👁️ Проверить зрение",
        "💡 Советы",
        "⏰ Напоминания",
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

# Меню напоминаний

def get_reminders_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Добавить", callback_data="add_reminder"),
        InlineKeyboardButton(text="Мои напоминания", callback_data="list_reminders"),
    )
    builder.row(
        InlineKeyboardButton(text="Удалить", callback_data="delete_reminder"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="back_main"),
    )
    return builder.as_markup()


def get_delete_reminder_keyboard(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    user_reminders = reminders.get(user_id, [])

    if not user_reminders:
        builder.button(text="Нет напоминаний", callback_data="no_reminders")
    else:
        for idx, rem in enumerate(user_reminders):
        
            builder.button(
            text=f"Удалить {idx + 1}: {rem['text']}",
            callback_data=f"delete_{rem['id']}"  # rem["id"] должен быть числом
        )
    
    builder.button(text="🔙 Назад", callback_data="back_main")
    builder.adjust(1)
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
