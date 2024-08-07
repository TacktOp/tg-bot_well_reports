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

    cursor.execute("SELECT * FROM Reports WHERE date(дата) BETWEEN ? AND ?", dates).fetchall()
    rows = cursor

    evotor_nal = 0
    evotor_besnal = 0
    langeim_nal = 0
    terminal_nal = 0
    terminal_besnal = 0
    terminal_sbp = 0
    return_money = 0
    result_money = 0
    for row in rows:
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


def db_get_employee():
    connection = sqlite3.connect("./database/database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT имя FROM Employees")
    rows = cursor.fetchall()

    connection.commit()
    connection.close()

    return rows


def db_delete_employee(name, phone_number):
    connection = sqlite3.connect("./database/database.db")
    cursor = connection.cursor()
    data = (name, phone_number,)

    info = cursor.execute("SELECT * FROM Employees WHERE имя = ? AND номер_телефона = ?", (data)).fetchall()
    if len(info) == 0:
        return False
    else:
        cursor.execute("DELETE FROM Employees WHERE имя = ? AND номер_телефона = ?", (data))

    connection.commit()
    connection.close()


def db_add_employee_report(name):
    connection = sqlite3.connect("./database/database.db")
    cursor = connection.cursor()

    data = (name, 0, datetime.datetime.now().date(), '')

    cursor.execute(
        "INSERT INTO EmployeesReports (админ, количество_смен, дата, задачи) VALUES (?, ?, ?, ?)", data)

    connection.commit()
    connection.close()


def db_update_employee_report(name):
    connection = sqlite3.connect("./database/database.db")
    cursor = connection.cursor()

    current_date = datetime.datetime.now().date()

    cursor.execute("SELECT id, админ, количество_смен, дата FROM EmployeesReports ORDER BY дата DESC")
    rows = cursor.fetchall()

    for row in rows:
        if int(row[3][5:7]) == current_date.month and row[1] == name:
            data = (int(row[2]) + 1, current_date, row[0])
            cursor.execute("UPDATE EmployeesReports SET количество_смен = ?, дата = ? WHERE id = ?", data)
            connection.commit()
            connection.close()
            return
        elif int(row[3][5:7]) <= current_date.month and row[1] == name:
            data = (name, 1, current_date, '')
            cursor.execute("INSERT INTO EmployeesReports (админ, количество_смен, дата, задачи) VALUES (?, ?, ?, ?)",
                           data)
            connection.commit()
            connection.close()
            return


def db_get_employee_report():
    connection = sqlite3.connect("./database/database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM EmployeesReports ORDER BY дата DESC")
    rows = cursor.fetchall()
    rows_2 = db_get_employee()

    data = ""
    for row_2 in rows_2:
        for row in rows:
            if row[1] == row_2[0] and int(row[3][5:7]) == datetime.datetime.now().date().month:
                data += f"Администратор: {row_2[0]}\n" \
                        f"Кол-во смен: {row[2]}\n\n"

    connection.commit()
    connection.close()

    return data
