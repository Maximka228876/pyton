from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, BufferedInputFile
from keyboards.main import get_vision_test_menu, get_cancel_keyboard, get_main_menu
from config import (
    SIVTSEV_IMAGES, SIVTSEV_ANSWERS,
    COLOR_IMAGES, COLOR_ANSWERS,
    ASTIGMATISM_IMAGES, ASTIGMATISM_ANSWERS,
    bot
)
from states import Form
import os

router = Router()

@router.message(F.text == "👁️ Проверить зрение")
async def vision_tests(message: types.Message):
    await message.answer(
        "🔍 Выберите тест:\n"
        "1. Тест на четкость зрения\n"
        "2. Тест на цветовосприятие\n"
        "3. Тест на астигматизм",
        reply_markup=get_vision_test_menu()
    )


@router.callback_query(F.data == "test_sivtsev")
async def start_sivtsev_test(callback: CallbackQuery, state: FSMContext):
    await state.update_data(current_test_step=1, correct_answers=0, total_questions=5)
    await callback.message.answer(
        "👁️ Тест на четкость зрения:\n"
        "1. Отойдите на 2-3 шага от экрана\n"
        "2. Закройте один глаз\n"
        "3. Вводите буквы через пробел (например: В Б Ы)",
        reply_markup=get_cancel_keyboard()
    )
    await _send_test_image(callback.from_user.id, 1)
    await state.set_state(Form.vision_test)
    await callback.answer()


@router.message(Form.vision_test)
async def process_test_answer(message: types.Message, state: FSMContext):
    # Если пользователь отменил тест
    if message.text == "❌ Отмена":
        await cancel_action(message, state)
        return

    data = await state.get_data()
    step = data["current_test_step"]
    correct_answers = SIVTSEV_ANSWERS.get(step, [])

    user_answers = [x.upper().strip() for x in message.text.split()]
    is_correct = set(user_answers) == set(correct_answers)

    new_correct = data["correct_answers"] + (1 if is_correct else 0)
    await state.update_data(
        current_test_step=step + 1,
        correct_answers=new_correct,
        **{f"step_{step}": is_correct}
    )

    if step + 1 > data["total_questions"]:
        await _finish_test(message, state)
    else:
        await _send_test_image(message.from_user.id, step + 1)


async def _send_test_image(user_id: int, step: int):
    image_path = os.path.join("images", SIVTSEV_IMAGES[step])
    if not os.path.exists(image_path):
        await bot.send_message(user_id, "❌ Ошибка загрузки теста")
        return

    with open(image_path, "rb") as f:
        await bot.send_photo(
            user_id,
            BufferedInputFile(f.read(), filename=f"test_{step}.jpg"),
            caption=f"Строка {step}. Введите буквы:"
        )


async def _finish_test(message: types.Message, state: FSMContext):
    data = await state.get_data()
    correct = data["correct_answers"]
    total = data["total_questions"]

    # Формируем результат
    result_text = "📊 Результаты:\n"
    for step in range(1, 6):
        result_text += f"Строка {step}: {'✅' if data.get(f'step_{step}') else '❌'}\n"

    recommendation = "🔴 Результат не очень хороший. Рекомендуем пройти обследование у офтальмолога!" if (correct / total < 0.6) else "🟢 Результат в норме. Но всеже рекомендуем пройти обследование у офтальмолога!"

    await message.answer(
        f"{result_text}\nПравильных ответов: {correct}/{total}\n{recommendation}",
        reply_markup=get_main_menu()
    )
    await state.clear()


@router.callback_query(F.data == "test_color")
async def start_color_test(callback: CallbackQuery, state: FSMContext):
    await state.update_data(
        current_test_step=1,
        correct_answers=0,
        total_questions=len(COLOR_IMAGES)
    )
    await callback.message.answer(
        "🎨 Тест на цветовосприятие:\n"
        "1. Рассмотрите изображение\n"
        "2. Введите число, которое видите",
        reply_markup=get_cancel_keyboard()
    )
    await _send_color_image(callback.from_user.id, 1)
    await state.set_state(Form.color_test)
    await callback.answer()


@router.message(Form.color_test)
async def process_color_answer(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await cancel_action(message, state)
        return

    data = await state.get_data()
    step = data["current_test_step"]
    correct = COLOR_ANSWERS.get(step, [])

    user_answer = message.text.strip()
    is_correct = user_answer in correct

    new_correct = data["correct_answers"] + (1 if is_correct else 0)
    await state.update_data(
        current_test_step=step + 1,
        correct_answers=new_correct,
        **{f"step_{step}": is_correct}
    )

    if step + 1 > data["total_questions"]:
        await _finish_color_test(message, state)
    else:
        await _send_color_image(message.from_user.id, step + 1)


async def _send_color_image(user_id: int, step: int):
    image_path = os.path.join("images", COLOR_IMAGES[step])
    with open(image_path, "rb") as f:
        await bot.send_photo(
            user_id,
            BufferedInputFile(f.read(), filename=f"color_{step}.jpg"),
            caption="Какое число вы видите?"
        )


async def _finish_color_test(message: types.Message, state: FSMContext):
    data = await state.get_data()
    correct = data["correct_answers"]
    total = data["total_questions"]

    result_text = "🎨 Результаты теста на цветовосприятие:\n"
    for step in range(1, total + 1):
        result_text += f"Изображение {step}: {'✅' if data.get(f'step_{step}') else '❌'}\n"

    recommendation = "🔴 Возможно нарушение цветовосприятия. Рекомендуем пройти обследование у офтальмолога!" if (correct / total < 1) else "🟢 Цветовосприятие в норме. Но всеже рекомендуем пройти обследование у офтальмолога!"

    await message.answer(
        f"{result_text}\nПравильных ответов: {correct}/{total}\n{recommendation}",
        reply_markup=get_main_menu()
    )
    await state.clear()


@router.callback_query(F.data == "test_astigmatism")
async def start_astigmatism_test(callback: CallbackQuery, state: FSMContext):
    await state.update_data(
        current_test_step=1,
        correct_answers=0,
        total_questions=len(ASTIGMATISM_IMAGES)
    )
    await callback.message.answer(
        "🌀 Тест на астигматизм:\n"
        "1. Отойдите на 2-3 шага от экрана\n"
        "2. Закройте один глаз\n"
        "3. Расмотрите изображение и опишите, что видите (если картинка никак не меняется, пишите 'Все линии четкие' или 'Нет искажений')",
        reply_markup=get_cancel_keyboard()
    )
    await _send_astigmatism_image(callback.from_user.id, 1)
    await state.set_state(Form.astigmatism_test)
    await callback.answer()


@router.message(Form.astigmatism_test)
async def process_astigmatism_answer(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await cancel_action(message, state)
        return

    data = await state.get_data()
    step = data["current_test_step"]
    correct = ASTIGMATISM_ANSWERS.get(step, [])

    user_answer = message.text.strip().lower()
    is_correct = any(user_answer == ans.lower() for ans in correct)

    new_correct = data["correct_answers"] + (1 if is_correct else 0)
    await state.update_data(
        current_test_step=step + 1,
        correct_answers=new_correct,
        **{f"step_{step}": is_correct}
    )

    if step + 1 > data["total_questions"]:
        await _finish_astigmatism_test(message, state)
    else:
        await _send_astigmatism_image(message.from_user.id, step + 1)


async def _send_astigmatism_image(user_id: int, step: int):
    image_path = os.path.join("images", ASTIGMATISM_IMAGES[step])
    with open(image_path, "rb") as f:
        await bot.send_photo(
            user_id,
            BufferedInputFile(f.read(), filename=f"astig_{step}.jpg"),
            caption="Опишите, что видите:"
        )


async def _finish_astigmatism_test(message: types.Message, state: FSMContext):
    data = await state.get_data()
    correct = data["correct_answers"]
    total = data["total_questions"]

    result_text = "🌀 Результаты теста на астигматизм:\n"
    for step in range(1, total + 1):
        result_text += f"Изображение {step}: {'✅' if data.get(f'step_{step}') else '❌'}\n"

    recommendation = "🔴 Возможен астигматизм. Рекомендуем пройти обследование у офтальмолога!" if (correct / total < 1) else "🟢 Искажений не обнаружено. Но всеже рекомендуем пройти обследование у офтальмолога!"

    await message.answer(
        f"{result_text}\nПравильных ответов: {correct}/{total}\n{recommendation}",
        reply_markup=get_main_menu()
    )
    await state.clear()


@router.message(F.text == "❌ Отмена")
async def cancel_action(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Действие отменено.", reply_markup=get_main_menu())
