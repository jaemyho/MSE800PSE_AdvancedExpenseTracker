import os
import re

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

    # Function to extract transactions
    def extract_transactions(self, statement):
        # Split the statement into lines
        lines = statement.strip().split('\n')

        # Temporary storage for transaction parts and final transaction list
        transaction_lines = []
        transactions = []

        # Helper function to check if the beginning of a line is a valid date
        def is_date(line):
            parts = line.split()
            if len(parts) >= 3:
                try:
                    datetime.strptime(" ".join(parts[:3]), "%d %B %Y")
                    return True
                except ValueError:
                    return False
            return False

        for line in lines:
            # Stop if we reach the end marker
            if "--- End of Transactions ---" in line:
                break

            # Check if line starts with a date
            if is_date(line):
                # Process previous transaction if exists
                if transaction_lines:
                    self.process_transaction(transaction_lines, transactions)
                    transaction_lines = []

            # Accumulate lines for current transaction
            transaction_lines.append(line)

        # Process the last accumulated transaction
        if transaction_lines:
            self.process_transaction(transaction_lines, transactions)

        print("transactions", transactions)

        return transactions

    def process_transaction(self, lines, transactions):
        # Join lines for each transaction
        transaction_text = " ".join(lines)
        parts = list(filter(None, transaction_text.split()))

        if len(parts) < 5:
            # Skip incomplete transactions without printing a message
            return

        try:
            # Extract date
            date = datetime.strptime(" ".join(parts[:3]), "%d %B %Y").date()

            # Find the balance and debit fields by working from the end
            balance = float(parts[-1].replace(",", ""))
            debit_parts = []
            for part in reversed(parts[:-1]):
                if part.replace(",", "").replace(".", "").isdigit():
                    debit_parts.insert(0, part)
                else:
                    break

            # Create debit value and remove .0 if applicable
            debit = float("".join(debit_parts).replace(",", ""))
            debit = int(debit) if debit.is_integer() else debit  # Convert to int if it is a whole number

            # Extract description
            description = " ".join(parts[3:len(parts) - len(debit_parts) - 1])

            # Append the parsed transaction
            transactions.append({
                "Date": date,
                "Description": description,
                "Debit": debit,
                "Balance": balance
            })

        except ValueError:
            # Instead of printing, just skip the transaction
            return


def view_details():
    # Get file path input from user
    file_path = 'uploads/invoice_1.pdf'

    # Ensure the file exists
    if not os.path.exists(file_path):
        print(f"File '{file_path}' does not exist.")
        return

    # Create an instance of the BankStatementReader class
    reader = BankStatementReader(upload_folder=".")

    try:
        # Extract text from the file
        extracted_text = reader.extract_text_from_file(file_path)
        print(extracted_text)

        # Extract transactions from the statement data
        try:
            parsed_transactions = reader.extract_transactions(extracted_text)
            print("parsed_transactions",parsed_transactions)

            # Print the extracted transactions
            print("\nExtracted Transactions:")
            for transaction in parsed_transactions:
                print(transaction)

        except ValueError as e:
            print(e)

    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")




if __name__ == "__main__":

    view_details()
