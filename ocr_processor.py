# EMAIL_INTELLIGENT_SYSTEM/file_tagger.py

from pathlib import Path
import json
import re

BASE_DIR = Path(__file__).resolve().parent
OCR_DIR = BASE_DIR / "data" / "ocr"
OUT_DIR = BASE_DIR / "data" / "file_tags"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------
# FILE TAGGING TAXONOMY (STRICT, BUSINESS-SAFE)
# -------------------------------------------------

FILE_TAXONOMY = {
    "MEDICAL": [
        r"medical report",
        r"hospital",
        r"treatment",
        r"physician",
        r"diagnosis",
        r"injury",
        r"clinic"
    ],
    "POLICE": [
        r"police report",
        r"incident report",
        r"accident report",
        r"fir\s*no",
        r"case\s*number",
        r"report\s*number",
        r"police department"
    ],
    "LEGAL": [
        r"legal notice",
        r"attorney",
        r"lawyer",
        r"court",
        r"lawsuit",
        r"litigation",
        r"summons"
    ],
    "REPAIR_ESTIMATE": [
        r"repair estimate",
        r"estimated repairs",
        r"damage estimate",
        r"labor cost",
        r"parts cost"
    ],
    "ACORD": [
        r"acord\s*25",
        r"acord\s*140",
        r"certificate of insurance"
    ],
    "PROPERTY": [
        r"property",
        r"residence",
        r"home",
        r"condo",
        r"dwelling",
        r"structure"
    ]
}

# -------------------------------------------------
# FILE TAGGING LOGIC
# -------------------------------------------------

def tag_file(text: str, filename: str):
    tags = set()

    lower_text = text.lower()
    lower_name = filename.lower()

    # -------------------------------------------------
    # 1️⃣ PHOTO FILES — filename based ONLY
    # -------------------------------------------------
    if any(x in lower_name for x in ["damage", "photo", "img", "image"]):
        tags.add("PHOTOS")
        return list(tags)

    # -------------------------------------------------
    # 2️⃣ POLICE FILE — filename hard rule
    # -------------------------------------------------
    if "police" in lower_name:
        tags.add("POLICE")
        return list(tags)

    # -------------------------------------------------
    # 3️⃣ TEXT-BASED STRICT TAGGING
    # -------------------------------------------------
    for tag, patterns in FILE_TAXONOMY.items():
        for pattern in patterns:
            if re.search(pattern, lower_text):
                tags.add(tag)
                break

    # -------------------------------------------------
    # 4️⃣ FALLBACK
    # -------------------------------------------------
    if not tags:
        tags.add("OTHER")

    return list(tags)

# -------------------------------------------------
# BATCH RUN
# -------------------------------------------------

def main():
    for claim_folder in OCR_DIR.iterdir():
        if not claim_folder.is_dir():
            continue

        claim_out = OUT_DIR / claim_folder.name
        claim_out.mkdir(exist_ok=True)

        results = {}

        for txt_file in claim_folder.glob("*.txt"):
            text = txt_file.read_text(errors="ignore")
            tags = tag_file(text, txt_file.name)
            results[txt_file.name] = tags

        with open(claim_out / "FILE_TAGS.json", "w") as f:
            json.dump(results, f, indent=2)

    print("✅ FILE TAGGING COMPLETE (STRICT MODE)")

if __name__ == "__main__":
    main()