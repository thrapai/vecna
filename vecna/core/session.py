from ..config import SESSION_FILE
import datetime

import json


def unlock_session():
    """
    Mark the session as unlocked by writing the current timestamp to the session file.
    
    This function creates or updates the session file with the current timestamp,
    indicating that the session is now active and unlocked.
    
    Returns:
        None
    """
    session_data = {
        "unlocked": True,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    with open(SESSION_FILE, 'w') as f:
        json.dump(session_data, f, indent=4)