import imaplib
import email
from email.header import decode_header

# Set up your credentials
username = "mse800pse.aet@gmail.com"
password = "AETabc123"  # Use the app password if 2FA is enabled

# Connect to the Gmail IMAP server
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(username, password)

# Select the mailbox you want to retrieve emails from
mail.select("inbox")

# Search for all emails in the inbox
status, messages = mail.search(None, "ALL")

# Convert the messages to a list of email IDs
email_ids = messages[0].split()

# Fetch the most recent email
latest_email_id = email_ids[-1]

# Fetch the email by ID
status, msg_data = mail.fetch(latest_email_id, "(RFC822)")

for response_part in msg_data:
    if isinstance(response_part, tuple):
        # Parse the email
        msg = email.message_from_bytes(response_part[1])

        # Decode the email subject
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            # If it's a bytes type, decode to str
            subject = subject.decode(encoding if encoding else 'utf-8')

        # Decode the email sender
        from_ = msg.get("From")

        print("Subject:", subject)
        print("From:", from_)

        # If the email message is multipart
        if msg.is_multipart():
            # Iterate over email parts
            for part in msg.walk():
                # Extract the email content type
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" not in content_disposition:
                    if content_type == "text/plain" or content_type == "text/html":
                        # Get the email body
                        body = part.get_payload(decode=True).decode()
                        print("Body:", body)
        else:
            # If the email is not multipart
            body = msg.get_payload(decode=True).decode()
            print("Body:", body)

# Logout from the mailbox
mail.logout()