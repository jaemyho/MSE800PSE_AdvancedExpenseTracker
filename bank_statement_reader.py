import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from datetime import datetime


class BankStatementReader:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from a PDF file."""
        text = ""
        with fitz.open(pdf_path) as pdf_document:
            for page in pdf_document:
                text += page.get_text()
        return text

    def extract_text_from_image(self, image_path):
        """Extract text from an image file using OCR."""
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text

    def extract_text_from_file(self, file_path):
        """Extract text from either PDF or image file."""
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_extension in ['.png', '.jpg', '.jpeg']:
            return self.extract_text_from_image(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    def parse_bank_statement(self, text):
        """Parse the bank statement text and extract relevant details."""
        transactions = []
        lines = text.splitlines()

        # Initialize variables to extract other required details
        start_date = None
        end_date = None
        customer_first_name = None
        customer_last_name = None
        currency = None
        bank_name = None
        total_payment = 0.0

        for line in lines:
            if 'Account Holder' in line:
                # Extract customer names from line
                parts = line.split(':')
                if len(parts) > 1:
                    customer_full_name = parts[1].strip()
                    customer_first_name, customer_last_name = customer_full_name.split(' ', 1)

            if 'Bank Name' in line:
                # Extract bank name from line
                parts = line.split(':')
                if len(parts) > 1:
                    bank_name = parts[1].strip()

            if 'Currency' in line:
                # Extract currency from line
                parts = line.split(':')
                if len(parts) > 1:
                    currency = parts[1].strip()

            if 'Start Date' in line:
                # Extract start date from line
                parts = line.split(':')
                if len(parts) > 1:
                    start_date = datetime.strptime(parts[1].strip(), '%Y-%m-%d')  # Adjust date format if necessary

            if 'End Date' in line:
                # Extract end date from line
                parts = line.split(':')
                if len(parts) > 1:
                    end_date = datetime.strptime(parts[1].strip(), '%Y-%m-%d')  # Adjust date format if necessary

            # Assuming each transaction has a date and an amount, adjust according to your expected format
            transaction_parts = line.split()
            if len(transaction_parts) > 2:
                try:
                    # Assuming the date is the first element and formatted as 'DD Month YYYY'
                    date_str = transaction_parts[0] + " " + transaction_parts[1] + " " + transaction_parts[2]
                    amount_str = transaction_parts[-1]  # Assuming amount is the last element
                    amount = float(amount_str.replace(',', '').replace('$', ''))  # Adjust according to currency format
                    total_payment += amount
                    # Attempt to parse the transaction date
                    transaction_date = datetime.strptime(date_str, '%d %B %Y')  # Adjust date format if necessary

                    # Append transaction
                    transactions.append({'date': transaction_date, 'amount': amount})

                    # Determine start and end dates
                    if start_date is None or transaction_date < start_date:
                        start_date = transaction_date
                    if end_date is None or transaction_date > end_date:
                        end_date = transaction_date


                except ValueError:
                    continue  # Handle parsing error
            # Format start_date and end_date to remove time
        start_date_str = start_date.strftime('%Y-%m-%d') if start_date else None
        end_date_str = end_date.strftime('%Y-%m-%d') if end_date else None
        return {
            'transactions': transactions,
            'total_payment': total_payment,
            'start_date': start_date_str,
            'end_date': end_date_str,
            'customer_first_name': customer_first_name,
            'customer_last_name': customer_last_name,
            'currency': currency,
            'bank_name': bank_name
        }


def view_details():
    # Get file path input from user
    file_path =  'uploads/invoice_1.pdf'

    # Ensure the file exists
    if not os.path.exists(file_path):
        print(f"File '{file_path}' does not exist.")
        return

    # Create an instance of the BankStatementReader class
    reader = BankStatementReader(upload_folder=".")

    try:
        # Extract text from the file
        extracted_text = reader.extract_text_from_file(file_path)

        # Parse the extracted text
        parsed_data = reader.parse_bank_statement(extracted_text)

        # Display the parsed information
        print("\nParsed Bank Statement Data:")
        print(f"Customer Name: {parsed_data['customer_first_name']} {parsed_data['customer_last_name']}")
        print(f"Bank Name: {parsed_data['bank_name']}")
        print(f"Currency: {parsed_data['currency']}")
        print(f"Statement Period: {parsed_data['start_date']} to {parsed_data['end_date']}")
        print(f"Total Payment: {parsed_data['total_payment']}")
        print("\nTransactions:")
        for transaction in parsed_data['transactions']:
            print(f"- Date: {transaction['date']}, Amount: {transaction['amount']}")

    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    view_details()
