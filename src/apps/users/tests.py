import smtplib
import os

try:
    with smtplib.SMTP(os.getenv('EMAIL_HOST'), int(os.getenv('EMAIL_PORT'))) as server:
        server.starttls()
        server.login(os.getenv('EMAIL_HOST_USER'), os.getenv('EMAIL_HOST_PASSWORD'))
        print("SMTP connection successful!")
except Exception as e:
    print(f"SMTP connection failed: {e}")