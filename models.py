from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, unique=True, index=True)
    is_email = Column(Boolean)

class OTPRequest(Base):
    __tablename__ = "otp_requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    otp_hash = Column(String)
    expiry = Column(DateTime)
    attempts = Column(Integer, default=0)
    resends = Column(Integer, default=0)
    status = Column(String, default="pending")  # pending, verified, expired, blocked
    created_at = Column(DateTime, default=func.now())

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    api_name = Column(String)
    step = Column(String)
    status = Column(String)
    message = Column(String)
    timestamp = Column(DateTime, default=func.now())
    trace_id = Column(String)