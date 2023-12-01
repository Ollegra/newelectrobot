from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, StateFilter, Text
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
import logging
from bot_db import people_add, power_add, db_get_pow, people_get, trans_get, task_add, task_get, num_sql, trans_update, people_stat, trans_stat, powers_stat, oldpeople_stat
from kbrd import main_keyboard, answ_keyboard, ktp_keyboard, onf_keyboard, stats_keyboard
from config import POWER_GK, FIL1, FIL2, FIL3


txt_p = ''
txt_c = ''
user_dict: dict[int, dict[str, str | int]] = {}

logger2 = logging.getLogger(__name__)
logger2.setLevel(logging.INFO)
handler2 = logging.FileHandler(f"{__name__}.log")
formatter2 = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler2.setFormatter(formatter2)
logger2.addHandler(handler2)

logger2.info(f'Handlers created for module {__name__}...')

router = Router()


class FSMFillForm(StatesGroup):
  person_st = State()
  category_st = State()
  new_tasks = State()
  ktp_update = State()
  ktp_save = State()


@router.message(Command(commands='start'))
async def start_command(message: Message):
  await message.answer(f'<b>{message.from_user.first_name}</b>, <i>это информационно-производственный бот электроучастка ГК ⚡</i>', reply_markup=main_keyboard())


@router.message(Command(commands='zakoma'))
async def zakoma_command(message: Message):
  await message.answer_photo(FIL1)


@router.message(Command(commands='motor'))
async def motor_command(message: Message):
  await message.answer_photo(FIL2)
  await message.answer_photo(FIL3)


@router.message(Command(commands='statuspower'))
async def st_power_command(message: Message):
  await message.answer(f'<b>Определите новое состояние питания:</b> ', reply_markup=answ_keyboard())


@router.message(Command(commands='statist'))
async def statist_command(message: Message):
  await message.answer(f'<i>Статистика по участку за месяц: </i>',
                       reply_markup=stats_keyboard())

@router.message(Command(commands='admin'), F.from_user.id != 463456492)
async def st_not_admin(message: Message):
  await message.answer(f'🛑 <i>Эта конманда доступна только администраторам!</i>', reply_markup=stats_keyboard())
  logger2.info(f'конманда admin доступна только администраторам!...')


@router.message(Command(commands='admin'), F.from_user.id == 463456492, StateFilter(default_state))
async def admin_stat(message: Message, state: FSMContext):
  await message.answer(text='Введите наличие персонала (yes|no) или статус КТП (on|off) через пробел')
  await state.set_state(FSMFillForm.person_st)


@router.message(StateFilter(FSMFillForm.person_st))
async def person_add(message: Message, state: FSMContext):
  await state.update_data(name=message.text)
  await message.answer(text='Введите код персонала или код КТП (p|t)')
  await state.set_state(FSMFillForm.category_st)


@router.message(StateFilter(FSMFillForm.category_st))
async def cat_add(messsage: Message, state: FSMContext):
  await state.update_data(categ=messsage.text)
  user_dict[messsage.from_user.id] = await state.get_data()
  work = user_dict[messsage.from_user.id]['name'].lower()
  kat = user_dict[messsage.from_user.id]['categ'].lower()
  people_add(work, kat)
  if kat == 'p':
    tcat = 'персонал'
  elif kat == 't':
    tcat = 'трансформаторы'
  await messsage.answer(
    text=f'<b>Отлично!</b>\n<i>Обновляю статус категории</i> <b>{tcat}</b>',
    reply_markup=main_keyboard())
  logger2.info(f'Обновляю статус категории {tcat}...')
  await state.clear()


@router.message(Command(commands='newtask'), StateFilter(default_state))
async def admin_task(message: Message, state: FSMContext):
  await message.answer(text='Введите описание новой задачи (до 50 символов)')
  await state.set_state(FSMFillForm.new_tasks)


@router.message(StateFilter(FSMFillForm.new_tasks))
async def newtasks_add(message: Message, state: FSMContext):
  await state.update_data(name=message.text)
  task_add(message.text)
  await message.answer(
    text=f'<b>Отлично!</b>\n<i>Обновляю список задач на сегодня</i>',
    reply_markup=main_keyboard())
  logger2.info(f'Обновляю список задач на сегодня...')
  await state.clear()


@router.message(Command(commands='statusktp'), StateFilter(default_state))
async def st_ktp_command(message: Message, state: FSMContext):
  await message.answer(f'Выберите КТП для изменения состояния : ',
                       reply_markup=ktp_keyboard())
  await state.set_state((FSMFillForm.ktp_update))


@router.callback_query(
  StateFilter(FSMFillForm.ktp_update),
  Text(text=['КТП 160', 'КТП 250', 'КТП 400', 'КТП 630', 'КТП 2500']))
async def ktp_press(callback: CallbackQuery, state: FSMContext):
  await state.update_data(name=callback.data)
  await callback.message.delete()
  await callback.message.answer(text='Выберите новое состояние КТП :)',
                                reply_markup=onf_keyboard())
  await state.set_state(FSMFillForm.ktp_save)


@router.callback_query(StateFilter(FSMFillForm.ktp_save),
                       Text(text=['on', 'off']))
async def st_press(callback: CallbackQuery, state: FSMContext):
  await state.update_data(stat=callback.data)
  user_dict[callback.from_user.id] = await state.get_data()
  ktp = user_dict[callback.from_user.id]['name']
  onf = user_dict[callback.from_user.id]['stat']
  trans_update(ktp, onf)
  await callback.answer(text=f'Выбрано состояние {onf}')
  await callback.message.delete()
  await callback.message.answer(text=f'Состояние {ktp} изменено: <b>{onf}</b>',
                                reply_markup=main_keyboard())
  logger2.info(f'Состояние {ktp} изменено: {onf}...')
  await state.clear()


@router.callback_query(lambda c: c.data == 'power')
async def pr_callback_start(callback: CallbackQuery):
  # await callback.answer(text='⚡ Запрос состояния эелектропитания', show_alert=True)
  # await callback.answer(text=f'Питание: ⚡ {db_get_pow()}')
  await callback.answer()
  await callback.message.edit_text(text=f'Питание: ⚡ {db_get_pow()}',
                                   reply_markup=callback.message.reply_markup)


@router.callback_query(lambda c: c.data == 'workers')
async def pr_callback_workers(callback: CallbackQuery):
  #await callback.answer(text='выбрано наличие персонала на участке')
  await callback.message.edit_text(people_get(),
                                   reply_markup=callback.message.reply_markup)
  await callback.answer()


@router.callback_query(lambda c: c.data == 'transformers')
async def pr_callback_transformers(callback: CallbackQuery):
  #await callback.answer(text='информация о состоянии подстанций')
  await callback.message.edit_text(trans_get(),
                                   reply_markup=callback.message.reply_markup)
  await callback.answer()


@router.callback_query(lambda c: c.data == 'tasks')
async def task_get_start(callback: CallbackQuery):
  #await callback.answer(text='чем занят персонал на участке')
  await callback.message.edit_text(task_get(),
                                   reply_markup=callback.message.reply_markup)
  await callback.answer()


@router.callback_query(Text(text=['basic', 'backup']))
async def call_basic_buckup(callback: CallbackQuery):
  if callback.data == 'basic':
    powered = POWER_GK[0]
    power_add(powered)
  if callback.data == 'backup':
    powered = POWER_GK[1]
    power_add(powered)
  await callback.answer(text='Питание: ⚡ ' + powered, show_alert=True)
  # await callback.message.delete()
  await callback.message.edit_text(
    f'⚡ <i>Состояние электропитания изменено</i>',
    reply_markup=main_keyboard())
  logger2.info(f'Состояние электропитания изменено {powered}...')


@router.callback_query(
  Text(text=['worktime', 'oldworktime', 'ontrans', 'tenkvoff', 'statoff']))
async def call_work_onf(callback: CallbackQuery):
  if callback.data == 'worktime':
    await callback.message.edit_text(people_stat(),
                                     reply_markup=stats_keyboard())
  if callback.data == 'oldworktime':
    await callback.message.edit_text(oldpeople_stat(),
                                     reply_markup=stats_keyboard())
  if callback.data == 'ontrans':
    await callback.message.edit_text(trans_stat(),
                                     reply_markup=stats_keyboard())
  if callback.data == 'tenkvoff':
    await callback.message.edit_text(powers_stat(),
                                     reply_markup=stats_keyboard())
  if callback.data == 'statoff':
    await callback.message.delete()
    await callback.message.answer(f'⚡ <i>Просмотр статистики окончен</i>',
                                  reply_markup=main_keyboard())
    logger2.info(f'Просмотр статистики окончен...')


@router.message(F.photo)
async def send_photo(message: Message):
  print(message.photo[-1].file_id)
  await message.reply_photo(message.photo[-1].file_id)


@router.message()
async def other_message(message: Message):
  await message.answer(
    text=
    f'✋ <b>{message.from_user.first_name}</b>, <i>я не отвечаю на сообщения</i>\n👉 <b>используй команды в меню или кнопки</b>',
    reply_markup=main_keyboard())
  # await message.answer(people_stat(), reply_markup=main_keyboard())
# print('Handlers created', '.' * 24)