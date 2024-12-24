from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from db.db_functions import get_random_task, create_paste_user_id

# Заготовка кода, не более
# user_id = message.from_user.id
# username = message.from_user.username
# first_name = message.from_user.first_name
# last_name = message.from_user.last_name


# Переменные
# ------------------------------------
p_html = ParseMode.HTML
router = Router()


# Привественное сообщение и получение данных о пользователе
# ------------------------------------
@router.message(F.text == '/start')
async def send_welcome(message: types.Message) -> None:
    first_name = message.from_user.first_name
    tg_id = message.from_user.id
    text = (f'<b>Привет, {first_name} </b>👋\n'
            f'Меня зовут <b>Тьютор</b> и я помогу тебе подготовиться к ЕГЭ по английскому!\n'
            f'Но сначала выбери, в каком классе ты учишься:')
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Прогуливаюсь мимо'), KeyboardButton(text='10'), KeyboardButton(text='11')]]
    )
    create_paste_user_id(tg_id, first_name)

    await message.answer(text=text, reply_markup=kb, parse_mode=p_html)


@router.message(F.text in ['10', '11', 'Прогуливаюсь мимо'])
async def paste_class(message: types.Message):
    grade = message.text
    

# Стартовый запрос для появления сообщения бота
# ------------------------------------
# @router.message(F.text == "/start")
# async def send_welcome(message: types.Message) -> None:
#     first_name = message.from_user.first_name
#
#     kb = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(text="Подготовка", callback_data="preparation")],
#             [InlineKeyboardButton(text="Личный кабинет", callback_data="user_cabinet")],
#             [InlineKeyboardButton(text="Поддержка", callback_data="support")],
#         ]
#     )
#     text = f"<b>Привет, {first_name} </b>👋\nВыбери интересующий тебя раздел:"
#
#     await message.answer(text=text, reply_markup=kb, parse_mode=p_html)
#

# Возвращение в главное меню
# ------------------------------------
@router.callback_query(F.data == "main_menu")
async def back_to_main_menu(callback: types.CallbackQuery) -> None:
    first_name = callback.from_user.first_name
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Подготовка", callback_data="preparation")],
            [InlineKeyboardButton(text="Личный кабинет", callback_data="user_cabinet")],
            [
                InlineKeyboardButton(
                    text="Техническая поддержка", callback_data="support"
                )
            ],
        ]
    )
    text = f"<b>Привет, {first_name} 👋</b>\n Выбери интересующий тебя раздел ниже:"

    await callback.message.edit_text(text=text, reply_markup=kb, parse_mode=p_html)
    await callback.answer()


# Меню "Подготовка"
# ------------------------------------
@router.callback_query(F.data == "preparation")
async def menu_preparation(callback: types.CallbackQuery) -> None:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Готовые варианты 📚", callback_data="choose_exam_variants"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Типовые задания 📋", callback_data="choose_tamplate_tasks"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Проверить письмо 📝", callback_data="choose_essay"
                )
            ],
            [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")],
        ]
    )
    text = "Отлично, что же тебя интересует?"

    await callback.message.edit_text(text=text, reply_markup=kb, parse_mode=p_html)
    await callback.answer()


# Меню личного кабинета пользователя
# ------------------------------------
@router.callback_query(F.data == "user_cabinet")
async def menu_user_profile(callback: types.CallbackQuery) -> None:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="main_menu")],
        ]
    )
    text = "Пока в разработке, скоро исправим 😆"

    await callback.message.edit_text(text=text, reply_markup=kb, parse_mode=p_html)
    await callback.answer()


# Меню с технической поддержкой
# ------------------------------------
@router.callback_query(F.data == "support")
async def menu_support(callback: types.CallbackQuery) -> None:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="main_menu")],
        ]
    )
    text = "При возникновении проблем обращаться: @delotbtw"

    await callback.message.edit_text(text=text, reply_markup=kb, parse_mode=p_html)
    # await callback.message.answer()


# Выбор готового варианта
# ------------------------------------
@router.callback_query(F.data == "choose_exam_variants")
async def menu_exam_variants(callback: types.CallbackQuery) -> None:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Вариант 1", callback_data="variant"),
                InlineKeyboardButton(text="Вариант 2", callback_data="variant"),
            ],
            [
                InlineKeyboardButton(text="Вариант 3", callback_data="variant"),
                InlineKeyboardButton(text="Вариант 4", callback_data="variant"),
            ],
            [
                InlineKeyboardButton(
                    text="Рандомный вариант", callback_data="variant_random"
                )
            ],
            [InlineKeyboardButton(text="Назад", callback_data="preparation")],
        ]
    )
    text = "При возникновении проблем обращаться: @delobtw"

    await callback.message.edit_text(text=text, reply_markup=kb, parse_mode=p_html)
    await callback.answer()


# Выбор типовых заданий
# ------------------------------------
@router.callback_query(F.data == "choose_tamplate_tasks")
async def menu_template_tasks(callback: types.CallbackQuery) -> None:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Аудирование 🎧", callback_data="part_audirovanie"
                ),
                InlineKeyboardButton(text="Чтение 📖", callback_data="part_reading"),
            ],
            [
                InlineKeyboardButton(
                    text="Лексика и грамматика 📚", callback_data="part_grammar"
                ),
                InlineKeyboardButton(text="Письмо ✍️", callback_data="part_mail"),
            ],
            [InlineKeyboardButton(text="Назад", callback_data="preparation")],
        ]
    )
    text = "Часть экзамена:"

    await callback.message.edit_text(text=text, reply_markup=kb, parse_mode=p_html)
    await callback.answer()


# Раздел с проверкой письма
# ------------------------------------
@router.callback_query(F.data == "choose_essay")
async def menu_check_mail(callback: types.CallbackQuery) -> None:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Проверка нейросетью 🤖", callback_data="check_by_ai"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Проверка экспертом 👨‍🏫", callback_data="check_by_expert"
                )
            ],
            [InlineKeyboardButton(text="Назад", callback_data="preparation")],
        ]
    )
    text = "Ух ты, уже есть написанное письмо? Круто! \nКакой тип проверки выберешь?"

    await callback.message.edit_text(text=text, reply_markup=kb, parse_mode=p_html)
    await callback.answer()


# !!!!!!!!!!! !!ТУПО ЗАГЛУШКИ ДЛЯ КНОПОК, ПОКА НЕ НАПИШУ ПОД НИХ КОД !!!!!!!!!!!
# ? Заглушка на проверку экспертом
# ------------------------------------
@router.callback_query(F.data == "check_by_expert")
async def check_by_expert(callback: types.CallbackQuery) -> None:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="choose_essay")]
        ]
    )
    text = "Пока в разработке, скоро исправим 😆"

    await callback.message.edit_text(text=text, reply_markup=kb, parse_mode=p_html)
    await callback.answer()


# ? Заглушка на проверку нейронкой
# ------------------------------------
@router.callback_query(F.data == "check_by_ai")
async def check_by_ai(callback: types.CallbackQuery) -> None:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="choose_essay")]
        ]
    )
    text = "Пока в разработке, скоро исправим 😆"

    await callback.message.edit_text(text=text, reply_markup=kb, parse_mode=p_html)
    await callback.answer()


# ? Заглушка на готовые нумерованные варианты
# ------------------------------------
@router.callback_query(F.data == "variant")
async def done_variants(callback: types.CallbackQuery) -> None:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="choose_exam_variants")]
        ]
    )
    text = "Пока в разработке, скоро исправим 😆"

    await callback.message.edit_text(text=text, reply_markup=kb, parse_mode=p_html)
    await callback.answer()


# ? Заглушка на рандомный варинат
# ------------------------------------
@router.callback_query(F.data == "variant_random")
async def random_variant(callback: types.CallbackQuery) -> None:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="choose_exam_variants")]
        ]
    )
    text = "Пока в разработке, скоро исправим 😆"

    await callback.message.edit_text(text=text, reply_markup=kb, parse_mode=p_html)
    await callback.answer()


# ! Вариант того, как можно вытаскивать задания из бд и отправлять их пользователю
# @router.callback_query(F.data == "variant_random")
# async def random_variant(callback: types.CallbackQuery) -> None:
#     kb = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(text="Назад", callback_data="choose_exam_variants")]
#         ]
#     )
#     task = get_random_task(10)
#     id, desc, ans = task[1], task[2], task[3]
#     text = (f'Так, ну вот твое задание {id}:\n'
#             f'{desc}\n'
#             f'<span class="tg-spoiler">{ans}</span>')
#
#     await callback.message.edit_text(text=text, reply_markup=kb, parse_mode=p_html)
#     await callback.answer()


# ? Заглушка на аудирование
# ------------------------------------
@router.callback_query(F.data == "part_audirovanie")
async def part_audio(callback: types.CallbackQuery) -> None:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="choose_tamplate_tasks")]
        ]
    )
    text = "Пока в разработке, скоро исправим 😆"

    await callback.message.edit_text(text=text, reply_markup=kb, parse_mode=p_html)
    await callback.answer()


# ? Заглушка на чтение
# ------------------------------------
@router.callback_query(F.data == "part_reading")
async def part_reading(callback: types.CallbackQuery) -> None:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="choose_tamplate_tasks")]
        ]
    )
    text = "Пока в разработке, скоро исправим 😆"

    await callback.message.edit_text(text=text, reply_markup=kb, parse_mode=p_html)
    await callback.answer()


# ? Заглушка на чтение
# ------------------------------------
@router.callback_query(F.data == "part_grammar")
async def part_grammar(callback: types.CallbackQuery) -> None:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="choose_tamplate_tasks")]
        ]
    )
    text = "Пока в разработке, скоро исправим 😆"

    await callback.message.edit_text(text=text, reply_markup=kb, parse_mode=p_html)
    await callback.answer()


# ? Заглушка на чтение
# ------------------------------------
@router.callback_query(F.data == "part_mail")
async def part_mail(callback: types.CallbackQuery) -> None:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="choose_tamplate_tasks")]
        ]
    )
    text = "Пока в разработке, скоро исправим 😆"

    await callback.message.edit_text(text=text, reply_markup=kb, parse_mode=p_html)
    await callback.answer()
