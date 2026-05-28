from fastapi import HTTPException
import re



def validate_email(email: str):

    pattern = (
        r"^[A-Za-z0-9._%+-]+"

        r"@[A-Za-z0-9.-]+"

        r"\.[A-Za-z]{2,}$")

    return re.match(
        pattern,
        email)


def validate_phone(phone: str):
    pattern = (
        r"^[6-9]\d{9}$")

    return re.match(
        pattern,
        phone)