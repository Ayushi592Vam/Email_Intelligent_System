# EMAIL_INTELLIGENT_SYSTEM/summary_generator.py

from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent
OCR_DIR = BASE_DIR / "data" / "ocr"
SUMMARY_DIR = BASE_DIR / "data" / "summaries"
SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------
# Helpers
# -------------------------------------------------

def extract(patterns, text):
    for p in patterns:
        m = re.search(p, text, re.I | re.M)
        if m and m.groups():
            return m.group(1).strip()
    return None

def format_amount(raw):
    if not raw:
        return "Unknown"
    raw = re.sub(r"[,$]", "", raw)
    try:
        return f"${int(float(raw)):,}"
    except:
        return raw

# -------------------------------------------------
# INSURED (FIXED)
# -------------------------------------------------

def extract_insured(text):
    # Repair estimate is most reliable
    m = re.search(r"Customer[:\s]*([A-Z][a-z]+\s+[A-Z][a-z]+)", text)
    if m:
        return m.group(1)

    # ACORD insured line
    m = re.search(
        r"Fire Insurance Brokerage Services\s+([A-Z][a-z]+\s+[A-Z][a-z]+)",
        text
    )
    if m:
        return m.group(1)

    return "Unknown"

# -------------------------------------------------
# VEHICLE (FIXED)
# -------------------------------------------------

def extract_vehicle(text):
    m = re.search(
        r"Vehicle[:\s]*((19|20)\d{2}\s+[A-Za-z]+\s+[A-Za-z0-9]+)",
        text
    )
    vehicle = m.group(1) if m else None

    vin = extract([r"VIN[:\s]*([A-HJ-NPR-Z0-9]{17})"], text)

    if vehicle and vin:
        return f"{vehicle} | VIN: {vin}"
    if vehicle:
        return vehicle
    if vin:
        return f"VIN: {vin}"

    return "N/A"

# -------------------------------------------------
# SMART RISK DETECTION (🔥 MAIN FIX)
# -------------------------------------------------

def detect_injury(text):
    text = text.lower()

    positive = [
        "medical report",
        "patient information",
        "diagnosis",
        "treating physician",
        "emergency room",
        "hospital admission",
        "physical therapy",
        "medical record",
        "ssn:",
        "dob:"
    ]

    negative = [
        "medical payments",
        "medical coverage",
        "policy",
        "coverage"
    ]

    if any(p in text for p in positive):
        return "Yes"

    if any(n in text for n in negative):
        return "No"

    return "No"

def detect_police(text):
    text = text.lower()
    police_signals = [
        "police accident report",
        "police department",
        "reporting officer",
        "badge:",
        "incident information",
        "narrative",
        "citations issued"
    ]
    return "Yes" if any(p in text for p in police_signals) else "No"

def detect_legal(text):
    text = text.lower()
    legal_signals = [
        "law firm",
        "attorneys at law",
        "demand for settlement",
        "esq",
        "legal demand",
        "attorney for"
    ]
    return "Yes" if any(l in text for l in legal_signals) else "No"

# -------------------------------------------------
# MAIN SUMMARY
# -------------------------------------------------

def generate_summary(text):

    claim_number = extract([r"(CLM-[A-Z]{2}\d{4})"], text) or "Unknown"
    policy_number = extract([r"Policy Number[:\s]*((AU|HO)\d{7})"], text) or "Unknown"
    carrier = extract([r"INSURER A[:\s]*([^\n]+)"], text) or "Unknown"
    loss_date = extract([r"Date of Loss[:\s]*([\d/]{8,10})"], text) or "Unknown"

    amount_raw = extract([
        r"Total Estimated Repairs[:\s]*\$?([\d,]+)",
        r"Estimated Amount[:\s]*\$?([\d,]+)"
    ], text)
    amount = format_amount(amount_raw)

    insured = extract_insured(text)
    vehicle = extract_vehicle(text)

    has_injury = detect_injury(text)
    has_police = detect_police(text)
    has_legal = detect_legal(text)

    severity_score = 20
    if has_injury == "Yes": severity_score += 30
    if has_police == "Yes": severity_score += 20
    if has_legal == "Yes": severity_score += 40

    severity = (
        "CRITICAL" if severity_score >= 80 else
        "HIGH" if severity_score >= 60 else
        "MEDIUM" if severity_score >= 40 else
        "LOW"
    )

    return f"""
CLAIM SUMMARY
--------------------------------------------------
Claim Type: AUTO
Claim Number: {claim_number}
Policy Number: {policy_number}
Insured: {insured}
Carrier: {carrier}
Date of Loss: {loss_date}
Estimated Amount: {amount}

Injuries Reported: {has_injury}
Police Report: {has_police}
Legal Involvement: {has_legal}

Vehicle: {vehicle}

Severity: {severity} ({severity_score})

Summary Narrative:
Loss reported under active policy. OCR documents reviewed including ACORD forms,
repair estimates, and supporting evidence. Claim requires adjuster review.
"""

# -------------------------------------------------
# BATCH RUNNER
# -------------------------------------------------

def main():
    folders = [f for f in OCR_DIR.iterdir() if f.is_dir()]
    print(f"🚀 Processing {len(folders)} claims")

    for folder in folders:
        texts = folder.glob("*.txt")
        full_text = "\n".join(t.read_text(errors="ignore") for t in texts)

        summary = generate_summary(full_text)

        out = SUMMARY_DIR / folder.name
        out.mkdir(exist_ok=True)
        (out / "CLAIM_SUMMARY.txt").write_text(summary)

    print("✅ All summaries generated")

if __name__ == "__main__":
    main()