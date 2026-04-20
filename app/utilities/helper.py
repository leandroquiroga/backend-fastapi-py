from datetime import datetime, timezone

# Helper para datetime UTC
def utc_now() -> datetime:
    """Retorna datetime actual en UTC"""
    return datetime.now(timezone.utc)
