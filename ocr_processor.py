# EMAIL_INTELLIGENT_SYSTEM/ocr_processor.py

import os
from pathlib import Path
import pytesseract
from PIL import Image
import pdfplumber

# 🔴 IMPORTANT: tesseract.exe path (tumhara path)
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\AyushiPrashantNagpur\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "data" / "raw" / "ClaimsEnterpriseEML"
OCR_DIR = BASE_DIR / "data" / "ocr"

OCR_DIR.mkdir(parents=True, exist_ok=True)

SUPPORTED_IMAGES = {".png", ".jpg", ".jpeg"}
SUPPORTED_PDFS = {".pdf"}


# ------------------------------------------------------------------
# OCR helpers
# ------------------------------------------------------------------

def ocr_image(path: Path) -> str:
    img = Image.open(path)
    return pytesseract.image_to_string(img)


def ocr_pdf(path: Path) -> str:
    text = ""
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                text += f"\n--- PAGE {i} ---\n{page_text}\n"
    return text.strip()


# ------------------------------------------------------------------
# Process one claim folder
# ------------------------------------------------------------------

def process_claim_folder(claim_folder: Path):
    claim_id = claim_folder.name
    out_dir = OCR_DIR / claim_id
    out_dir.mkdir(parents=True, exist_ok=True)

    combined_text = []

    for file in claim_folder.iterdir():
        if file.suffix.lower() in SUPPORTED_IMAGES:
            print(f"[OCR-IMG] {claim_id} -> {file.name}")
            text = ocr_image(file)

        elif file.suffix.lower() in SUPPORTED_PDFS:
            print(f"[OCR-PDF] {claim_id} -> {file.name}")
            text = ocr_pdf(file)

        else:
            continue

        txt_path = out_dir / f"{file.stem}.txt"
        txt_path.write_text(text, encoding="utf-8")

        combined_text.append(
            f"\n===== FILE: {file.name} =====\n{text}\n"
        )

    # Write combined OCR
    combined_path = out_dir / "combined.txt"
    combined_path.write_text("\n".join(combined_text), encoding="utf-8")

    print(f"[DONE] OCR completed for {claim_id}")


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

def main():
    if not RAW_DIR.exists():
        raise FileNotFoundError(f"RAW DIR not found: {RAW_DIR}")

    claim_folders = sorted([f for f in RAW_DIR.iterdir() if f.is_dir()])

    print(f"Found {len(claim_folders)} claim folders")

    for folder in claim_folders:
        process_claim_folder(folder)

    print("\n✅ ALL OCR DONE")


if __name__ == "__main__":
    main()
