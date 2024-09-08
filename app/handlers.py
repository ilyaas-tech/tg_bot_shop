from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

import app.keyboards as kb
from app.database.requests import get_items_by_id, set_user


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await set_user(message.from_user.id)
    await message.answer('Добро пожаловать в магазин кроссовок!', reply_markup=kb.main)


@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите категорию товара', reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    category_id = int(callback.data.split('_')[1])

    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Все товары из категории', reply_markup=await kb.items(category_id))

@router.callback_query(F.data.startswith('item_'))
async def category(callback: CallbackQuery):
    item_id = int(callback.data.split('_')[1])

    item_info = await get_items_by_id(item_id)

    await callback.message.answer(f'товар: {item_info.title}\nцена: {item_info.price}\nописание: {item_info.description}', reply_markup=kb.item_use())