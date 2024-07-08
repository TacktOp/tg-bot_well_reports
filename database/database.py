import sqlite3
import datetime


def db_add_report(
        shift_type,
        date,
        admin,
        evotor_nal,
        evotor_besnal,
        lanheim_nal,
        terminal_nal,
        terminal_besnal,
        terminal_sbp,
        return_evotor,
        return_lanheim,
        total
):
    connection = sqlite3.connect("./database/database.db")
    cursor = connection.cursor()

    data = (
        shift_type,
        date,
        admin,
        evotor_nal,
        evotor_besnal,
        lanheim_nal,
        terminal_nal,
        terminal_besnal,
        terminal_sbp,
        return_evotor,
        return_lanheim,
        total
    )

    cursor.execute(
        "INSERT INTO Reports ("
        "тип_смены,"
        "дата,"
        "админ,"
        "эвотор_нал,"
        "эвотор_безнал,"
        "лангейм_нал,"
        "терминал_нал,"
        "терминал_безнал,"
        "терминал_сбп,"
        "возврат_эвотор,"
        "возврат_лангейм,"
        "итого"
        ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data
    )

    connection.commit()
    connection.close()


def db_get_report_money(dates):
    connection = sqlite3.connect("./database/database.db")
    cursor = connection.cursor()

    dates = (
        f"{datetime.datetime.now().year}-{dates[0]}",
        f"{datetime.datetime.now().year}-{dates[1]}"
    )

    cursor.execute("SELECT * FROM Reports WHERE date(дата) BETWEEN ? AND ?", dates)
    rows = cursor.fetchall()

    evotor_nal = 0
    evotor_besnal = 0
    langeim_nal = 0
    terminal_nal = 0
    terminal_besnal = 0
    terminal_sbp = 0
    return_money = 0
    result_money = 0
    for row in rows:
        print(row)
        evotor_nal = evotor_nal + row[4]
        evotor_besnal = evotor_besnal + row[5]
        langeim_nal = langeim_nal + row[6]
        terminal_nal = terminal_nal + row[7]
        terminal_besnal = terminal_besnal + row[8]
        terminal_sbp = terminal_sbp + row[9]
        return_money = return_money + row[10] + row[11]
        result_money = result_money + row[12] - (row[10] + row[11])

    connection.commit()
    connection.close()

    result = f"Эвотор нал: {evotor_nal}\n" \
             f"Эвотор безнал: {evotor_besnal}\n\n" \
             f"Лангейм нал: {langeim_nal}\n\n" \
             f"Терминал нал: {terminal_nal}\n" \
             f"Терминал безнал: {terminal_besnal}\n" \
             f"Терминал СБП: {terminal_sbp}\n\n" \
             f"Возвраты: {return_money}\n\n" \
             f"Итоги: {result_money}"

    return result


def db_add_employee(shift_type, name, phone_number):
    connection = sqlite3.connect("./database/database.db")
    cursor = connection.cursor()
    data = (shift_type, name, phone_number)

    cursor.execute("INSERT INTO Employees (тип_смены, имя, номер_телефона) VALUES (?, ?, ?)", data)

    connection.commit()
    connection.close()
