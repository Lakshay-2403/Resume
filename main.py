from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from database import get_db
from schemas import SendOTPRequest, VerifyOTPRequest, ResendOTPRequest
from crud import send_otp, verify_otp, resend_otp
from utils import log_action

app = FastAPI(title="OTP-Based Login System")

@app.post("/send_otp")
def send_otp_endpoint(request: SendOTPRequest, db: Session = Depends(get_db)):
    trace_id = str(uuid.uuid4())
    try:
        result = send_otp(db, request.identifier, request.is_email, trace_id)
        log_action(db, "send_otp", "success", "OTP sent successfully", trace_id)
        return result
    except Exception as e:
        log_action(db, "send_otp", "failure", str(e), trace_id)
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/verify_otp")
def verify_otp_endpoint(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    trace_id = str(uuid.uuid4())
    try:
        result = verify_otp(db, request.identifier, request.otp, trace_id)
        log_action(db, "verify_otp", "success", "OTP verified successfully", trace_id)
        return result
    except Exception as e:
        log_action(db, "verify_otp", "failure", str(e), trace_id)
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/resend_otp")
def resend_otp_endpoint(request: ResendOTPRequest, db: Session = Depends(get_db)):
    trace_id = str(uuid.uuid4())
    try:
        result = resend_otp(db, request.identifier, trace_id)
        log_action(db, "resend_otp", "success", "OTP resent successfully", trace_id)
        return result
    except Exception as e:
        log_action(db, "resend_otp", "failure", str(e), trace_id)
        raise HTTPException(status_code=400, detail=str(e))
    
    from database import Base, engine
    Base.metadata.create_all(bind=engine)