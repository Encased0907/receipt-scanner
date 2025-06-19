from PIL import Image
import pytesseract
import os
import csv

# Ensure you have Tesseract installed and the path is set correctly
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to extract text from an image using Tesseract OCR
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

extracted_text = extract_text_from_image('D:\\VS Projects\\Barcode prototype\\Receipt2.png')
lines = extracted_text.split('\n')

# Extracting the store name from the receipt
known_stores = [
    "Walmart", "Target", "CVS", "Walgreens", "Kroger", "Costco",
    "Publix", "Aldi", "Whole Foods", "Safeway", "Rite Aid",
    "Best Buy", "Home Depot", "Lowe's", "Dollar Tree", "Sam's Club"
]

# Function to extract the store name from the OCR text by comparing lowercase versions
# of both the OCR text and the store names for case-insensitive matching
def extract_store_name(ocr_text, store_names):
    ocr_text_lower = ocr_text.lower()
    for store in store_names:
        if store.lower() in ocr_text_lower:
            return store
    return None

store_name = extract_store_name(extracted_text, known_stores)
print(f"Store Name: {store_name}")

# Extracting the date from the receipt
date_line = next((line for line in lines if '/25' in line or '/2025' in line), None)
receipt_date = date_line.strip() if date_line else ''
print(f"Receipt Date: {receipt_date}")

# Extracting the total amount from the receipt
total_line = next((line for line in lines if 'Total' in line or 'TOTAL' in line), None)
total_amount = total_line.strip() if total_line else ''
print(f"Total Amount: {total_amount}")

# Saving the extracted information to a CSV file
output_file = 'D:\\VS Projects\\Barcode prototype\\extracted_receipt_info.csv'
file_exists = os.path.isfile(output_file)

with open(output_file, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    if not file_exists:
        writer.writerow(['Store Name', 'Receipt Date', 'Total Amount'])
    writer.writerow([store_name, receipt_date, total_amount])

print(f"Extracted information saved to {output_file}")
