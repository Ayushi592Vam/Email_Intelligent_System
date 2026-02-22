from pathlib import Path
import re
import json

BASE_DIR = Path(__file__).resolve().parent
OCR_DIR = BASE_DIR / "data" / "ocr"
OUT_DIR = BASE_DIR / "data" / "entities"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------
# HELPERS
# -------------------------------------------------

def extract(patterns, text):
    for p in patterns:
        m = re.search(p, text, re.I | re.S)
        if m:
            return m.group(1).strip()
    return None

def clean_amount(val):
    return re.sub(r"[^\d]", "", val) if val else None

# -------------------------------------------------
# ENTITY EXTRACTION
# -------------------------------------------------

def extract_entities(folder: Path):

    texts = {}
    for f in folder.glob("*.txt"):
        texts[f.name.lower()] = f.read_text(errors="ignore")

    full_text = "\n".join(texts.values())

    # ---------------- CLAIM TYPE ----------------
    if folder.name.startswith("CLM-AU"):
        claim_type = "AUTO"
    elif folder.name.startswith("CLM-HO"):
        claim_type = "HOME"
    else:
        claim_type = "UNKNOWN"

    # ---------------- BASIC FIELDS ----------------
    claim_number = extract([r"(CLM-[A-Z]{2}\d{4})"], full_text)

    policy_number = extract([
        r"Policy Number[:\s]*((AU|HO)\d{7})"
    ], full_text)

    carrier = extract([
        r"INSURER A[:\s]*([^\n]+)",
        r"INSURANCE COMPANY\s+Company[:\s]*([^\n]+)",
        r"Prepared for[:\s]*([^\n]+)",
        r"Dear\s+([A-Za-z]+)\s+Claims"
    ], full_text)

    date_of_loss = extract([
        r"Date of Loss[:\s]*([\d/]{8,10})",
        r"occurred on\s*([\d/]{8,10})"
    ], full_text)

    estimated_amount = clean_amount(extract([
        r"Total Estimated Repairs[:\s]*\$([\d,]+)",
        r"Estimated Damage[:\s]*\$([\d,]+)",
        r"Estimated Amount[:\s]*\$([\d,]+)"
    ], full_text))

    # ---------------- INSURED NAME ----------------
    if claim_type == "AUTO":
        insured = extract([
            r"Customer[:\s]*([A-Z][a-z]+\s+[A-Z][a-z]+)",
            r"Brokerage Services\s+([A-Z][a-z]+\s+[A-Z][a-z]+)",
            r"(?:Regards|Sincerely|Thank you),?\s*\n\s*([A-Z][a-z]+\s+[A-Z][a-z]+)",
            r"\n([A-Z][a-z]+\s+[A-Z][a-z]+)\nPhone:",
            r"\n([A-Z][a-z]+\s+[A-Z][a-z]+)\nEmail:"
        ], full_text)
    else:
        insured = extract([
            r"Name[:\s]*([A-Z][a-z]+\s+[A-Z][a-z]+)",
            r"Sincerely,\s*([A-Z][a-z]+\s+[A-Z][a-z]+)"
        ], full_text)

    # ---------------- AUTO ----------------
    vehicle = vin = loss_type = None
    property_address = None

    if claim_type == "AUTO":
        vehicle = extract([
            r"Vehicle[:\s]*((19|20)\d{2}\s+[A-Za-z]+\s+[A-Za-z0-9]+)"
        ], full_text)

        vin = extract([
            r"VIN[:\s]*([A-HJ-NPR-Z0-9]{17})"
        ], full_text)

        loss_type = "vehicle damage"

    # ---------------- HOME ----------------
    if claim_type == "HOME":
        property_address = extract([
            r"Property Address[:\s]*([\s\S]*?\d{5})",
            r"Address[:\s]*([\s\S]*?\d{5})",
            r"located at\s*([\s\S]*?\d{5})"
        ], full_text)

        loss_type = extract([
            r"Cause of Loss[:\s]*([A-Za-z ]+)(?:\n|$)",
            r"Loss Type[:\s]*([A-Za-z ]+)(?:\n|$)"
        ], full_text)

    # ---------------- FLAGS (FILE-BASED) ----------------
    has_medical = any("medical" in k for k in texts)
    has_police = any("police" in k for k in texts)
    has_legal = any("legal" in k for k in texts)

    return {
        "claim_type": claim_type,
        "claim_number": claim_number,
        "policy_number": policy_number,
        "insured_name": insured,
        "carrier": carrier,
        "date_of_loss": date_of_loss,
        "estimated_amount": estimated_amount,
        "injuries_reported": has_medical,
        "police_report": has_police,
        "legal_involvement": has_legal,
        "vehicle": vehicle,
        "vin": vin,
        "property_address": property_address.replace("\n", ", ").strip() if property_address else None,
        "loss_type": loss_type.lower().strip() if loss_type else None
    }

# -------------------------------------------------
# BATCH RUN
# -------------------------------------------------

def main():
    for folder in OCR_DIR.iterdir():
        if not folder.is_dir():
            continue

        entities = extract_entities(folder)

        out = OUT_DIR / folder.name
        out.mkdir(exist_ok=True)

        with open(out / "ENTITIES.json", "w") as f:
            json.dump(entities, f, indent=2)

    print("✅ ENTITY EXTRACTION COMPLETE (AUTO + HOME)")

if __name__ == "__main__":
    main()