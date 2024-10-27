import re
import cv2
import os
import numpy as np
from collections import Counter
from pdf2image import convert_from_path
from pytesseract import pytesseract
from datetime import datetime

class ReceiptReader:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = None

    def load_image(self):
        """Load image from file or convert PDF to image."""
        print(f"Loading image from: {self.image_path}")

        if not os.path.isfile(self.image_path):
            raise ValueError(f"File does not exist: {self.image_path}")

        if self.image_path.lower().endswith('.pdf'):
            try:
                images = convert_from_path(self.image_path)
                self.image = images[0]  # Use the first page as the receipt image
            except Exception as e:
                raise ValueError(f"Failed to convert PDF to image: {e}")
        else:
            self.image = cv2.imread(self.image_path)

        if self.image is None:
            raise ValueError(f"Image not found or unable to load: {self.image_path}")

    def preprocess_image(self):
        """Preprocess the image for better OCR accuracy."""
        if self.image is None:
            self.load_image()

        image = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Use GaussianBlur to reduce noise and improve OCR results
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

        # Dilate to make text thicker
        kernel = np.ones((3, 3), np.uint8)
        thresh = cv2.dilate(thresh, kernel, iterations=1)

        return thresh

    def extract_text_from_image(self, image):
        """Extract text from the preprocessed image using Tesseract OCR."""
        custom_config = r'--oem 3 --psm 6'
        extracted_text = pytesseract.image_to_string(image, config=custom_config)
        return extracted_text

    def parse_receipt_data(self, extracted_text):
        """Parse the extracted text to identify vendor, date, items, and total."""
        lines = extracted_text.split('\n')
        items = []
        vendor = None
        currency = None
        date = None

        # Improved regex pattern for date to match various formats
        date_pattern = re.compile(
            r'\b(\d{1,2}(?:[/-])\d{1,2}(?:[/-])\d{2,4}|\d{4}(?:[/-])\d{1,2}(?:[/-])\d{1,2}|'
            r'\d{1,2} (?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|'
            r'Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?) \d{4})\b',
            re.IGNORECASE
        )

        currency_pattern = re.compile(r'(\$|€|¥|£)(\d+(?:\.\d{1,2})?)')

        for line in lines:
            line = line.strip()
            if line:
                # Set vendor as the first non-empty line
                if vendor is None:
                    vendor = line

                # Extract date
                date_match = date_pattern.search(line)
                if date_match:
                    date_str = date_match.group(0)
                    date = self.convert_date_format(date_str)

                    # Extract currency
                currency_match = currency_pattern.search(line)
                if currency_match:
                    currency = currency_match.group(1)

                # Check if the line matches item patterns
                item_price_pattern = re.compile(r'([\w\s]+)\s+(\$|€|¥|£)?\s*([\d,.]+)')
                item_match = item_price_pattern.search(line)

                if item_match:
                    item_name = item_match.group(1).strip()
                    price_str = item_match.group(3)

                    # Debugging statement for the price string
                    print(f"Extracted price string: '{price_str}'")  # Debugging line

                    price = self.clean_price(price_str)  # Clean the price string
                    items.append((item_name, price))

        # Attempt to parse the date string into a date object


        # Extract total amount using specific keyword
        total_pattern = re.compile(r'TOTAL[:\s$€¥£]*([\d,]+(?:\.\d{1,2})?)')
        total_match = total_pattern.search(extracted_text)
        if total_match:
            amount = self.clean_price(total_match.group(1))
        else:
            amount = None
            print("Total amount not found in receipt data.")

        # Categorize items
        categorized_items = self.categorize_items(items)

        return {
            "vendor": vendor,
            "date": date,
            "currency": currency,
            "items": categorized_items,
            "amount": amount,
            "description": 'receipt data'
        }

    def clean_price(self, price_str):
        """Remove commas and currency symbols, then convert to float. Defaults to 0.0 if empty or invalid."""
        # Check if the price string is empty or None
        if not price_str or price_str.strip() == '':
            print("Warning: Empty price string received.")  # Debugging line
            return 0.0

        # Remove any commas, currency symbols, and strip whitespace
        cleaned_str = price_str.replace(',', '').replace('$', '').strip()

        try:
            return float(cleaned_str)
        except ValueError:
            print(f"Warning: Could not convert '{cleaned_str}' to float.")  # Debugging line
            return 0.0  # Default to 0.0 if conversion fails


    def extract_total(self, extracted_text):
        """Extract the total amount from the extracted text."""
        total_pattern = re.compile(
            r'Total\s*:?(\s*\$?\s*([0-9]+(?:[.,][0-9]{1,2})?))|(?:TOTAL\s*:?(\s*\$?\s*([0-9]+(?:[.,][0-9]{1,2})?)))',
            re.IGNORECASE)

        total_match = total_pattern.search(extracted_text)

        if total_match:
            total = total_match.group(1) or total_match.group(3)
            if total:
                total = total.replace("$", "").replace(" ", "").strip()
                total = self.clean_price(total)
            else:
                total = 0.0
        else:
            total = 0.0

        return total

    def categorize_item(self, item_name):
        """Categorize items into major categories."""
        categories = {
            'Food': ['bread', 'apple', 'banana', 'chicken', 'beef', 'vegetable', 'fruit', 'pasta'],
            'Beverages': ['water', 'juice', 'soda', 'milk', 'coffee', 'tea', 'beer', 'wine'],
            'Household': ['detergent', 'soap', 'cleaner', 'paper towels', 'trash bags'],
            'Electronics': ['phone', 'charger', 'battery', 'cable', 'headphones', 'speaker'],
            'Clothing': ['shirt', 'pants', 'dress', 'shoes', 'socks', 'jacket'],
            'Health & Beauty': ['shampoo', 'soap', 'cream', 'toothpaste', 'vitamins'],
            'Office Supplies': ['paper', 'pen', 'pencil', 'notebook', 'stapler'],
            'Groceries': ['rice', 'beans', 'pasta', 'cereal', 'snack'],
            'Others': []
        }

        for category, keywords in categories.items():
            if any(keyword in item_name.lower() for keyword in keywords):
                return category
        return 'Others'

    def convert_date_format(self, date_string):
        possible_formats = [
            '%m/%d/%Y',  # MM/DD/YYYY
            '%d/%m/%Y',  # DD/MM/YYYY
            '%Y-%m-%d',  # YYYY-MM-DD
            '%m/%d/%y',  # MM/DD/YY
            '%d/%m/%y',  # DD/MM/YY
            '%d %B %Y',  # DD Month YYYY (e.g., 11 October 2024)
            '%d %b %Y'  # DD Mon YYYY (e.g., 11 Oct 2024)
        ]
        for fmt in possible_formats:
            try:
                return datetime.strptime(date_string, fmt).strftime('%Y-%m-%d')
            except ValueError:
                continue
        raise ValueError(f"Date format not recognized for date: {date_string}")


    def categorize_items(self, items):
        """Categorize all items into major categories."""
        categorized_items = {}

        # Iterate through the dictionary items
        for category, item_list in items:
            # Check if item_list is indeed a list
            if isinstance(item_list, list):
                for item_name, price in item_list:  # Unpack each tuple
                    # Get the category for the item
                    item_category = self.categorize_item(item_name)
                    # Use setdefault to categorize items
                    categorized_items.setdefault(item_category, []).append((item_name, price))
            else:
                print(f"Expected a list but got {type(item_list)} in category: {category}")

        return categorized_items

    def get_main_category(self, categorized_items):
        """Get the main category based on the number of items."""
        category_counts = Counter({category: len(items) for category, items in categorized_items.items()})
        main_category = category_counts.most_common(1)[0][0] if category_counts else 'Others'
        return main_category

    def read_receipt(self):
        """Read the receipt and extract relevant information."""
        preprocessed_image = self.preprocess_image()
        extracted_text = self.extract_text_from_image(preprocessed_image)
        print("\nRaw Extracted Text:\n", extracted_text)

        receipt_data = self.parse_receipt_data(extracted_text)

        print("\nExtracted Receipt Data:")
        print(f"Vendor: {receipt_data['vendor']}")
        print(f"Date: {receipt_data['date']}")
        print(f"Currency: {receipt_data['currency']}")

        print("\nItems:")
        for item in receipt_data['items']:
            print(f"{item[0]}: ${item[1]:.2f}")

        print(f"\nTotal Amount: ${receipt_data['amount']:.2f}")

        categorized_items = self.categorize_items(receipt_data['items'])
        print("\nCategorized Items:")
        for category, items in categorized_items.items():
            print(f"{category}: {len(items)} item(s)")

        main_category = self.get_main_category(categorized_items)
        print(f"\nMain Category: {main_category}")

        return receipt_data
