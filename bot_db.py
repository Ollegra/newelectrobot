import sqlite3 as sq
import datetime
from config import W, K, COD_SM, POWER_GK
#import csv
import logging

num_sql = 0

logger3 = logging.getLogger(__name__)
logger3.setLevel(logging.INFO)
handler3 = logging.FileHandler(f"{__name__}.log")
formatter3 = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler3.setFormatter(formatter3)
logger3.addHandler(handler3)

logger3.info(f'DB created for module {__name__}...')


def db_start():
    global db, cur
    db = sq.connect('electro.db')
    db.row_factory = sq.Row
    cur = db.cursor()

    if db:
        logger3.info(f'DataBases conected for module {__name__}...')
    cur.execute(
        "CREATE TABLE IF NOT EXISTS people(id INTEGER PRIMARY KEY AUTOINCREMENT, person TEXT, datat TEXT, cod TEXT, cat TEXT)")
    db.commit()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS transf(id INTEGER PRIMARY KEY AUTOINCREMENT, person TEXT, datat TEXT, cod TEXT, cat TEXT, timex TEXT, timem TEXT, timed INTEGER)")
    db.commit()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS powers(id INTEGER PRIMARY KEY AUTOINCREMENT, datat TEXT, powers TEXT, timex TEXT)")
    db.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY AUTOINCREMENT, datat TEXT, task TEXT)")
    db.commit()
    cur.close()



def people_add(work, kat):
    data = datetime.datetime.today().strftime("%Y-%m-%d")
    cur = db.cursor()
    if kat == 'p':
        list = work.split(' ')
        for i in range(len(W)):
            cur.execute("INSERT INTO people (person, datat, cod, cat) VALUES(?, ? ,?, ?)",
                        (W[i], data, list[i], kat))
        db.commit()
        logger3.info(f'People ({kat}) in {data} edit...')
    elif kat == 't':
        list = work.split(' ')
        for i in range(len(K)):
            cur.execute("INSERT INTO transf (person, datat, cod, cat, timex, timem, timed) VALUES(?, ? ,?, ?, ?, ?, ?)", (K[i], data, list[i], kat, ' ', ' ', 0))
        db.commit()
        logger3.info(f'Transformator ({kat}) in {data} edit...')
    cur.close()


def trans_update(ktp, onf):
    data = datetime.datetime.today().strftime("%Y-%m-%d")
    xtime = (datetime.datetime.today() + datetime.timedelta(hours=2)).strftime("%H:%M")
    ttt = 't'
    if onf == 'off':
        cur = db.cursor()
        onetimes = cur.execute("SELECT timex FROM transf WHERE datat = ? AND person = ?", (data, ktp)).fetchall()[0][0]
        db.commit()
        zdelta = str(datetime.datetime.strptime(xtime, "%H:%M") - datetime.datetime.strptime(
            onetimes, "%H:%M"))
        eddelta = zdelta.split(':')
        tdelta = int(eddelta[0]) * 60 + int(eddelta[1])
        cur.execute("UPDATE transf SET cod = ?, timem = ?, timed = ? WHERE datat = ? AND person = ?", (onf, xtime, tdelta, data, ktp))
        
        db.commit()
        logger3.info(f'Transformator {ktp} OFF - {xtime}, total time {tdelta}...')
    else:
        cur = db.cursor()
        cur.execute("UPDATE transf SET cod = ?, cat = ?, timex = ? WHERE datat = ? AND person = ?", (onf, 'w', xtime, data, ktp))
        db.commit()
        logger3.info(f'Transformator {ktp} ON - {xtime}...')
    cur.close()


def people_get():
    cur = db.cursor()
    txtpeople = '<b>👷 Наличие персонала</b>' + '\n'
    for ret in cur.execute("SELECT person, cod FROM people WHERE datat = date()").fetchall():
        txtpeople += f'<code>{ret[0].ljust(16)}</code> {COD_SM[ret[1]]}\n'
    cur.close()
    return txtpeople


def trans_get():
    cur = db.cursor()
    txtpeople = '<b>🕋 Состояние КТП</b>' + '\n'
    for ret in cur.execute("SELECT person, cod, timex, timem FROM transf WHERE datat = date()").fetchall():
        txtpeople += f'<code>{ret[0].ljust(11)}</code> {COD_SM[ret[1]]}  <code>{ret[2]}</code>  <code>{ret[3]}</code>\n'
    cur.close()
    return txtpeople


def power_add(powered):
    data = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")
    xtime = datetime.datetime.today().strftime("%H:%M")
    cur = db.cursor()
    cur.execute('INSERT INTO powers (datat, powers, timex) VALUES(?, ?, ?)', (data, powered, xtime))
    db.commit()
    cur.close()


def db_get_pow():
    cur = db.cursor()
    txtpower = cur.execute("SELECT powers FROM powers ORDER BY datat DESC LIMIT 1").fetchall()[0][0]
    cur.close()
    return txtpower


def task_add(newtask):
    data = datetime.datetime.today().strftime("%Y-%m-%d")
    tasks = newtask[:50]
    cur = db.cursor()
    cur.execute("INSERT INTO tasks (datat, task) VALUES(?, ?)", (data, tasks))
    db.commit()
    logger3.info(f'New task in {data} adding...')
    cur.close()


def task_get():
    txttask = '<b>📖 Задачи на сегодня</b>\n'
    cur = db.cursor()
    for ret in cur.execute("SELECT task FROM tasks WHERE datat = date()").fetchall():
        txttask += f'⚡ <i>{ret[0]}</i>\n'
    cur.close()
    return txttask


def people_stat():
    cods, dats = 'yes', datetime.datetime.today().strftime("%Y-%m-%d")
    txtstat = '<b>📅 Кол-во рабочих дней за текущий месяц</b>\n'
    cur = db.cursor()
    for ret in cur.execute(
            "SELECT person, COUNT(*) FROM people WHERE cod = ? AND datat BETWEEN date(?, 'start of month') AND date('now') GROUP BY person",
            (cods, dats)).fetchall():
        txtstat += f'<code>{ret[0].ljust(16)} {str(ret[1]).rjust(3)} дн.</code>\n'

    cur.close()
    return txtstat
    # print(txtstat)

def oldpeople_stat():
    cods, dats = 'yes', datetime.datetime.today().strftime("%Y-%m-%d")
    txtstat = '<b>📅 Кол-во рабочих дней за предыдущий месяц</b>\n'
    cur = db.cursor()
    for ret in cur.execute(
            "SELECT person, COUNT(*) FROM people WHERE cod = ? AND datat BETWEEN date(?, 'start of month', '-1 month') AND date(?, 'start of month', '-1 days') GROUP BY person",
            (cods, dats, dats)).fetchall():
        txtstat += f'<code>{ret[0].ljust(16)} {str(ret[1]).rjust(3)} дн.</code>\n'

    cur.close()
    return txtstat


def trans_stat():
    cats, dats = 'w', datetime.datetime.today().strftime("%Y-%m-%d")
    txtstat = '<b>🛑 Количество включений КТП за месяц</b>\n'
    cur = db.cursor()
    for ret in cur.execute(
            "SELECT person, COUNT(*), SUM(timed) FROM transf WHERE cat = ? AND datat BETWEEN date(?, 'start of month') AND date('now') GROUP BY person",
            (cats, dats)).fetchall():
        txtstat += f'<code>{ret[0].ljust(9)} {str(ret[1]).rjust(2)}, {str(ret[2] // 60).rjust(3)} час. {str(ret[2] % 60).rjust(2)} мин.</code>\n'

    cur.close()
    return txtstat


def powers_stat():
    # dats = datetime.datetime.today().strftime("%Y-%m-%d")
    txtstat = '<b>⚡⚡ Работа дизель-генератора за месяц</b>\n'
    cur = db.cursor()
    # for ret in cur.execute("SELECT powers, datat FROM powers WHERE datat BETWEEN date(?, 'start of month') AND date('now')", (dats)).fetchall():
    for ret in cur.execute("SELECT powers, datat FROM powers ORDER BY datat LIMIT 10").fetchall():
        txtstat += f'<code>{ret[0]} {ret[1]}</code>\n'

    cur.close()
    return txtstat


# SELECT person, COUNT(cod) FROM person WHERE cat = 'p' AND cod = 'yes' AND datat BETWEEN date('2023-07-04', 'start of month') AND date('now') GROUP BY person ORDER BY datat
# SELECT person, COUNT(cod) FROM person WHERE cat = 't' AND cod = 'off' AND NOT timex = ' ' AND datat BETWEEN date('2023-07-04', 'start of month') AND date('now') GROUP BY person ORDER BY datat
# SELECT person, cod, datat, timex FROM person WHERE cat = 't' AND datat BETWEEN date('2023-07-04', 'start of month') AND date('now') ORDER BY datat
# SELECT person, cod, datat, timex FROM person WHERE cat = 't' AND NOT timex = ' ' AND datat BETWEEN date('2023-07-04', 'start of month') AND date('now') ORDER BY datat
# SELECT powers, datat FROM powers ORDER BY datat LIMIT 3
# SELECT user_id, user_name, MAX(data) FROM analytic GROUP BY user_id
# SELECT * From table ORDER BY data DESC LIMIT 1
