
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



# SMTP server configuration
smtp_host = "smtp.gmail.com"
smtp_port = 587
smtp_user = "biaravet@gmail.com"
smtp_pass = "bxtgwmoqdqopfbhq"


def send_email(recipient_email, html_content, subject):
    # Email setup
    sender_email = "biaravet@gmail.com"
    # smtp_host = "your_smtp_host"  # e.g., smtp.gmail.com
    # smtp_port = 587  # Typical port for TLS
    # smtp_user = sender_email
    # smtp_pass = "your_smtp_password"

    # Create the email message
    msg = MIMEMultipart("alternative")  # Using 'alternative' for HTML and text parts
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the HTML content as part of the email body
    part = MIMEText(html_content, 'html')
    msg.attach(part)

    # Send the email using SMTP server
    try:
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()  # Secure connection using TLS
            server.login(smtp_user, smtp_pass)  # Log in to the SMTP server
            server.sendmail(sender_email, recipient_email, msg.as_string())  # Send the email
            return "Email sent successfully!"
    except Exception as e:
        return f"Error sending email: {e}"