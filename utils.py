import random
import string
from datetime import datetime
from sqlalchemy.orm import Session
from email_validator import validate_email, EmailNotValidError
import phonenumbers
from phonenumbers import NumberParseException

from models import AuditLog

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

def validate_identifier(identifier: str, is_email: bool):
    if is_email:
        try:
            validate_email(identifier)
        except EmailNotValidError:
            raise ValueError("Invalid email format")
    else:
        try:
            phone = phonenumbers.parse(identifier)
            if not phonenumbers.is_valid_number(phone):
                raise ValueError("Invalid mobile number")
        except NumberParseException:
            raise ValueError("Invalid mobile number format")

def log_action(db: Session, api_name: str, step: str, message: str, trace_id: str, status: str = "info"):
    log = AuditLog(
        api_name=api_name,
        step=step,
        status=status,
        message=message,
        timestamp=datetime.utcnow(),
        trace_id=trace_id
    )
    db.add(log)
    db.commit()