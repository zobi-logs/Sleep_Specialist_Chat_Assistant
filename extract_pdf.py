import fitz
import os

def extract_text(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

pdf_folder = "./pdf/"
combined_text = ""

for file in os.listdir(pdf_folder):
    if file.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, file)
        print(f"Extracting text from: {pdf_path}")
        combined_text += extract_text(pdf_path) + "\n\n"

with open("combined_books.txt", "w", encoding="utf-8") as f:
    f.write(combined_text)

print("✅ Text extraction completed! Saved as combined_books.txt.")
