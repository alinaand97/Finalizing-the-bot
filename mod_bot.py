# Витамины для всех!
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

api=''
bot = Bot(token = api)
storage = MemoryStorage()
dp = Dispatcher(bot, storage = MemoryStorage())

# Определение состояний
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# Создание обычной клавиатуры
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_calculate = types.KeyboardButton('Рассчитать')
button_info = types.KeyboardButton('Информация')
button_buy = types.KeyboardButton('Купить')  # Новая кнопка "Купить"
keyboard.add(button_calculate, button_info, button_buy)

# Создание Inline-клавиатуры
inline_keyboard = types.InlineKeyboardMarkup()
product_buttons = [
    types.InlineKeyboardButton(f'Product{i}', callback_data='product_buying')
    for i in range(1, 5)
]
inline_keyboard.add(*product_buttons)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == 'Купить')
async def get_buying_list(message: types.Message):
    products_info = []
    for i in range(1, 5):
        product_info = f'Название: Product{i} | Описание: описание {i} | Цена: {i * 100}'
        products_info.append(product_info)

        # Предположим, что у вас есть изображения Product1.jpg, Product2.jpg и т.д.
        photo_path = f'Product{i}.jpg'  # Путь к изображению продукта (замените на актуальный путь)
        with open(photo_path, 'rb') as photo:
            await message.answer(product_info)
            await bot.send_photo(message.chat.id, photo)

    await message.answer("Выберите продукт для покупки:", reply_markup=inline_keyboard)

@dp.callback_query_handler(lambda call: call.data == 'product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    await call.answer()  # Ответить на callback
    await call.message.answer("Вы успешно приобрели продукт!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)