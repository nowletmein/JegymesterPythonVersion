from datetime import datetime

def ensure_datetime(value):
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace('Z', '+00:00'))
        except Exception:
            return value
    return value