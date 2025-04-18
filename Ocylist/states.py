from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    vision_test = State()
    waiting_for_reminder_text = State()
    waiting_for_reminder_time = State()
    waiting_for_feedback = State()
    color_test = State()
    astigmatism_test = State()
    waiting_for_feedback = State()