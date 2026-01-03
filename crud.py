from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import bcrypt

from models import User, OTPRequest, AuditLog
from utils import generate_otp, validate_identifier, log_action

MAX_ATTEMPTS = 3
MAX_RESENDS = 3
OTP_EXPIRY_MINUTES = 5
COOLDOWN_MINUTES = 1

def send_otp(db: Session, identifier: str, is_email: bool, trace_id: str):
    log_action(db, "send_otp", "start", f"Validating identifier: {identifier}", trace_id)
    validate_identifier(identifier, is_email)
    
    user = db.query(User).filter(User.identifier == identifier).first()
    if not user:
        log_action(db, "send_otp", "info", "User not found, creating new user", trace_id)
        user = User(identifier=identifier, is_email=is_email)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Invalidate previous OTP if any
    previous_otp = db.query(OTPRequest).filter(OTPRequest.user_id == user.id, OTPRequest.status == "pending").first()
    if previous_otp:
        previous_otp.status = "invalidated"
        db.commit()
    
    otp = generate_otp()
    otp_hash = bcrypt.hashpw(otp.encode(), bcrypt.gensalt()).decode()
    expiry = datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)
    
    otp_request = OTPRequest(user_id=user.id, otp_hash=otp_hash, expiry=expiry)
    db.add(otp_request)
    db.commit()
    
    # Simulate sending (print to console for demo)
    print(f"Simulated OTP send to {identifier}: {otp}")
    log_action(db, "send_otp", "info", "OTP generated and 'sent'", trace_id)
    
    return {"message": "OTP sent successfully"}

def verify_otp(db: Session, identifier: str, otp: str, trace_id: str):
    log_action(db, "verify_otp", "start", f"Verifying OTP for {identifier}", trace_id)
    
    user = db.query(User).filter(User.identifier == identifier).first()
    if not user:
        raise ValueError("User not found")
    
    otp_request = db.query(OTPRequest).filter(OTPRequest.user_id == user.id, OTPRequest.status == "pending").first()
    if not otp_request:
        raise ValueError("No active OTP found")
    
    if datetime.utcnow() > otp_request.expiry:
        otp_request.status = "expired"
        db.commit()
        raise ValueError("OTP expired")
    
    if otp_request.attempts >= MAX_ATTEMPTS:
        otp_request.status = "blocked"
        db.commit()
        raise ValueError("Max attempts reached, OTP blocked")
    
    if not bcrypt.checkpw(otp.encode(), otp_request.otp_hash.encode()):
        otp_request.attempts += 1
        db.commit()
        raise ValueError("Invalid OTP")
    
    otp_request.status = "verified"
    db.commit()
    log_action(db, "verify_otp", "info", "OTP verified", trace_id)
    
    return {"message": "Login successful"}

def resend_otp(db: Session, identifier: str, trace_id: str):
    log_action(db, "resend_otp", "start", f"Resending OTP for {identifier}", trace_id)
    
    user = db.query(User).filter(User.identifier == identifier).first()
    if not user:
        raise ValueError("User not found")
    
    otp_request = db.query(OTPRequest).filter(OTPRequest.user_id == user.id, OTPRequest.status == "pending").first()
    if not otp_request:
        raise ValueError("No active OTP to resend")
    
    if otp_request.resends >= MAX_RESENDS:
        raise ValueError("Max resends reached")
    
    last_resend_time = otp_request.created_at + timedelta(minutes=COOLDOWN_MINUTES * otp_request.resends)
    if datetime.utcnow() < last_resend_time:
        raise ValueError("Cooldown period active, try later")
    
    otp = generate_otp()
    otp_hash = bcrypt.hashpw(otp.encode(), bcrypt.gensalt()).decode()
    otp_request.otp_hash = otp_hash
    otp_request.expiry = datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)
    otp_request.resends += 1
    otp_request.attempts = 0  # Reset attempts on resend
    db.commit()
    
    # Simulate sending
    print(f"Simulated OTP resend to {identifier}: {otp}")
    log_action(db, "resend_otp", "info", "OTP resent", trace_id)
    
    return {"message": "OTP resent successfully"}