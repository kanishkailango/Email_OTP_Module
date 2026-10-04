import requests
import streamlit as st

st.title("Email OTP Verification")

st.write("Enter a Gmail address to generate an OTP.")

email = st.text_input("Gmail address")
otp = st.text_input("6-digit OTP", max_chars=6)

if st.button("Send OTP"):
    try:
        response = requests.post(
            "http://127.0.0.1:5000/send-otp",
            json={"email": email},
            timeout=5,
        )
        st.write(response.json()["message"])
    except requests.RequestException:
        st.error("Start the Flask app first: python app.py")

if st.button("Verify OTP"):
    try:
        response = requests.post(
            "http://127.0.0.1:5000/verify-otp",
            json={"otp": otp},
            timeout=5,
        )
        data = response.json()

        if response.ok:
            st.success(data["message"])
        else:
            st.error(data["message"])

    except requests.RequestException:
        st.error("Start the Flask app first: python app.py")
