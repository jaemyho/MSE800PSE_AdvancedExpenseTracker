import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build
from PyPDF2 import PdfFileReader

# Set up Gmail API
"""SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SERVICE_ACCOUNT_FILE = 'path/to/your/service-account-file.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('gmail', 'v1', credentials=credentials)"""

class Emails():
    # Search for invoice emails
    def search_emails(service, query):
        results = service.users().messages().list(userId='me', q=query).execute()
        return results.get('messages', [])

    # Get email content and attachments
    def get_email_content(service, msg_id):
        message = service.users().messages().get(userId='me', id=msg_id).execute()
        parts = message['payload'].get('parts', [])
        for part in parts:
            filename = part['filename']
            if filename:
                data = part['body'].get('data')
                if data:
                    data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                    with open(filename, 'wb') as f:
                        f.write(data)
                    return filename
        return None

    # Read and parse PDF invoice
    def read_pdf(file_path):
        with open(file_path, 'rb') as f:
            reader = PdfFileReader(f)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        return text

    # Example usage
    """query = 'subject:invoice'
    emails = search_emails(service, query)
    for email in emails:
        msg_id = email['id']
        filename = get_email_content(service, msg_id)
        if filename:
            invoice_text = read_pdf(filename)
            print(invoice_text)"""