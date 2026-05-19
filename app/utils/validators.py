from fastapi import HTTPException
import re
def validate_mobile(mobile_number: str):
    if not mobile_number:
        raise HTTPException(status_code=400, detail="Mobile number required")

    # Indian mobile validation (10 digit, starts 6-9, optional +91)
    if not re.fullmatch(r"^(\+91)?[6-9]\d{9}$", mobile_number):
        raise HTTPException(
            status_code=400,
            detail="Mobile number must be a valid 10-digit Indian number",
        )
