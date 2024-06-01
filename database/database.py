import sqlite3
import datetime


def db_add_new_report(
        shift_type,
        date,
        admin_day,
        admin_night,
        admin_intermediate,
        evotor_nal,
        evotor_besnal,
        lanheim_nal,
        lanheim_besanl,
        return_evotor,
        return_lanheim,
        total
):
    connection = sqlite3.connect("./database/database.db")
    cursor = connection.cursor()

    data = (shift_type,
            date,
            admin_day,
            admin_night,
            admin_intermediate,
            evotor_nal,
            evotor_besnal,
            lanheim_nal,
            lanheim_besanl,
            return_evotor,
            return_lanheim,
            total)

    cursor.execute(
        "INSERT INTO Reports ("
        "тип_смены,"
        "дата,"
        "админ_дневной,"
        "админ_ночной,"
        "админ_промежуточный,"
        "эвотор_нал,"
        "эвотор_безнал,"
        "лангейм_нал,"
        "лангейм_безанл,"
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
    langeim_besnal = 0
    vozvrat = 0
    itog = 0
    for row in rows:
        print(row)
        evotor_nal = evotor_nal + row[6]
        evotor_besnal = evotor_besnal + row[7]
        langeim_nal = langeim_nal + row[8]
        langeim_besnal = langeim_besnal + row[9]
        vozvrat = vozvrat + row[10] + row[11]
        itog = itog + row[12] - (row[10] + row[11])

    connection.commit()
    connection.close()

    result = f"Эвотор нал: {evotor_nal}\n" \
             f"Эвотор безнал: {evotor_besnal}\n" \
             f"Лангейм нал: {langeim_nal}\n" \
             f"Лангейм безнал: {langeim_besnal}\n" \
             f"Возвраты: {vozvrat}\n" \
             f"Итоги: {itog}"

    return result
