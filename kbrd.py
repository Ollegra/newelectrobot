from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging
from config import POWER_GK, K

logger4 = logging.getLogger(__name__)
logger4.setLevel(logging.INFO)
handler4 = logging.FileHandler(f"{__name__}.log")
formatter4 = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler4.setFormatter(formatter4)
logger4.addHandler(handler4)

logger4.info(f'Keyboads created for module {__name__}...')


def main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='⚡ Питание', callback_data='power')
    builder.button(text='👷 Персонал', callback_data='workers')
    builder.button(text='🕋 Подстанции', callback_data='transformers')
    builder.button(text='📖 Задачи', callback_data='tasks')
    builder.adjust(3)
    key_bot = builder.as_markup()
    return key_bot


def answ_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='💡 ' + POWER_GK[0], callback_data='basic')
    builder.button(text=' 🕯 ' + POWER_GK[1], callback_data='backup')
    builder.adjust(2)
    key_ans = builder.as_markup()
    return key_ans


def ktp_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='⚡ ' + K[0], callback_data=K[0])
    builder.button(text='⚡ ' + K[1], callback_data=K[1])
    builder.button(text='⚡ ' + K[2], callback_data=K[2])
    builder.button(text='⚡ ' + K[3], callback_data=K[3])
    builder.button(text='⚡ ' + K[4], callback_data=K[4])
    builder.adjust(3)
    key_ktp = builder.as_markup()
    return key_ktp


def onf_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='🔻 Включена', callback_data='on')
    builder.button(text='▪ Отключена', callback_data='off')
    builder.adjust(2)
    key_onf = builder.as_markup()
    return key_onf


def stats_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='🕓 Кол-во раб. дней, текущий период', callback_data='worktime')
    builder.button(text='📅 Кол-во раб. дней, предыд. период', callback_data='oldworktime')
    builder.button(text='🚦 Статистика работы КТП за месяц  ', callback_data='ontrans')
    builder.button(text='🚨 Состояние электропитания        ', callback_data='tenkvoff')
    builder.button(text='❎ Закрыть статистику              ', callback_data='statoff')
    builder.adjust(1)
    key_stat = builder.as_markup()
    return key_stat

# print('Keyboards created', '.' * 23)
# admin_kb = InlineKeyboardMarkup()
# adm_kb_1 = InlineKeyboardButton('❎ Статус персонала', callback_data='add_person')
# adm_kb_2 = InlineKeyboardButton('🛑 Статус подстанции', callback_data='trans_stat')
# adm_kb_3 = InlineKeyboardButton('📅 Отмена', callback_data='cancel')
# admin_kb.add(adm_kb_1, adm_kb_2)
#
# ktp_kbrd = InlineKeyboardMarkup()
# ktp_kb_1 = InlineKeyboardButton(K[0], callback_data='160')
# ktp_kb_2 = InlineKeyboardButton(K[1], callback_data='250')
# ktp_kb_3 = InlineKeyboardButton(K[2], callback_data='400')
# ktp_kb_4 = InlineKeyboardButton(K[3], callback_data='630')
# ktp_kb_5 = InlineKeyboardButton(K[4], callback_data='2500')
# ktp_kbrd.add(ktp_kb_1, ktp_kb_2, ktp_kb_3, ktp_kb_4, ktp_kb_5)

# ikb_bot = InlineKeyboardMarkup()
##ib1 = InlineKeyboardButton('🏁 Старт', callback_data='start')
# ib2 = InlineKeyboardButton('⚡ Питание', callback_data='power')
# ib3 = InlineKeyboardButton('👷 Персонал', callback_data='workers')
# ib4 = InlineKeyboardButton('🕋 Подстанции', callback_data='transformers')
##ib5 = InlineKeyboardButton('⚠ Статус ввода', callback_data='statuspower')
##ikb_bot.add(ib1, ib2, ib3).insert(ib4).insert(ib5)
# ikb_bot.add(ib2, ib3, ib4)
