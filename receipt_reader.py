import re
from collections import Counter

import cv2
from pytesseract import pytesseract


class ReceiptReader:
    def __init__(self, image_path):
        self.image_path = image_path

    def preprocess_image(self):
        """Preprocess the image for better OCR accuracy."""
        # Read the image
        image = cv2.imread(self.image_path)

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply thresholding to binarize the image
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

        return thresh

    def extract_text_from_image(self, image):
        """Extract text from the preprocessed image using Tesseract OCR."""
        custom_config = r'--oem 3 --psm 6'  # Adjust PSM based on your receipt layout
        extracted_text = pytesseract.image_to_string(image, config=custom_config)
        return extracted_text

    @staticmethod
    def clean_price(price_str):
        """Clean the price string and convert it to a float."""
        # Remove any unwanted characters (e.g., multiple dots)
        cleaned_str = re.sub(r'[^\d.]', '', price_str)  # Keep only digits and dots
        if cleaned_str.count('.') > 1:  # If there are multiple dots, remove extra dots
            cleaned_str = cleaned_str.replace('.', '', cleaned_str.count('.') - 1)

        try:
            return float(cleaned_str)
        except ValueError:
            return 0.0  # Fallback to 0.0 if conversion fails

    def parse_receipt_data(self, extracted_text):
        """Parse the extracted text to identify vendor, date, items, and their prices."""
        lines = extracted_text.split('\n')
        items = []
        vendor = None
        currency = None
        date = None

        # Define regex patterns
        date_pattern = re.compile(r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2})\b')  # Matches dates
        currency_pattern = re.compile(r'(\$|€|¥|£)(\d+(?:\.\d{1,2})?)')  # Matches currency

        exclude_keywords = [
            'subtotal', 'total', 'cash', 'change', 'thank you', 'items', 'store', 'open',
            'dallas', 'tx', 'thank', 'you', 'for', 'shopping'
        ]

        for line in lines:
            line = line.strip()  # Remove leading/trailing whitespace
            if line:
                # Set vendor as the first non-empty line
                if vendor is None:
                    vendor = line

                # Extract date
                if date is None:
                    date_match = date_pattern.search(line)
                    if date_match:
                        date = date_match.group(0)

                # Extract currency and amount
                currency_match = currency_pattern.search(line)
                if currency_match:
                    currency = currency_match.group(1)  # e.g., $

                # Check if the line matches item patterns
                # Use regex to capture items and prices
                item_price_pattern = re.compile(r'([\w\s]+)\s+(\$|€|¥|£)?\s*([\d,.]+)')  # Matches item names and prices
                item_match = item_price_pattern.search(line)

                if item_match:
                    item_name = item_match.group(1).strip()
                    price = self.clean_price(item_match.group(3))  # Clean and convert the price
                    items.append((item_name, price))  # Store items as tuples of (item_name, price)

        amount = self.extract_total(extracted_text)

        return {
            "vendor": vendor,
            "date": date,
            "currency": currency,
            "items": items,
            "amount":amount,
            "description":'receipt data'
        }

    def extract_total(self, extracted_text):
        """Extract the total amount from the extracted text."""
        total_pattern = re.compile(
            r'Total\s*:?(\s*\$?\s*([0-9]+(?:[.,][0-9]{1,2})?))|(?:TOTAL\s*:?(\s*\$?\s*([0-9]+(?:[.,][0-9]{1,2})?)))',
            re.IGNORECASE)

        total_match = total_pattern.search(extracted_text)

        if total_match:
            total = total_match.group(1) or total_match.group(3)  # Choose the correct group based on match
            if total:
                total = total.replace("$", "").replace(" ", "").strip()  # Clean the total string
                total = self.clean_price(total)  # Clean the total string
            else:
                total = 0.0  # Fallback to 0.0 if no match is found
        else:
            total = 0.0  # Fallback to 0.0 if no match is found

        return total

    def categorize_item(self, item_name):
        """Categorize items into major categories."""
        # Define major categories and keywords
        categories = {
            'Food': ['bread', 'apple', 'banana', 'chicken', 'beef', 'vegetable', 'fruit', 'pasta'],
            'Beverages': ['water', 'juice', 'soda', 'milk', 'coffee', 'tea', 'beer', 'wine'],
            'Household': ['detergent', 'soap', 'cleaner', 'paper towels', 'trash bags'],
            'Electronics': ['phone', 'charger', 'battery', 'cable', 'headphones', 'speaker'],
            'Clothing': ['shirt', 'pants', 'dress', 'shoes', 'socks', 'jacket'],
            'Health & Beauty': ['shampoo', 'soap', 'cream', 'toothpaste', 'vitamins'],
            'Office Supplies': ['paper', 'pen', 'pencil', 'notebook', 'stapler'],
            'Groceries': ['rice', 'beans', 'pasta', 'cereal', 'snack'],
            'Others': []  # Placeholder for uncategorized items
        }

        # Check the item name against categories
        for category, keywords in categories.items():
            if any(keyword in item_name.lower() for keyword in keywords):
                return category
        return 'Others'  # Return 'Others' if no category matched

    def categorize_items(self, items):
        """Categorize all items into major categories."""
        categorized_items = {}
        for item_name, price in items:
            category = self.categorize_item(item_name)
            if category in categorized_items:
                categorized_items[category].append((item_name, price))
            else:
                categorized_items[category] = [(item_name, price)]
        return categorized_items

    def get_main_category(self, categorized_items):
        """Get the main category based on the number of items."""
        category_counts = Counter({category: len(items) for category, items in categorized_items.items()})
        main_category = category_counts.most_common(1)[0][0] if category_counts else 'Others'
        return main_category

    def read_receipt(self):
        """Read the receipt and extract relevant information."""
        # Preprocess the image
        preprocessed_image = self.preprocess_image()

        # Extract text from the image
        extracted_text = self.extract_text_from_image(preprocessed_image)
        print("\nRaw Extracted Text:\n", extracted_text)

        # Parse the extracted text to get vendor, date, currency, and items
        receipt_data = self.parse_receipt_data(extracted_text)

        # Display the extracted data
        print("\nExtracted Receipt Data:")
        print(f"Vendor: {receipt_data['vendor']}")
        print(f"Date: {receipt_data['date']}")
        print(f"Currency: {receipt_data['currency']}")

        print("\nExtracted Items with Prices:\n")
        for item_name, price in receipt_data['items']:
            print(f"{item_name}: {price}")

        # Categorize items
        categorized_items = self.categorize_items(receipt_data['items'])
        print("\nCategorized Items:\n")
        for category, items in categorized_items.items():
            print(f"{category}: {items}")

        # Get main category
        main_category = self.get_main_category(categorized_items)
        print("\nMain Category:\n", main_category)

        # Extract total
        total = self.extract_total(extracted_text)
        print("\nExtracted Total:\n", total)
