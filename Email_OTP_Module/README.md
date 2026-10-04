# Email OTP Module - Technical Assessment

This project implements the Email OTP requirements from the assessment.

## Features

- OOP-based `EmailOTPModule` class
- 6-digit random OTP
- Only `@gmail.com` addresses are accepted
- OTP expires after 1 minute
- Maximum 10 verification attempts
- Flask REST API
- Simple HTML/CSS UI
- Optional Streamlit UI
- PostgreSQL connection placeholder
- Exception handling
- Unit tests
- Security placeholder for database credentials

## 1. Open in VS Code

Open this folder in Visual Studio Code.

## 2. Create virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

## 3. Install packages

```bash
pip install -r requirements.txt
```

## 4. Run Flask

```bash
python app.py
```

Open:

http://127.0.0.1:5000

## 5. Test the OTP

1. Enter an address such as `yourname@gmail.com`.
2. Click **Send OTP**.
3. Look at the VS Code terminal.
4. The demo email and OTP will be printed there.
5. Enter the 6-digit OTP in the webpage.
6. Click **Verify OTP**.

### Important

This project uses a demo `send_email()` function because the assessment says that this function can be assumed to be implemented.

For a real application, connect it to SMTP or an email provider.

## 6. Run unit tests

From the project root:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

or:

```bash
pytest
```

## 7. Streamlit UI (optional)

Keep Flask running in one terminal.

Open a second VS Code terminal:

```bash
streamlit run streamlit_app.py
```

The Streamlit page will open in your browser.

## 8. PostgreSQL

The file `database.py` contains the PostgreSQL connection and table creation code.

Set environment variables instead of putting real credentials in the code:

```text
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
```

The current OTP demo does not require PostgreSQL to run the Flask UI.

## How to explain the project

"The EmailOTPModule class is responsible for generating and validating OTPs. First it validates the Gmail address. Then it generates a six-digit OTP and stores the generation time. The OTP is valid for one minute and the user has a maximum of ten attempts. Flask exposes the module through REST APIs, while the HTML page provides a simple user interface. Unit tests check valid emails, invalid emails, correct OTPs, wrong OTPs and timeout behavior."

## Security improvements for production

- Store credentials in environment variables or a secret manager.
- Never log the OTP in production.
- Store only a hashed OTP if persistence is required.
- Add rate limiting.
- Use HTTPS.
- Associate OTP attempts with the specific user/email.
