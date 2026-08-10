import os
import re

from django.conf import settings


SESSION_DB_DIR = os.path.join(
    settings.BASE_DIR,
    "session_database"
)

def get_session_db(session_key):

    if not session_key:
        raise ValueError("Session key required.")

        safe_key = re.sub(r"[^a-zA-A0-9_-]", "", session_key)
        return f"session_{safe_key}.db"


def get_session_db_path(session_key):

    os.makedirs(SESSION_DB_DIR, exist_ok=True)

    db_name = get_session_db(session_key)

    return os.path.join(
        SESSION_DB_DIR,
        db_name
    )


def session_db_exists(session_key):

    return os.path.exists(
        get_session_db_path(session_key)
    )


def delete_session_db(session_key):

    db_path = get_session_db_path(session_key)

    if os.path.exists(db_path):
        os.remove(db_path)