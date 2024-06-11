from bot import dp, bot, router
from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from handlers.functions import mute_all_notifications


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
        text=f"Подтвердите найденый объект\nНайденный класс: {predicted_class}",
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
    else:
        response_text = 'Вы отклонили объект!'

    await bot.send_message(callback_query.from_user.id, response_text)
