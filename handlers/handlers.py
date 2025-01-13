import os
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config_data.config import Config, load_config
from aiogram.types.input_file import FSInputFile
from database.database import insert_database
from keyboards.keyboard import html_keyboard
from lexicon.lexicon import LEXICON_RU
from utils.utils import convert_docx_to_txt, convert_txt_to_pdf, convert_images_to_pdf, convert_txt_to_docx, convert_docx_to_pdf, convert_png_to_jpeg

config: Config = load_config()
bot = Bot(token=config.tg_bot.token)

# Create states for FSM
class Convert(StatesGroup):
    txt = State()
    docx = State()
    pics = State()
    docx_to_txt = State()  # State for DOCX to TXT conversion
    txt_to_docx = State()  # New state for TXT to DOCX conversion
    png_to_jpeg = State()  # State for PNG to JPEG conversion
router = Router()

# Handlers for commands and actions
@router.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer(LEXICON_RU['/start'], reply_markup=html_keyboard)
    user_id = message.from_user.id
    username = message.from_user.username
    insert_database(user_id, username)

@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(LEXICON_RU['/help'])

@router.message(F.text == 'PNG в JPEG')  # New handler for PNG to JPEG
async def register_png_to_jpeg(message: Message, state: FSMContext):
    await state.set_state(Convert.png_to_jpeg)
    await message.answer("Пожалуйста, загрузите изображение в формате .png.")

@router.message(Convert.png_to_jpeg)
async def png_to_jpeg_convert(message: Message, state: FSMContext):
    user_id = message.from_user.id
    document = message.document

    if not document.file_name.lower().endswith('.png'):
        await message.reply("Пожалуйста, отправьте изображение в формате .png.")
        return

    file_info = await bot.get_file(document.file_id)
    png_file_path = f"./temps/{document.file_name}"
    jpeg_file_path = f"./temps/{document.file_name.replace('.png', '.jpg')}"

    await bot.download_file(file_info.file_path, png_file_path)
    convert_png_to_jpeg(png_file_path, jpeg_file_path)

    await bot.send_document(user_id, FSInputFile(jpeg_file_path), caption='Ваш JPEG-файл!')

    os.remove(png_file_path)
    os.remove(jpeg_file_path)
    await state.clear()
    await message.answer("Выберите действие:", reply_markup=html_keyboard)

@router.message(F.text == 'TXT в DOCX')  # New handler for TXT to DOCX
async def register_txt_to_docx(message: Message, state: FSMContext):
    await state.set_state(Convert.txt_to_docx)
    await message.answer("Пожалуйста, загрузите текстовый файл в формате .txt.")

@router.message(Convert.txt_to_docx)
async def txt_to_docx_convert(message: Message, state: FSMContext):
    user_id = message.from_user.id
    document = message.document

    if not document.file_name.endswith('.txt'):
        await message.reply("Пожалуйста, отправьте текстовый файл в формате .txt.")
        return

    file_info = await bot.get_file(document.file_id)
    txt_file_path = f"./temps/{document.file_name}"
    docx_file_path = f"./temps/{document.file_name.replace('.txt', '.docx')}"

    await bot.download_file(file_info.file_path, txt_file_path)
    convert_txt_to_docx(txt_file_path, docx_file_path)

    await bot.send_document(user_id, FSInputFile(docx_file_path), caption='Ваш DOCX-файл!')

    os.remove(txt_file_path)
    os.remove(docx_file_path)
    await state.clear()
    await message.answer("Выберите действие:", reply_markup=html_keyboard)

@router.message(F.text == 'DOCX в TXT')  # Existing handler for DOCX to TXT
async def register_docx_to_txt(message: Message, state: FSMContext):
    await state.set_state(Convert.docx_to_txt)
    await message.answer("Пожалуйста, загрузите документ в формате .docx.")

@router.message(Convert.docx_to_txt)
async def docx_to_txt_convert(message: Message, state: FSMContext):
    user_id = message.from_user.id
    document = message.document

    if not document.file_name.endswith('.docx'):
        await message.reply("Пожалуйста, отправьте документ в формате .docx.")
        return

    file_info = await bot.get_file(document.file_id)
    docx_file_path = f"./temps/{document.file_name}"
    txt_file_path = f"./temps/{document.file_name.replace('.docx', '.txt')}"

    await bot.download_file(file_info.file_path, docx_file_path)
    convert_docx_to_txt(docx_file_path, txt_file_path)

    await bot.send_document(user_id, FSInputFile(txt_file_path), caption='Ваш TXT-файл!')

    os.remove(docx_file_path)
    os.remove(txt_file_path)
    await state.clear()
    await message.answer("Выберите действие:", reply_markup=html_keyboard)

@router.message(F.text == 'TXT в PDF')
async def register_txt(message: Message, state: FSMContext):
    await state.set_state(Convert.txt)
    await message.answer("Пожалуйста, загрузите текстовый файл в формате .txt.")

@router.message(Convert.txt)
async def txt_convert(message: Message, state: FSMContext):
    user_id = message.from_user.id
    document = message.document

    if not document.file_name.endswith('.txt'):
        await message.reply("Пожалуйста, отправьте текстовый файл в формате .txt.")
        return

    file_info = await bot.get_file(document.file_id)
    txt_file_path = f"./temps/{document.file_name}"
    pdf_file_path = f"./temps/{document.file_name}.pdf"

    await bot.download_file(file_info.file_path, txt_file_path)
    convert_txt_to_pdf(txt_file_path, pdf_file_path)

    await bot.send_document(user_id, FSInputFile(pdf_file_path), caption='Ваш PDF-файл!')

    os.remove(txt_file_path)
    os.remove(pdf_file_path)
    await state.clear()
    await message.answer("Выберите действие:", reply_markup=html_keyboard)

@router.message(F.text == 'DOCX в PDF')
async def register_docx(message: Message, state: FSMContext):
    await state.set_state(Convert.docx)
    await message.answer("Пожалуйста, загрузите документ в формате .docx.")

@router.message(Convert.docx)
async def docx_convert(message: Message, state: FSMContext):
    user_id = message.from_user.id
    document = message.document

    if not document.file_name.endswith('.docx'):
        await message.reply("Пожалуйста, отправьте документ в формате .docx.")
        return

    file_info = await bot.get_file(document.file_id)
    docx_file_path = f"./temps/{document.file_name}"
    pdf_file_path = f"./temps/{document.file_name}.pdf"

    await bot.download_file(file_info.file_path, docx_file_path)
    convert_docx_to_pdf(docx_file_path, pdf_file_path)

    await bot.send_document(user_id, FSInputFile(pdf_file_path), caption='Ваш PDF-файл!')

    os.remove(docx_file_path)
    os.remove(pdf_file_path)
    await state.clear()
    await message.answer("Выберите действие:", reply_markup=html_keyboard)

@router.message(F.text == 'Изображение в PDF')
async def register_images(message: Message, state: FSMContext):
    await state.set_state(Convert.pics)
    await message.answer("Пожалуйста, загрузите изображение в формате .png, .jpg или .bmp.")

@router.message(Convert.pics)
async def images_convert(message: Message, state: FSMContext):
    user_id = message.from_user.id
    document = message.document

    if not document.file_name.lower().endswith(('.png', '.jpg', '.bmp')):
        await message.reply("Пожалуйста, отправьте изображение в формате .png, .jpg или .bmp.")
        return

    file_info = await bot.get_file(document.file_id)
    image_file_path = f"./temps/{document.file_name}"
    pdf_file_path = f"./temps/{document.file_name}.pdf"

    await bot.download_file(file_info.file_path, image_file_path)
    convert_images_to_pdf(image_file_path, pdf_file_path)

    await bot.send_document(user_id, FSInputFile(pdf_file_path), caption='Ваш PDF-файл!')

    os.remove(image_file_path)
    os.remove(pdf_file_path)
    await state.clear()
    await message.answer("Выберите действие:", reply_markup=html_keyboard)