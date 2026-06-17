import re


USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9]+$")
EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def is_valid_username(username: str) -> bool:
    return bool(USERNAME_PATTERN.fullmatch(username or ""))


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_PATTERN.fullmatch(email or ""))
