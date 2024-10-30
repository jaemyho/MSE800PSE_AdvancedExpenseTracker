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
            'Food': ['food', 'meal', 'dinner', 'lunch', 'breakfast'],
            'Groceries': ['grocery', 'supermarket', 'market', 'food store'],
            'Entertainment': ['movie', 'concert', 'show', 'theater', 'entertainment'],
            'Subscriptions': ['subscription', 'monthly', 'annual fee', 'service'],
            'Rental': ['rental', 'lease', 'rent'],
            'Tax': ['tax', 'taxes', 'tax preparation'],
            'Insurance': ['insurance', 'policy', 'coverage'],
            'Medical': ['doctor', 'medical', 'health', 'pharmacy'],
            'Education': ['tuition', 'class', 'course', 'school'],
            'Investments': ['investment', 'stocks', 'bonds'],
            'Transportation': ['transportation', 'taxi', 'bus', 'train', 'uber'],
            'Accommodation': ['hotel', 'motel', 'stay', 'lodging'],
            'Clothings': ['clothing', 'apparel', 'fashion', 'shoes', 'wear'],
            'Events': ['event', 'conference', 'meeting', 'gathering'],
        }

        if isinstance(item_name, str):
            item_name = item_name.lower()
            for category, keywords in categories.items():
                if any(keyword in item_name for keyword in keywords):
                    return category
        else:
            print("Item name is not a string:", item_name)

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

    def extract_description(self, extracted_text):
        """Extract a short description from the extracted text."""
        # Split the extracted text into lines
        lines = extracted_text.split('\n')
        description_lines = []

        # Iterate through the lines to find the most relevant descriptions
        for line in lines:
            line = line.strip()
            if line and not line.startswith(('TOTAL', 'DATE', 'TIME', 'VENDOR', 'ITEMS')):  # Filter out header lines
                description_lines.append(line)

        # Join the first few relevant lines to form the description
        description = ' '.join(description_lines[:3])  # Adjust the number as needed for a concise description
        return description.replace(",", "").strip()

    def extract_shop_name(self,extracted_text):
        # This method does not take any parameters, it uses self.receipt_text
        shop_name_pattern = r'^[^\d]+'  # Match from the start of the string until a number is encountered
        match = re.search(shop_name_pattern,extracted_text)
        return match.group(0).strip() if match else 'Unknown'

    def get_category_from_receipt(self,extracted_text):
        categories = {
            'Food': r'\b(food|meal|dinner|lunch|breakfast|cafe|restaurant|bar|coffee|snack|breakfast)\b',
            'Groceries': r'\b(grocery|supermarket|market|produce|food store|shop|groceries)\b',
            'Entertainment': r'\b(movie|concert|show|theater|entertainment|event|game)\b',
            'Subscriptions': r'\b(subscription|monthly|annual|service|membership)\b',
            'Rental': r'\b(rental|lease|rent|hire)\b',
            'Tax': r'\b(tax|taxes|tax preparation|filing)\b',
            'Insurance': r'\b(insurance|policy|coverage|premium)\b',
            'Medical': r'\b(doctor|medical|health|pharmacy|hospital|clinic)\b',
            'Education': r'\b(tuition|class|course|school|college|university)\b',
            'Investments': r'\b(investment|stocks|bonds|fund)\b',
            'Transportation': r'\b(transportation|taxi|bus|train|fare|uber|lyft|travel)\b',
            'Accommodation': r'\b(hotel|motel|stay|lodging|resort|inn)\b',
            'Clothing': r'\b(clothing|apparel|fashion|shoes|wear|attire)\b',
            'Events': r'\b(event|conference|meeting|gathering|celebration)\b',
        }

        # Check each category with regex
        for category, pattern in categories.items():
            if re.search(pattern, extracted_text):
                return category  # Return the first matching category

        return 'Others'  # Default category if no match is found

    def read_receipt(self,extracted_text):
        """Read the receipt and extract relevant information."""
        preprocessed_image = self.preprocess_image()
        extracted_text = self.extract_text_from_image(preprocessed_image)
        print("\nRaw Extracted Text:\n", extracted_text)

        receipt_data = self.parse_receipt_data(extracted_text)

        # Extract the description
        description = self.extract_description(extracted_text)

        print("\nExtracted Receipt Data:")
        print(f"Vendor: {receipt_data['vendor']}")
        print(f"Date: {receipt_data['date']}")
        print(f"Currency: {receipt_data['currency']}")
        print(f"Description: {description}")  # Display the extracted description

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

    # def read_receipt(self):
    #     """Read the receipt and extract relevant information."""
    #     preprocessed_image = self.preprocess_image()
    #     extracted_text = self.extract_text_from_image(preprocessed_image)
    #     print("\nRaw Extracted Text:\n", extracted_text)
    #
    #     receipt_data = self.parse_receipt_data(extracted_text)
    #
    #     print("\nExtracted Receipt Data:")
    #     print(f"Vendor: {receipt_data['vendor']}")
    #     print(f"Date: {receipt_data['date']}")
    #     print(f"Currency: {receipt_data['currency']}")
    #
    #     print("\nItems:")
    #     for item in receipt_data['items']:
    #         print(f"{item[0]}: ${item[1]:.2f}")
    #
    #     print(f"\nTotal Amount: ${receipt_data['amount']:.2f}")
    #
    #     categorized_items = self.categorize_items(receipt_data['items'])
    #     print("\nCategorized Items:")
    #     for category, items in categorized_items.items():
    #         print(f"{category}: {len(items)} item(s)")
    #
    #     main_category = self.get_main_category(categorized_items)
    #     print(f"\nMain Category: {main_category}")
    #
    #     return receipt_data


    def extract_items(self,receipt_text):
        # Extract items from the receipt
        item_pattern = r'([A-Za-z\s]+)\s+(\d+)\s+\$(\d+(\.\d{2})?)\s+\$(\d+(\.\d{2})?)'
        items = re.findall(item_pattern, receipt_text)
        return [(item[0].strip(), int(item[1]), float(item[2]), float(item[4])) for item in items]

