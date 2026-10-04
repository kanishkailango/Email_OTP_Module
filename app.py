from flask import Flask, jsonify, request, render_template
from otp_module import (
    EmailOTPModule,
    STATUS_EMAIL_OK,
    STATUS_EMAIL_FAIL,
    STATUS_EMAIL_INVALID,
    STATUS_OTP_OK,
    STATUS_OTP_FAIL,
    STATUS_OTP_TIMEOUT,
    
)

app = Flask(__name__)
otp_module = EmailOTPModule()
attempts = 0


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/send-otp", methods=["POST"])
def send_otp():
    global attempts

    try:
        data = request.get_json(silent=True) or {}
        email = data.get("email", "").strip()

        result = otp_module.generate_OTP_email(email)

        if result == STATUS_EMAIL_OK:
            attempts = 0
            # Demo only: the OTP is printed in the VS Code terminal.
            return jsonify({
                "status": "success",
                "message": "OTP sent successfully. Check the VS Code terminal for the demo OTP."
            })

        if result == STATUS_EMAIL_INVALID:
            return jsonify({
                "status": "error",
                "message": "Only a valid @gmail.com address is allowed."
            }), 400

        return jsonify({
            "status": "error",
            "message": "Failed to send OTP."
        }), 500

    except Exception as exc:
        return jsonify({"status": "error", "message": str(exc)}), 500


@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    global attempts

    try:
        if otp_module.current_otp is None:
            return jsonify({
                "status": "error",
                "message": "Please generate a new OTP first."
            }), 400

        if attempts >= 10:
            return jsonify({
                "status": "error",
                "message": "Maximum 10 attempts reached. Generate a new OTP."
            }), 400

        data = request.get_json(silent=True) or {}
        entered_otp = str(data.get("otp", "")).strip()

        if not entered_otp.isdigit() or len(entered_otp) != 6:
            return jsonify({
                "status": "error",
                "message": "OTP must contain exactly 6 digits."
            }), 400

        attempts += 1
        result = otp_module.check_OTP(entered_otp)

        if result == STATUS_OTP_OK:
            attempts = 0
            return jsonify({
                "status": "success",
                "message": "OTP verified successfully."
            })

        if result == STATUS_OTP_TIMEOUT:
            attempts = 0
            return jsonify({
                "status": "error",
                "message": "OTP expired. Please generate a new OTP."
            }), 400

        remaining = 10 - attempts
        return jsonify({
            "status": "error",
            "message": f"Invalid OTP. {remaining} attempts remaining."
        }), 400

    except Exception as exc:
        return jsonify({"status": "error", "message": str(exc)}), 500


if __name__ == "__main__":
    app.run(debug=True)
