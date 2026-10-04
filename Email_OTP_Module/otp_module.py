import os
import random
import re
import time
import smtplib

from email.mime.text import MIMEText
from dotenv import load_dotenv


# Load .env file
load_dotenv()


# Email status codes
STATUS_EMAIL_OK = 1
STATUS_EMAIL_FAIL = 2
STATUS_EMAIL_INVALID = 3

# OTP status codes
STATUS_OTP_OK = 4
STATUS_OTP_FAIL = 5
STATUS_OTP_TIMEOUT = 6


class EmailOTPModule:
    """Generate, send, and verify email OTPs."""

    def __init__(self):
        self.current_otp = None
        self.otp_time = None
        self.max_attempts = 10

    def start(self):
        self.current_otp = None
        self.otp_time = None

    def close(self):
        self.current_otp = None
        self.otp_time = None

    def validate_email(self, email):
        """Allow only valid Gmail addresses."""
        pattern = r"^[A-Za-z0-9._%+-]+@gmail\.com$"
        return bool(re.fullmatch(pattern, email))

    def send_email(self, email_address, email_body):
        """Send OTP using Gmail SMTP."""

        sender_email = os.getenv("OTP_SENDER_EMAIL")
        sender_password = os.getenv("OTP_APP_PASSWORD")

        if not sender_email:
            print("ERROR: OTP_SENDER_EMAIL is missing in .env")
            return False

        if not sender_password:
            print("ERROR: OTP_APP_PASSWORD is missing in .env")
            return False

        try:
            # Create email
            message = MIMEText(email_body, "plain")
            message["Subject"] = "Your OTP Verification Code"
            message["From"] = sender_email
            message["To"] = email_address

            # Connect to Gmail SMTP
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()

                # Login using Gmail App Password
                server.login(sender_email, sender_password)

                # Send email
                server.sendmail(
                    sender_email,
                    email_address,
                    message.as_string()
                )

            print("OTP email sent successfully to:", email_address)
            return True

        except smtplib.SMTPAuthenticationError:
            print("ERROR: Gmail authentication failed.")
            print("Check your Gmail address and App Password.")
            return False

        except Exception as exc:
            print("ERROR: Email sending failed:", exc)
            return False

    def generate_OTP_email(self, user_email):
        """Generate a 6-digit OTP and send it to the user's Gmail."""

        try:
            # Validate Gmail address
            if not user_email or not self.validate_email(user_email):
                return STATUS_EMAIL_INVALID

            # Generate exactly 6 digits
            self.current_otp = str(random.randint(100000, 999999))

            # Save generation time
            self.otp_time = time.time()

            # Email body
            email_body = (
                "Hello,\n\n"
                f"Your OTP verification code is: {self.current_otp}\n\n"
                "This OTP is valid for 1 minute.\n\n"
                "If you did not request this OTP, please ignore this email.\n\n"
                "Thank you."
            )

            # Send email
            if self.send_email(user_email, email_body):
                return STATUS_EMAIL_OK

            return STATUS_EMAIL_FAIL

        except Exception as exc:
            print("OTP generation error:", exc)
            return STATUS_EMAIL_FAIL

    def check_OTP(self, entered_otp):
        """Check whether the entered OTP is valid."""

        try:
            # No OTP exists
            if self.current_otp is None or self.otp_time is None:
                return STATUS_OTP_FAIL

            # OTP expires after 60 seconds
            if time.time() - self.otp_time >= 60:
                self.current_otp = None
                self.otp_time = None
                return STATUS_OTP_TIMEOUT

            # Correct OTP
            if str(entered_otp).strip() == self.current_otp:
                # OTP is single-use
                self.current_otp = None
                self.otp_time = None
                return STATUS_OTP_OK

            # Wrong OTP
            return STATUS_OTP_FAIL

        except Exception as exc:
            print("OTP checking error:", exc)
            return STATUS_OTP_FAIL