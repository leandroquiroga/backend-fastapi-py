from datetime import datetime, timezone


# Helper para datetime UTC
def utc_now() -> datetime:
    """Retorna datetime actual en UTC"""
    return datetime.now(timezone.utc)


def logging(message: str, context: str = "INFO") -> None:
    """Imprime los logs con formato fastapi"""
    TEXTO_BLANCO = "\033[97m"
    NEGRITA = "\033[1m"
    RESET = "\033[0m"

    COLOR_MAP = {
        "INFO": "\033[44m",
        "SUCCESS": "\033[42m",
        "WARNING": "\033[43m",
        "ERROR": "\033[41m",
        "REQUEST": "\033[46m",
        "RESPONSE": "\033[45m",
        "DATABASE": "\033[42m",
    }

    CONTEXT_COLORS = COLOR_MAP.get(context.upper(), "\033[44m")
    tag_info = f"{CONTEXT_COLORS}{TEXTO_BLANCO}{NEGRITA} {context:8} {RESET}"
    TABS = " " * 5

    print(f"{TABS}{tag_info} {message}")
