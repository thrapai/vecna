from ..config import SESSION_FILE
import os
import datetime

import json


def create_session():
    session_data = {"unlocked": True, "timestamp": datetime.datetime.now().isoformat()}

    if os.path.exists(SESSION_FILE):
        os.chmod(SESSION_FILE, 0o600)

    with open(SESSION_FILE, "w") as f:
        json.dump(session_data, f, indent=4)
    os.chmod(SESSION_FILE, 0o400)


def end_session():
    if not os.path.exists(SESSION_FILE):
        return None
    os.chmod(SESSION_FILE, 0o600)
    os.remove(SESSION_FILE)
