import unittest
from unittest.mock import patch

from otp_module import (
    EmailOTPModule,
    STATUS_EMAIL_OK,
    STATUS_EMAIL_INVALID,
    STATUS_OTP_OK,
    STATUS_OTP_FAIL,
    STATUS_OTP_TIMEOUT,
)


class TestEmailOTP(unittest.TestCase):

    def setUp(self):
        self.otp = EmailOTPModule()

    @patch.object(EmailOTPModule, "send_email", return_value=True)
    def test_valid_gmail(self, mock_send):
        result = self.otp.generate_OTP_email("test@gmail.com")
        self.assertEqual(result, STATUS_EMAIL_OK)
        self.assertIsNotNone(self.otp.current_otp)

    def test_invalid_email(self):
        result = self.otp.generate_OTP_email("test@yahoo.com")
        self.assertEqual(result, STATUS_EMAIL_INVALID)

    @patch.object(EmailOTPModule, "send_email", return_value=True)
    def test_correct_otp(self, mock_send):
        self.otp.generate_OTP_email("test@gmail.com")
        result = self.otp.check_OTP(self.otp.current_otp)
        self.assertEqual(result, STATUS_OTP_OK)

    @patch.object(EmailOTPModule, "send_email", return_value=True)
    def test_wrong_otp(self, mock_send):
        self.otp.generate_OTP_email("test@gmail.com")
        result = self.otp.check_OTP("111111")
        self.assertEqual(result, STATUS_OTP_FAIL)

    @patch.object(EmailOTPModule, "send_email", return_value=True)
    @patch("otp_module.time.time")
    def test_otp_timeout(self, mock_time, mock_send):
        mock_time.side_effect = [1000, 1061]
        self.otp.generate_OTP_email("test@gmail.com")
        result = self.otp.check_OTP("111111")
        self.assertEqual(result, STATUS_OTP_TIMEOUT)


if __name__ == "__main__":
    unittest.main()
