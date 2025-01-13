from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


html_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='TXT в PDF')],
        [KeyboardButton(text='DOCX в PDF')],
        [KeyboardButton(text='Изображение в PDF')],
        [KeyboardButton(text='DOCX в TXT')],
        [KeyboardButton(text='TXT в DOCX')],  # New button for TXT to DOCX
        [KeyboardButton(text='PNG в JPEG')]  # New button for PNG to JPEG
    ],
    resize_keyboard=True
)
