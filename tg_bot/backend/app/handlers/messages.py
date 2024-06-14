from bot import dp, bot, router
from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from handlers.functions import mute_all_notifications


yolo_clasees = {
    0: 'БПЛА коптерного типа',
    1: 'Самолет',
    2: 'Вертолет',
    3: 'Птица',
    4: 'БПЛА самолетного типа',
}


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")
    await message.answer("Переходи в приложение для настройки оповещений: ")
    await message.answer("https://t.me/lct24_bb_bot/test/")


@dp.message(Command('settings'))
async def cmd_settings(message: Message):
    await message.answer("https://t.me/lct24_bb_bot/test/")


@dp.message(Command('off_all_notifications'))
async def cmd_off_all_notifications(message: Message):
    await mute_all_notifications(message.from_user.id)
    await message.answer("Оповещения для все классов были выключены")


async def bot_send_message(
    bot: Bot,
    user_id: int,
    photo_path: str,
    predicted_class: int
):
    sent_photo = await bot.send_photo(chat_id=user_id, photo=photo_path)
    photo_message_id = sent_photo.message_id

    button_true = InlineKeyboardButton(
        text="👍",
        callback_data='true'
    )

    button_false = InlineKeyboardButton(
        text="👎",
        callback_data='false'
    )

    markup = InlineKeyboardMarkup(
        inline_keyboard=[[button_true, button_false]]
    )

    sent_message = await bot.send_message(
        chat_id=user_id,
        text=f"Подтвердите найденый объект\nНайденный класс: {yolo_clasees[predicted_class]}",
        reply_markup=markup
    )
    message_message_id = sent_message.message_id

    return photo_message_id, message_message_id


@router.callback_query(lambda c: c.data == 'true' or c.data == 'false')
async def process_callback_button(callback_query: CallbackQuery):
    await bot.delete_message(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id
    )

    if callback_query.data == 'true':
        response_text = 'Вы подтвердили найденный объект! Он будет добавлен в базу данных.'
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=response_text,
        )
    else:
        response_text = 'Вы отклонили объект! Выберите подходящий класс из предложенного списка.'
        button_k1 = InlineKeyboardButton(
            text="1. БПЛА коптерного типа",
            callback_data='k1'
        )
        button_k2 = InlineKeyboardButton(
            text="2. Самолет",
            callback_data='k2'
        )
        button_k3 = InlineKeyboardButton(
            text="3. Вертолет",
            callback_data='k3'
        )
        button_k4 = InlineKeyboardButton(
            text="4. Птица",
            callback_data='k4'
        )
        button_k5 = InlineKeyboardButton(
            text="5. БПЛА самолетного типа",
            callback_data='k5'
        )
        button_k6 = InlineKeyboardButton(
            text="Нет ничего подходящего",
            callback_data='k6'
        )
        markup = InlineKeyboardMarkup(
            inline_keyboard=[[button_k1], [button_k2], [button_k3],
                             [button_k4], [button_k5], [button_k6]]
        )

        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=response_text,
            reply_markup=markup,
        )

@router.callback_query(lambda c: c.data == 'k1' or c.data == 'k2' or c.data == 'k3' or c.data == 'k4' or c.data == 'k5' or c.data == 'k6')
async def process_callback_after_false_button(callback_query: CallbackQuery):
    await bot.delete_message(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id
    )

    if callback_query.data == 'k1':
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text="Вы выбрали: БПЛА коптерного типа. Фото будет добавлено в датасет",
        )
    elif callback_query.data == 'k2':
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text="Вы выбрали: Самолет. Фото будет добавлено в датасет",
        )
    elif callback_query.data == 'k3':
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text="Вы выбрали: Вертолет. Фото будет добавлено в датасет",
        )
    elif callback_query.data == 'k4':
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text="Вы выбрали: Птица. Фото будет добавлено в датасет",
        )
    elif callback_query.data == 'k5':
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text="Вы выбрали: БПЛА самолетного типа. Фото будет добавлено в датасет",
        )
    elif callback_query.data == 'k6':
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text="Вы выбрали: Нет ничего подходящего.",
        )