# OTP-Based Login System

## Overview
This is a backend authentication system using OTP for login via email or mobile. It includes OTP generation, verification, resend, and audit logging. OTP is simulated (printed to console) for demo purposes.

## Database Schema
- **users**: id (PK), identifier (unique), is_email (bool)
- **otp_requests**: id (PK), user_id (FK), otp_hash, expiry, attempts, resends, status, created_at
- **audit_logs**: id (PK), api_name, step, status, message, timestamp, trace_id

Run the app to create the DB automatically.

## API Endpoints (Use Postman or /docs)
- **POST /send_otp**: Body: {"identifier": "example@email.com", "is_email": true} → Sends OTP
- **POST /verify_otp**: Body: {"identifier": "example@email.com", "otp": "123456"} → Verifies OTP
- **POST /resend_otp**: Body: {"identifier": "example@email.com"} → Resends OTP

## Sample Data
After running APIs, check `otp.db` using SQLite viewer. Logs and OTP records will be stored there.

## Setup and Run
See instructions in the main guide.