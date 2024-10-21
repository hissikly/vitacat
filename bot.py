from aiogram import Bot, Dispatcher, types
import chat_model
import asyncio
from aiogram.enums import ParseMode
import os
from dotenv import load_dotenv
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from keyboards import kb_doc, button_text, button_titles
from aiogram.types import ReplyKeyboardRemove


load_dotenv()


bot = Bot(os.getenv("BOT_TOKEN"))
dp = Dispatcher()


class CommandsRate(StatesGroup):
    vitadoc_rate = State()
    vitapers_rate = State()


@dp.message(Command("help"))
async def get_help_command(mes: types.Message):
    await mes.answer("/vitadoc - краткая документация по боту\n/vitapers - рекомендация витаминов по вашему самочувствию")


@dp.message(Command("start"))
async def get_start_command(mes: types.Message):
    await mes.answer("/vitadoc - краткая документация по боту\n/vitapers - рекомендация витаминов по вашему самочувствию")


@dp.message(StateFilter(None), Command("vitapers"))
async def get_vitapers_command(mes: types.Message, state: FSMContext):
    await mes.answer("Чётко напишите то, что вас беспокоит, не забудьте написать ваш рост, вес, пол")

    await state.set_state(CommandsRate.vitapers_rate)


@dp.message(CommandsRate.vitapers_rate)
async def get_vitapers_rate(mes: types.Message, state: FSMContext):
    await mes.answer("Секунду... Генерирую ответ")

    bot_answer = await chat_model.get_message_by_gigachain(mes)
    await mes.answer(bot_answer, parse_mode=ParseMode.MARKDOWN)
    await state.clear()


@dp.message(StateFilter(None), Command("vitadoc"))
async def get_vitadoc_command(mes: types.Message, state: FSMContext):
    await mes.answer("Добро пожаловать в документацию по витаминам и пищевым добавкам. Выберите интересуемый витамин, чтобы узнать о нем побольше", reply_markup=kb_doc())

    await state.set_state(CommandsRate.vitadoc_rate)


@dp.message(CommandsRate.vitadoc_rate)
async def get_vitadoc_rate(mes: types.Message, state: FSMContext):
    answer_dict = dict(zip(button_titles, button_text))
    await mes.answer(answer_dict[mes.text], reply_markup=ReplyKeyboardRemove())

    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())