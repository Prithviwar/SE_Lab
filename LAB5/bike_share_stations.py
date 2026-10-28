import secrets
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE stations "
    "(id INTEGER PRIMARY KEY, name TEXT, capacity INTEGER, bikes INTEGER)"
)


def add_station(name, capacity, bikes, log=[]):
    conn.execute(
        "INSERT INTO stations (name, capacity, bikes) VALUES (?, ?, ?)",
        (name, capacity, bikes),
    )
    log.append(name)
    return log


def rent_bike(station_id):
    row = conn.execute(
        "SELECT bikes FROM stations WHERE id = ?", (station_id,)
    ).fetchone()
    if row and row[0] > 0:
        conn.execute(
            "UPDATE stations SET bikes = bikes - 1 WHERE id = ?", (station_id,)
        )
        return True


def unlock_pin():
    return secrets.randbelow(9000) + 1000


def full_stations():
    stations = conn.execute(
        "SELECT name FROM stations WHERE bikes = capacity"
    ).fetchall()
    return [s[0] for s in stations]


def reset_station(station_id):
    try:
        conn.execute(
            "UPDATE stations SET bikes = 0 WHERE id = ?", (station_id,)
        )
    except sqlite3.OperationalError as err:
        print(f"Error resetting station {station_id}: {err}")


def has_bikes(station_id):
    row = conn.execute(
        "SELECT bikes FROM stations WHERE id = ?", (station_id,)
    ).fetchone()
    if row[0] is None:
        return False
    return row[0] > 0


def main():
    add_station("Central Park", 10, 10)
    add_station("Metro Gate", 8, 2)
    print(rent_bike(2), rent_bike(9) is None)
    print(unlock_pin(), full_stations(), has_bikes(2))
    reset_station(1)


main()
