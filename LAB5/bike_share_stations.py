"""Bike Share Station Management System.

Provides database interaction and utility functions to manage bike rentals,
station statuses, and security PIN generations.
"""

import secrets
import sqlite3
from typing import List, Optional, Tuple

CONN = sqlite3.connect(":memory:")
CONN.execute(
    "CREATE TABLE stations "
    "(id INTEGER PRIMARY KEY, name TEXT, capacity INTEGER, bikes INTEGER)"
)


def add_station(
    name: str, capacity: int, bikes: int, log: Optional[List[str]] = None
) -> List[str]:
    """Add a new bike station safely using parameterized SQL queries."""
    if log is None:
        log = []

    CONN.execute(
        "INSERT INTO stations (name, capacity, bikes) VALUES (?, ?, ?)",
        (name, capacity, bikes),
    )
    log.append(name)
    return log


def rent_bike(station_id: int) -> bool:
    """Rent a bike from a station if bikes are available."""
    row: Optional[Tuple[int]] = CONN.execute(
        "SELECT bikes FROM stations WHERE id = ?", (station_id,)
    ).fetchone()

    if row and row[0] > 0:
        CONN.execute(
            "UPDATE stations SET bikes = bikes - 1 WHERE id = ?", (station_id,)
        )
        return True
    return False


def unlock_pin() -> int:
    """Generate a cryptographically secure 4-digit PIN."""
    return secrets.randbelow(9000) + 1000


def full_stations() -> List[str]:
    """Return names of all stations that are at maximum capacity."""
    stations = CONN.execute(
        "SELECT name FROM stations WHERE bikes = capacity"
    ).fetchall()
    return [s[0] for s in stations]


def reset_station(station_id: int) -> None:
    """Reset available bikes count for a station to zero."""
    try:
        CONN.execute(
            "UPDATE stations SET bikes = 0 WHERE id = ?", (station_id,)
        )
    except sqlite3.OperationalError as err:
        print(f"Failed to reset station {station_id}: {err}")


def has_bikes(station_id: int) -> bool:
    """Check if a station currently has available bikes."""
    row = CONN.execute(
        "SELECT bikes FROM stations WHERE id = ?", (station_id,)
    ).fetchone()

    if row is None or row[0] is None:
        return False
    return row[0] > 0


def main() -> None:
    """Execute main demonstration logic."""
    add_station("Central Park", 10, 10)
    add_station("Metro Gate", 8, 2)
    print(rent_bike(2), rent_bike(9) is None)
    print(unlock_pin(), full_stations(), has_bikes(2))
    reset_station(1)


if __name__ == "__main__":
    main()
