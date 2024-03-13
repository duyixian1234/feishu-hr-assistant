"""Sorage"""

import sqlite3

from config import get_settings


def init_db() -> None:
    """Init DB"""
    with sqlite3.connect(get_settings().db_url) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS data "
            "(timeoff_event_id  CHAR PRIMARY KEY,instance_code CHAR);"
        )
        conn.commit()


def new(timeoff_event_id: str, instance_code: str) -> None:
    """ "New Data"""
    with sqlite3.connect(get_settings().db_url) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO data (timeoff_event_id, instance_code) VALUES (?, ?)""",
            (timeoff_event_id, instance_code),
        )
        conn.commit()


def get_event_id(instance_code: str) -> str:
    """Get Event ID"""
    with sqlite3.connect(get_settings().db_url) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT timeoff_event_id FROM data WHERE instance_code = ?""",
            (instance_code,),
        )
        return cursor.fetchone()[0]
