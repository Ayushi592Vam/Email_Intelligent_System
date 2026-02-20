# EMAIL_INTELLIGENT_SYSTEM/synthetic_data_generator.py

import os
import random
from datetime import datetime, timedelta
from pathlib import Path
from email.message import EmailMessage
from typing import Dict
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "data" / "raw" / "ClaimsEnterpriseEML"
os.makedirs(RAW_DIR, exist_ok=True)

AUTO = "AUTO"
HOME = "HOME"

FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael",
    "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan",
    "Joseph", "Jessica", "Thomas", "Sarah", "Christopher", "Karen",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Taylor", "Moore", "Jackson", "Martin",
]

CITIES_STATES = [
    ("Dallas", "TX"),
    ("Houston", "TX"),
    ("Phoenix", "AZ"),
    ("Los Angeles", "CA"),
    ("Chicago", "IL"),
    ("Miami", "FL"),
    ("Atlanta", "GA"),
    ("New York", "NY"),
]

INSURANCE_COMPANIES = [
    "State Farm", "Allstate", "Geico", "Progressive",
    "Nationwide", "Liberty Mutual", "Travelers", "Farmers"
]

VEHICLES = [
    ("Toyota", "Camry"),
    ("Honda", "Accord"),
    ("Ford", "F-150"),
    ("Chevrolet", "Silverado"),
    ("Tesla", "Model 3"),
    ("BMW", "3 Series"),
    ("Audi", "A4"),
]

HOME_CATEGORIES = ["Fire", "Water Damage", "Theft", "Liability", "Natural Disaster", "Vandalism"]
AUTO_CATEGORIES = ["Personal Liability", "Collision", "Comprehensive", "Medical Payments", "Uninsured Motorist"]

INJURY_TYPES = ["Whiplash", "Concussion", "Fractured Rib", "Back Strain", "Soft Tissue Injury", "Laceration"]
TREATMENTS = ["Emergency Room", "Urgent Care", "Orthopedic Specialist", "Physical Therapy", "Surgery"]


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def rand_name():
    fn = random.choice(FIRST_NAMES)
    ln = random.choice(LAST_NAMES)
    return fn, ln, f"{fn} {ln}"


def rand_address():
    num = random.randint(100, 9999)
    street = random.choice(["Main", "Oak", "Maple", "Cedar", "Pine", "Elm", "Washington", "Park"])
    st_type = random.choice(["St", "Ave", "Dr", "Ln", "Ct", "Blvd"])
    return f"{num} {street} {st_type}"


def rand_dates():
    end = datetime(2020, 1, 11)
    start = end - timedelta(days=180)
    loss = start + timedelta(days=random.randint(0, 180))
    report = loss + timedelta(days=random.randint(0, 5))
    return loss, report


def rand_phone():
    return f"{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"


def rand_vin():
    chars = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"
    return "".join(random.choice(chars) for _ in range(17))


def rand_ssn():
    return f"{random.randint(100,999)}-{random.randint(10,99)}-{random.randint(1000,9999)}"


def rand_dob():
    year = random.randint(1950, 1995)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{month:02d}/{day:02d}/{year}"


# ---------------------------------------------------------------------
# PDF Generation with Professional Formatting
# ---------------------------------------------------------------------

def create_acord25_pdf(path: Path, claim: Dict):
    """
    ACORD 25 - Certificate of Liability Insurance (Auto) - Corrected layout and alignments
    Fixed: drawCentredText -> drawCentredString
    """
    c = canvas.Canvas(str(path), pagesize=LETTER)
    width, height = LETTER

    L = 0.75 * inch
    W = 6.5 * inch

    # ================= HEADER =================
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1 * inch, height - 0.7 * inch, "ACORD 25 (2016/03)")
    c.drawString(1 * inch, height - 1.0 * inch, "CERTIFICATE OF LIABILITY INSURANCE")

    c.setFont("Helvetica-Oblique", 8)
    c.drawString(1 * inch, height - 1.25 * inch, f"DATE (MM/DD/YYYY): {claim.get('report_date', '02/19/2026')}")

    # ================= PRODUCER / INSURED =================
    producer_insured_top = height - 1.65 * inch
    box_h = 1.85 * inch
    c.rect(L, producer_insured_top - box_h, W, box_h)

    # Producer (left column)
    y = producer_insured_top - 0.25 * inch
    c.setFont("Helvetica-Bold", 9)
    c.drawString(L + 0.15 * inch, y, "PRODUCER")
    c.setFont("Helvetica", 8)
    c.drawString(L + 0.15 * inch, y - 0.15 * inch, "Fire Insurance Brokerage Services")
    c.drawString(L + 0.15 * inch, y - 0.28 * inch, "4025 Stockard Drive, Suite 876")
    c.drawString(L + 0.15 * inch, y - 0.41 * inch, "Frisco, TX 75034")
    c.drawString(L + 0.15 * inch, y - 0.54 * inch, f"Phone: {rand_phone()}")

    # Insured (right column)
    insured_x = L + 3.4 * inch
    c.setFont("Helvetica-Bold", 9)
    c.drawString(insured_x, y, "INSURED")
    c.setFont("Helvetica", 8)
    c.drawString(insured_x, y - 0.15 * inch, claim.get('insured_name', 'John Doe'))
    c.drawString(insured_x, y - 0.28 * inch, claim.get('address', '123 Main St'))
    c.drawString(insured_x, y - 0.41 * inch, f"{claim.get('city', 'Dallas')}, {claim.get('state', 'TX')} {claim.get('zip', '75001')}")
    c.drawString(insured_x, y - 0.54 * inch, f"Phone: {claim.get('phone', '(214) 555-0123')}")

    # ================= INSURER =================
    insurer_top = producer_insured_top - box_h - 0.25 * inch
    insurer_box_h = 1.3 * inch
    c.rect(L, insurer_top - insurer_box_h, W, insurer_box_h)

    y = insurer_top - 0.25 * inch
    c.setFont("Helvetica-Bold", 9)
    c.drawString(L + 0.15 * inch, y, "INSURER(S) AFFORDING COVERAGE")
    c.setFont("Helvetica", 8)
    c.drawString(L + 0.15 * inch, y - 0.20 * inch, f"INSURER A: {claim.get('carrier', 'ABC Insurance Co')}")
    c.drawString(L + 0.15 * inch, y - 0.35 * inch, f"Policy Number: {claim.get('policy_number', 'POL-123456')}")
    c.drawString(L + 0.15 * inch, y - 0.50 * inch, f"Effective Date: {claim.get('loss_date', '01/01/2026')}")
    c.drawString(L + 0.15 * inch, y - 0.65 * inch, "Expiration Date: 12/31/2026")

    # ================= COVERAGES =================
    coverages_top = insurer_top - insurer_box_h - 0.4 * inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(L, coverages_top, "COVERAGES")

    coverages_box_h = 1.8 * inch
    c.rect(L, coverages_top - coverages_box_h - 0.15 * inch, W, coverages_box_h)

    y = coverages_top - 0.45 * inch
    c.setFont("Helvetica", 8)
    c.drawString(L + 0.15 * inch, y, "TYPE OF INSURANCE")
    c.drawString(L + 3.0 * inch, y, "POLICY NUMBER")
    c.drawString(L + 4.6 * inch, y, "LIMITS")

    y -= 0.16 * inch
    c.line(L + 0.15 * inch, y, L + W - 0.15 * inch, y)

    y -= 0.22 * inch
    c.drawString(L + 0.15 * inch, y, "✓ AUTOMOBILE LIABILITY")
    c.drawString(L + 3.0 * inch, y, claim.get('policy_number', 'POL-123456'))
    c.drawString(L + 4.6 * inch, y, "$250,000 Each Accident")

    y -= 0.18 * inch
    c.drawString(L + 0.35 * inch, y, f"Category: {claim.get('category', 'Auto Physical Damage')}")
    c.drawString(L + 4.6 * inch, y, "$100,000 Each Person")

    y -= 0.18 * inch
    c.drawString(L + 0.35 * inch, y, "ANY AUTO")
    c.drawString(L + 4.6 * inch, y, "$50,000 Property Damage")

    # ================= DESCRIPTION =================
    desc_top = coverages_top - coverages_box_h - 0.35 * inch
    c.setFont("Helvetica-Bold", 9)
    c.drawString(L, desc_top, "DESCRIPTION OF OPERATIONS / LOCATIONS / VEHICLES / SPECIAL PROVISIONS")

    desc_box_h = 1.6 * inch
    c.rect(L, desc_top - desc_box_h - 0.15 * inch, W, desc_box_h)

    y = desc_top - 0.45 * inch
    c.setFont("Helvetica", 8)
    c.drawString(L + 0.15 * inch, y, f"Claim Number: {claim.get('claim_number', 'CLM-789012')}")
    c.drawString(L + 0.15 * inch, y - 0.20 * inch, f"Date of Loss: {claim.get('loss_date', '01/15/2026')}")
    c.drawString(L + 0.15 * inch, y - 0.40 * inch, f"Estimated Amount: ${claim.get('claim_amount', 12500):,}")
    c.drawString(L + 0.15 * inch, y - 0.60 * inch, f"Vehicle: {claim.get('vehicle_year', 2022)} {claim.get('vehicle_make', 'Toyota')} {claim.get('vehicle_model', 'Camry')}, VIN: {claim.get('vin', '4T1BF1FK0HU123456')}")

    # ================= FOOTER =================
    footer_y1 = 1.0 * inch
    footer_y2 = 0.65 * inch
    c.setFont("Helvetica-Oblique", 7)
    c.drawCentredString(width / 2, footer_y1, "ACORD 25 (2016/03) © 1988-2016 ACORD CORPORATION. All rights reserved.")
    c.drawCentredString(width / 2, footer_y2, "The ACORD name and logo are registered marks of ACORD")

    c.setFont("Helvetica-Oblique", 8)
    disclaimer_y = 0.35 * inch
    c.drawString(L + 0.15 * inch, disclaimer_y, "THIS CERTIFICATE IS ISSUED AS A MATTER OF INFORMATION ONLY AND CONFERS NO RIGHTS UPON THE")
    c.drawString(L + 0.15 * inch, disclaimer_y - 0.15 * inch, "CERTIFICATE HOLDER. THIS CERTIFICATE DOES NOT AFFIRMATIVELY OR NEGATIVELY AMEND, EXTEND OR")
    c.drawString(L + 0.15 * inch, disclaimer_y - 0.30 * inch, "ALTER THE COVERAGE AFFORDED BY THE POLICIES BELOW. THIS CERTIFICATE DOES NOT CONSTITUTE")
    c.drawString(L + 0.15 * inch, disclaimer_y - 0.45 * inch, "A CONTRACT BETWEEN THE ISSUING INSURER(S), AUTHORIZED REPRESENTATIVE OR PRODUCER, AND THE")

    c.save()





def create_acord140_pdf(path: Path, claim: Dict):
    """
    ACORD 140 - Property Section (Homeowners)
    """
    c = canvas.Canvas(str(path), pagesize=LETTER)
    width, height = LETTER

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, height - 0.75*inch, "ACORD 140 - PROPERTY LOSS NOTICE")

    c.setFont("Helvetica", 8)
    c.drawString(1*inch, height - 1*inch, f"DATE OF REPORT: {claim['report_date']}")

    # ------------------------------------------------------------------
    # INSURED INFORMATION
    # ------------------------------------------------------------------
    y = height - 1.6*inch
    c.rect(0.75*inch, y - 1.4*inch, 6.5*inch, 1.4*inch)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "INSURED INFORMATION")
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y - 0.25*inch, f"Name: {claim['insured_name']}")
    c.drawString(1*inch, y - 0.45*inch, f"Property Address: {claim['address']}")
    c.drawString(1*inch, y - 0.65*inch, f"{claim['city']}, {claim['state']} {claim['zip']}")
    c.drawString(1*inch, y - 0.85*inch, f"Phone: {claim['phone']}")
    c.drawString(1*inch, y - 1.05*inch, f"Email: {claim['email']}")

    # ------------------------------------------------------------------
    # INSURANCE COMPANY
    # ------------------------------------------------------------------
    y = height - 3.3*inch
    c.rect(0.75*inch, y - 1.2*inch, 6.5*inch, 1.2*inch)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "INSURANCE COMPANY")
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y - 0.25*inch, f"Company: {claim['carrier']}")
    c.drawString(1*inch, y - 0.45*inch, f"Policy Number: {claim['policy_number']}")
    c.drawString(1*inch, y - 0.65*inch, "Policy Period: 01/01/2019 - 12/31/2020")
    c.drawString(1*inch, y - 0.85*inch,
                 f"Agent: {random.choice(['Tom Anderson', 'Sarah Mitchell', 'John Roberts'])}")

    # ------------------------------------------------------------------
    # PROPERTY INFORMATION
    # ------------------------------------------------------------------
    y = height - 5.0*inch
    c.rect(0.75*inch, y - 1.2*inch, 6.5*inch, 1.2*inch)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "PROPERTY INFORMATION")
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y - 0.25*inch, f"Property Type: {claim['property_type']}")
    c.drawString(1*inch, y - 0.45*inch, f"Year Built: {claim['year_built']}")
    c.drawString(1*inch, y - 0.65*inch,
                 f"Square Footage: {random.randint(1200, 3500)} sq ft")
    c.drawString(1*inch, y - 0.85*inch,
                 f"Construction: {random.choice(['Frame', 'Brick', 'Stucco'])}")

    # ------------------------------------------------------------------
    # LOSS INFORMATION
    # ------------------------------------------------------------------
    y = height - 6.8*inch
    c.rect(0.75*inch, y - 1.6*inch, 6.5*inch, 1.6*inch)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "LOSS INFORMATION")
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y - 0.25*inch, f"Claim Number: {claim['claim_number']}")
    c.drawString(1*inch, y - 0.45*inch, f"Date of Loss: {claim['loss_date']}")
    c.drawString(
        1*inch,
        y - 0.65*inch,
        f"Time of Loss: {random.randint(1,12)}:{random.choice(['00','15','30','45'])} "
        f"{random.choice(['AM','PM'])}"
    )
    c.drawString(1*inch, y - 0.85*inch, f"Cause of Loss: {claim['category']}")
    c.drawString(1*inch, y - 1.05*inch,
                 f"Estimated Damage: ${claim['claim_amount']:,}")
    c.drawString(1*inch, y - 1.25*inch, "Status: Under Investigation")

    # ------------------------------------------------------------------
    # DESCRIPTION OF DAMAGE
    # ------------------------------------------------------------------
    y = height - 8.8*inch
    c.rect(0.75*inch, y - 1.1*inch, 6.5*inch, 1.1*inch)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "DESCRIPTION OF DAMAGE")
    c.setFont("Helvetica", 9)

    desc = f"Property sustained damage due to {claim['category'].lower()}. Initial inspection reveals "
    desc += random.choice([
        "structural damage requiring immediate repair.",
        "moderate damage to interior and exterior components.",
        "significant water intrusion affecting multiple rooms.",
        "extensive fire damage to roof and attic area.",
    ])

    c.drawString(1*inch, y - 0.3*inch, desc[:95])
    if len(desc) > 95:
        c.drawString(1*inch, y - 0.5*inch, desc[95:])

    # Footer
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(1*inch, 0.75*inch,
                 "ACORD 140 (2008/01) © ACORD CORPORATION 2008")

    c.save()


def create_medical_report_pdf(path: Path, claim: Dict):
    """
    Detailed Medical Report PDF
    """
    c = canvas.Canvas(str(path), pagesize=LETTER)
    width, height = LETTER

    # Header
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, height - 0.75*inch, "MEDICAL REPORT")

    c.setFont("Helvetica", 9)
    c.drawString(1*inch, height - 1*inch, f"Report Date: {claim['report_date']}")
    c.drawString(5*inch, height - 1*inch, f"Claim: {claim['claim_number']}")

    # ------------------------------------------------------------------
    # PATIENT INFORMATION
    # ------------------------------------------------------------------
    y = height - 1.6*inch
    c.rect(0.75*inch, y - 1.3*inch, 6.5*inch, 1.3*inch)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "PATIENT INFORMATION")
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y - 0.25*inch, f"Name: {claim['insured_name']}")
    c.drawString(4*inch, y - 0.25*inch, f"DOB: {rand_dob()}")
    c.drawString(1*inch, y - 0.4*inch, f"SSN: {rand_ssn()}")
    c.drawString(4*inch, y - 0.4*inch, f"Phone: {claim['phone']}")
    c.drawString(1*inch, y - 0.6*inch,
                 f"Address: {claim['address']}, {claim['city']}, {claim['state']} {claim['zip']}")

    # ------------------------------------------------------------------
    # MEDICAL FACILITY
    # ------------------------------------------------------------------
    y = height - 3.1*inch
    c.rect(0.75*inch, y - 1.0*inch, 6.5*inch, 1.0*inch)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "MEDICAL FACILITY")
    c.setFont("Helvetica", 9)
    facility = random.choice([
        "Memorial Hospital",
        "County General Medical Center",
        "Regional Emergency Care",
        "City Medical Center"
    ])
    c.drawString(1*inch, y - 0.25*inch, f"Facility: {facility}")
    c.drawString(1*inch, y - 0.45*inch, f"Date of Service: {claim['loss_date']}")
    c.drawString(4*inch, y - 0.45*inch,
                 f"Treating Physician: Dr. {random.choice(LAST_NAMES)}")

    # ------------------------------------------------------------------
    # CHIEF COMPLAINT
    # ------------------------------------------------------------------
    y = height - 4.6*inch
    c.rect(0.75*inch, y - 0.75*inch, 6.5*inch, 0.75*inch)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "CHIEF COMPLAINT")
    c.setFont("Helvetica", 9)
    injury = random.choice(INJURY_TYPES)
    c.drawString(
        1*inch,
        y - 0.3*inch,
        f"Patient presents with {injury.lower()} following motor vehicle accident on {claim['loss_date']}."
    )

    # ------------------------------------------------------------------
    # DIAGNOSIS
    # ------------------------------------------------------------------
    y = height - 5.7*inch
    c.rect(0.75*inch, y - 1.2*inch, 6.5*inch, 1.2*inch)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "DIAGNOSIS")
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y - 0.25*inch, f"Primary: {injury}")
    c.drawString(1*inch, y - 0.45*inch,
                 f"Secondary: {random.choice(['Contusions','Abrasions','Muscle Strain','Soft Tissue Damage'])}")
    c.drawString(1*inch, y - 0.65*inch, "ICD-10 Codes: S13.4XXA, M62.830")

    # ------------------------------------------------------------------
    # TREATMENT PLAN
    # ------------------------------------------------------------------
    y = height - 7.1*inch
    c.rect(0.75*inch, y - 1.5*inch, 6.5*inch, 1.5*inch)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "TREATMENT PLAN")
    c.setFont("Helvetica", 9)
    treatment = random.choice(TREATMENTS)
    c.drawString(1*inch, y - 0.25*inch, f"Immediate: {treatment}")
    c.drawString(1*inch, y - 0.45*inch,
                 "Medications: Ibuprofen 800mg, Cyclobenzaprine 10mg")
    c.drawString(1*inch, y - 0.65*inch,
                 "Follow-up: 2 weeks, Physical therapy 3x weekly for 6 weeks")
    c.drawString(1*inch, y - 0.85*inch,
                 "Restrictions: No heavy lifting, limited driving for 2 weeks")
    c.drawString(1*inch, y - 1.05*inch,
                 f"Estimated Recovery: {random.randint(4,12)} weeks")

    # ------------------------------------------------------------------
    # PROGNOSIS
    # ------------------------------------------------------------------
    y = height - 8.9*inch
    c.rect(0.75*inch, y - 0.6*inch, 6.5*inch, 0.6*inch)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "PROGNOSIS")
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y - 0.3*inch, random.choice([
        "Good with proper treatment and physical therapy compliance.",
        "Fair - may require extended treatment period.",
        "Excellent if patient follows prescribed treatment plan."
    ]))

    # ------------------------------------------------------------------
    # SIGNATURE
    # ------------------------------------------------------------------
    y = height - 9.8*inch
    c.rect(0.75*inch, y - 0.8*inch, 6.5*inch, 0.8*inch)

    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y - 0.2*inch,
                 f"Physician: Dr. {random.choice(LAST_NAMES)}, MD")
    c.drawString(1*inch, y - 0.4*inch,
                 f"License: {random.randint(100000,999999)}")
    c.drawString(1*inch, y - 0.6*inch,
                 f"Date: {claim['report_date']}")

    c.save()



def create_police_report_pdf(path: Path, claim: Dict):
    """
    Detailed Police Report PDF
    """
    c = canvas.Canvas(str(path), pagesize=LETTER)
    width, height = LETTER

    # Header
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, height - 0.75*inch, "POLICE ACCIDENT REPORT")

    c.setFont("Helvetica", 9)
    dept = f"{claim['city']} Police Department"
    c.drawString(1*inch, height - 1*inch, dept)
    c.drawString(5*inch, height - 1*inch, f"Report #: {random.randint(2019001000, 2019999999)}")

    # ------------------------------------------------------------------
    # INCIDENT DETAILS
    # ------------------------------------------------------------------
    y = height - 1.6*inch
    c.rect(0.75*inch, y - 1.1*inch, 6.5*inch, 1.1*inch)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "INCIDENT INFORMATION")
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y - 0.25*inch,
                 f"Date/Time: {claim['loss_date']} at {random.randint(7,21):02d}:{random.randint(0,59):02d}")
    c.drawString(1*inch, y - 0.4*inch,
                 f"Location: {rand_address()}, {claim['city']}, {claim['state']}")
    c.drawString(1*inch, y - 0.55*inch, f"Type: {claim['category']}")
    c.drawString(1*inch, y - 0.7*inch,
                 f"Weather: {random.choice(['Clear','Rainy','Cloudy','Foggy'])}, Road: {random.choice(['Dry','Wet','Icy'])}")

    # ------------------------------------------------------------------
    # PARTIES INVOLVED
    # ------------------------------------------------------------------
    y = height - 3.0*inch
    c.rect(0.75*inch, y - 1.4*inch, 6.5*inch, 1.4*inch)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "PARTIES INVOLVED")
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y - 0.25*inch, f"Driver 1: {claim['insured_name']}")
    c.drawString(1*inch, y - 0.4*inch,
                 f"  License: {claim['state']}{random.randint(10000000,99999999)}")
    c.drawString(1*inch, y - 0.55*inch,
                 f"  Vehicle: {claim['vehicle_year']} {claim['vehicle_make']} {claim['vehicle_model']}, VIN: {claim['vin']}")

    other_fn, other_ln, other_full = rand_name()
    c.drawString(1*inch, y - 0.8*inch, f"Driver 2: {other_full}")
    other_make, other_model = random.choice(VEHICLES)
    c.drawString(1*inch, y - 0.95*inch,
                 f"  Vehicle: {random.randint(2010,2019)} {other_make} {other_model}")

    # ------------------------------------------------------------------
    # NARRATIVE
    # ------------------------------------------------------------------
    y = height - 4.8*inch
    c.rect(0.75*inch, y - 2.1*inch, 6.5*inch, 2.1*inch)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "NARRATIVE")
    c.setFont("Helvetica", 9)
    y -= 0.25*inch

    narratives = [
        f"On {claim['loss_date']}, at approximately {random.randint(7,21):02d}:{random.randint(0,59):02d}, officers responded to",
        f"a {claim['category'].lower()} at the intersection of {rand_address()}. Upon arrival, officers observed",
        f"when Driver 2 ({other_full}) failed to yield right of way. Impact occurred to the",
        f"{random.choice(['front','rear','driver side','passenger side'])} of Driver 1's vehicle. Both drivers were",
        f"{'transported to hospital for evaluation' if claim['has_injury'] else 'uninjured'}. Damage to both vehicles estimated at moderate to severe.",
        f"Citations issued to Driver 2 for {random.choice(['failure to yield','running red light','unsafe lane change'])}.",
        "No witnesses were present at scene. Photos and measurements taken."
    ]

    for line in narratives:
        c.drawString(1*inch, y, line[:95])
        y -= 0.16*inch

    # ------------------------------------------------------------------
    # OFFICER INFORMATION
    # ------------------------------------------------------------------
    y = height - 7.2*inch
    c.rect(0.75*inch, y - 0.9*inch, 6.5*inch, 0.9*inch)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "REPORTING OFFICER")
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, y - 0.25*inch,
                 f"Officer: {random.choice(['J. Martinez','R. Thompson','S. Williams','K. Johnson'])}")
    c.drawString(1*inch, y - 0.4*inch, f"Badge: {random.randint(1000,9999)}")
    c.drawString(1*inch, y - 0.55*inch, f"Date: {claim['report_date']}")

    c.save()



def create_legal_demand_pdf(path: Path, claim: Dict):
    """
    Detailed Legal Demand Letter PDF
    """
    c = canvas.Canvas(str(path), pagesize=LETTER)
    width, height = LETTER
    
    # Law Firm Header
    c.setFont("Helvetica-Bold", 14)
    firm_name = random.choice(["Johnson & Associates", "Smith Legal Group", "Williams Law Firm", "Brown & Partners LLP"])
    c.drawString(1*inch, height - 0.75*inch, firm_name.upper())
    
    c.setFont("Helvetica", 9)
    c.drawString(1*inch, height - 1*inch, "Attorneys at Law")
    c.drawString(1*inch, height - 1.15*inch, f"{rand_address()}")
    c.drawString(1*inch, height - 1.3*inch, f"{claim['city']}, {claim['state']} {claim['zip']}")
    c.drawString(1*inch, height - 1.45*inch, f"Phone: {rand_phone()} | Fax: {rand_phone()}")
    
    # Date
    y = height - 2*inch
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, y, f"Date: {claim['report_date']}")
    
    # Recipient
    y -= 0.4*inch
    c.drawString(1*inch, y, f"{claim['carrier']}")
    y -= 0.15*inch
    c.drawString(1*inch, y, "Claims Department")
    y -= 0.15*inch
    c.drawString(1*inch, y, "P.O. Box 12345")
    y -= 0.15*inch
    c.drawString(1*inch, y, f"{random.choice(['Dallas', 'Houston', 'Phoenix'])}, {random.choice(['TX', 'AZ'])} {random.randint(70000, 85000)}")
    
    # RE line
    y -= 0.35*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, f"RE: Demand for Settlement - {claim['insured_name']}")
    y -= 0.15*inch
    c.setFont("Helvetica", 10)
    c.drawString(1.3*inch, y, f"Claim Number: {claim['claim_number']}")
    y -= 0.15*inch
    c.drawString(1.3*inch, y, f"Date of Loss: {claim['loss_date']}")
    y -= 0.15*inch
    c.drawString(1.3*inch, y, f"Your Insured: {claim['insured_name']}")
    
    # Body
    y -= 0.4*inch
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, y, "Dear Claims Adjuster:")
    
    y -= 0.35*inch
    body_lines = [
        f"This firm represents {claim['insured_name']} in connection with the above-referenced claim.",
        f"On {claim['loss_date']}, our client sustained injuries and property damage as a direct result of",
        f"the incident described in your claim file. Our client has incurred substantial medical expenses,",
        "lost wages, and continues to suffer from pain and limitations in daily activities.",
        "",
        "DAMAGES SUMMARY:",
        f"  Medical Expenses: ${random.randint(8000, 35000):,}",
        f"  Lost Wages: ${random.randint(3000, 15000):,}",
        f"  Property Damage: ${claim['claim_amount']:,}",
        f"  Pain and Suffering: ${random.randint(25000, 75000):,}",
        "",
        f"TOTAL DEMAND: ${claim['claim_amount'] + random.randint(30000, 100000):,}",
        "",
        "This demand is made in good faith based on the injuries, damages, and losses sustained by our",
        "client. We request that you respond to this demand within 30 days of receipt. Should you fail to",
        "respond appropriately, we are prepared to pursue all available legal remedies including filing suit.",
        "",
        "Please direct all communications to our office.",
        "",
        "Sincerely,",
    ]
    
    for line in body_lines:
        c.drawString(1*inch, y, line[:95])
        y -= 0.15*inch
        if y < 1.5*inch:
            c.showPage()
            y = height - 1*inch
            c.setFont("Helvetica", 10)
    
    # Signature
    y -= 0.2*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, random.choice(["John Smith, Esq.", "Sarah Johnson, Esq.", "Robert Williams, Esq."]))
    y -= 0.15*inch
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, y, firm_name)
    y -= 0.15*inch
    c.drawString(1*inch, y, f"Attorney for {claim['insured_name']}")
    
    c.save()


def create_damage_image(path: Path, text: str):
    """
    Create realistic-looking damage photo placeholder
    """
    img = Image.new("RGB", (800, 600), color=(45, 45, 45))
    draw = ImageDraw.Draw(img)
    
    # Add some visual noise/texture
    for _ in range(100):
        x = random.randint(0, 800)
        y = random.randint(0, 600)
        color = (random.randint(30, 60), random.randint(30, 60), random.randint(30, 60))
        draw.rectangle([x, y, x+random.randint(20, 80), y+random.randint(20, 80)], fill=color)
    
    # Add damage label
    draw.rectangle([20, 20, 400, 80], fill=(180, 40, 40))
    draw.text((30, 35), text, fill=(255, 255, 255))
    draw.text((30, 55), f"Photo taken: {datetime.now().strftime('%m/%d/%Y')}", fill=(255, 255, 255))
    
    img.save(path)


# ---------------------------------------------------------------------
# Email body templates
# ---------------------------------------------------------------------

def auto_email_body(claim: Dict) -> str:
    return f"""Dear {claim['carrier']} Claims Team,

I am submitting an auto insurance claim for the incident that occurred on {claim['loss_date']} involving my {claim['vehicle_year']} {claim['vehicle_make']} {claim['vehicle_model']} under policy number {claim['policy_number']}.

The incident took place in {claim['city']}, {claim['state']}. {'I sustained injuries requiring medical attention.' if claim['has_injury'] else 'Fortunately, no injuries were sustained.'} The vehicle sustained significant damage as documented in the attached photographs and repair estimate.

Attached Documents:
 - ACORD 25 Certificate of Liability Insurance
 - Repair Estimate
{' - Medical Report and Treatment Records' if claim['has_injury'] else ''}
{' - Police Accident Report' if claim['has_police'] else ''}
{' - Legal Demand Letter (representation by attorney)' if claim['has_legal'] else ''}
 - Damage Photographs

Claim Number: {claim['claim_number']}
Estimated Damage: ${claim['claim_amount']:,}

Please contact me at {claim['phone']} or {claim['email']} with any questions.

Thank you for your prompt attention to this matter.

Regards,
{claim['insured_name']}
Phone: {claim['phone']}
Email: {claim['email']}"""


def home_email_body(claim: Dict) -> str:
    return f"""Dear {claim['carrier']} Claims Department,

I am filing a homeowners insurance claim for property damage that occurred on {claim['loss_date']} at my residence located at {claim['address']}, {claim['city']}, {claim['state']} {claim['zip']}.

Policy Number: {claim['policy_number']}
Loss Type: {claim['category']}

The property sustained damage due to {claim['category'].lower()}. {'Medical attention was required.' if claim['has_injury'] else 'No injuries occurred.'} I have secured the property and taken measures to prevent further damage.

Attached Documents:
 - ACORD 140 Property Loss Notice
 - Repair/Restoration Estimate
{' - Medical Documentation' if claim['has_injury'] else ''}
{' - Police Report' if claim['has_police'] else ''}
{' - Legal Representation Notice' if claim['has_legal'] else ''}
 - Damage Photographs

Claim Number: {claim['claim_number']}
Estimated Damage: ${claim['claim_amount']:,}

Please send an adjuster at your earliest convenience. I can be reached at {claim['phone']} or {claim['email']}.

Sincerely,
{claim['insured_name']}
Phone: {claim['phone']}
Email: {claim['email']}"""


# ---------------------------------------------------------------------
# Claim generators
# ---------------------------------------------------------------------

def generate_auto_claim(idx: int) -> Dict:
    fn, ln, full = rand_name()
    city, state = random.choice(CITIES_STATES)
    addr = rand_address()
    zipc = f"{random.randint(10000, 99999)}"
    loss, report = rand_dates()
    make, model = random.choice(VEHICLES)
    year = random.randint(2015, 2020)

    category = random.choice(AUTO_CATEGORIES)
    has_injury = random.random() < 0.3
    has_police = category in ["Collision", "Uninsured Motorist", "Comprehensive"]
    is_high_cost = random.random() < 0.3
    has_legal = random.random() < 0.2

    base = random.randint(3000, 15000)
    if is_high_cost:
        base += random.randint(15000, 40000)
    if has_injury:
        base += random.randint(5000, 30000)
    if has_legal:
        base += random.randint(5000, 15000)

    claim = {
        "claim_number": f"CLM-AU{idx:04d}",
        "policy_number": f"AU{1000000 + idx}",
        "claim_type": AUTO,
        "category": category,
        "insured_name": full,
        "first_name": fn,
        "last_name": ln,
        "email": f"{fn.lower()}.{ln.lower()}@example.com",
        "phone": rand_phone(),
        "address": addr,
        "city": city,
        "state": state,
        "zip": zipc,
        "loss_date": loss.strftime("%m/%d/%Y"),
        "report_date": report.strftime("%m/%d/%Y"),
        "vehicle_year": year,
        "vehicle_make": make,
        "vehicle_model": model,
        "vin": rand_vin(),
        "carrier": random.choice(INSURANCE_COMPANIES),
        "claim_amount": base,
        "has_injury": has_injury,
        "has_police": has_police,
        "has_legal": has_legal,
        "severity_score": 30
            + (25 if has_injury else 0)
            + (20 if is_high_cost else 0)
            + (15 if has_legal else 0),
    }
    claim["severity_score"] = min(claim["severity_score"], 100)
    return claim


def generate_home_claim(idx: int) -> Dict:
    fn, ln, full = rand_name()
    city, state = random.choice(CITIES_STATES)
    addr = rand_address()
    zipc = f"{random.randint(10000, 99999)}"
    loss, report = rand_dates()

    category = random.choice(HOME_CATEGORIES)
    has_injury = random.random() < 0.2
    has_police = category in ["Theft", "Vandalism"]
    is_high_cost = random.random() < 0.35
    has_legal = random.random() < 0.15

    base = random.randint(5000, 25000)
    if is_high_cost:
        base += random.randint(30000, 120000)
    if has_injury:
        base += random.randint(8000, 40000)
    if has_legal:
        base += random.randint(5000, 25000)

    claim = {
        "claim_number": f"CLM-HO{idx:04d}",
        "policy_number": f"HO{2000000 + idx}",
        "claim_type": HOME,
        "category": category,
        "insured_name": full,
        "first_name": fn,
        "last_name": ln,
        "email": f"{fn.lower()}.{ln.lower()}@example.com",
        "phone": rand_phone(),
        "address": addr,
        "city": city,
        "state": state,
        "zip": zipc,
        "loss_date": loss.strftime("%m/%d/%Y"),
        "report_date": report.strftime("%m/%d/%Y"),
        "property_type": random.choice(["Single Family", "Condo", "Townhouse"]),
        "year_built": random.randint(1970, 2015),
        "carrier": random.choice(INSURANCE_COMPANIES),
        "claim_amount": base,
        "has_injury": has_injury,
        "has_police": has_police,
        "has_legal": has_legal,
        "severity_score": 30
            + (25 if has_injury else 0)
            + (20 if is_high_cost else 0)
            + (15 if has_legal else 0),
    }
    claim["severity_score"] = min(claim["severity_score"], 100)
    return claim


# ---------------------------------------------------------------------
# Write email.eml + attachments as PDFs
# ---------------------------------------------------------------------

def write_claim_folder(claim: Dict, idx: int):
    if claim["claim_type"] == "AUTO":
        folder = RAW_DIR / f"CLM-AU{idx:04d}"
    else:
        folder = RAW_DIR / f"CLM-HO{idx:04d}"
    folder.mkdir(parents=True, exist_ok=True)

    # email.eml
    msg = EmailMessage()
    msg["From"] = claim["email"]
    msg["To"] = "claims@" + claim["carrier"].replace(" ", "").lower() + ".com"
    msg["Subject"] = f"{claim['claim_type']} Claim - {claim['claim_number']}"

    if claim["claim_type"] == "AUTO":
        body = auto_email_body(claim)
    else:
        body = home_email_body(claim)

    msg.set_content(body)

    eml_path = folder / "email.eml"
    with open(eml_path, "wb") as f:
        f.write(msg.as_bytes())

    # Generate PDFs
    if claim["claim_type"] == "AUTO":
        acord_pdf = folder / f"ACORD25_{claim['claim_number']}.pdf"
        create_acord25_pdf(acord_pdf, claim)
    else:
        acord_pdf = folder / f"ACORD140_{claim['claim_number']}.pdf"
        create_acord140_pdf(acord_pdf, claim)

    repair_pdf = folder / f"REPAIR_EST_{claim['claim_number']}.pdf"
    # Simple repair estimate (you can enhance this similarly)
    c = canvas.Canvas(str(repair_pdf), pagesize=LETTER)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, 10*inch, "REPAIR ESTIMATE")
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, 9.5*inch, f"Customer: {claim['insured_name']}")
    c.drawString(1*inch, 9.3*inch, f"Claim: {claim['claim_number']}")
    c.drawString(1*inch, 9*inch, f"Total Estimated Repairs: ${claim['claim_amount']:,}")
    c.drawString(1*inch, 8.7*inch, f"Prepared for: {claim['carrier']}")
    c.save()

    if claim["has_injury"]:
        med_pdf = folder / f"MEDICAL_{claim['claim_number']}.pdf"
        create_medical_report_pdf(med_pdf, claim)

    if claim["has_police"] and claim["claim_type"] == "AUTO":
        police_pdf = folder / f"POLICE_{claim['claim_number']}.pdf"
        create_police_report_pdf(police_pdf, claim)


    if claim["has_legal"]:
        legal_pdf = folder / f"LEGAL_{claim['claim_number']}.pdf"
        create_legal_demand_pdf(legal_pdf, claim)

    # Generate 1-2 damage images only
    num_imgs = random.randint(1, 2)
    for i in range(1, num_imgs + 1):
        img_path = folder / f"DAMAGE_{i}_{claim['claim_number']}.png"
        damage_desc = f"{claim['claim_type']} {claim['category']} - Photo {i}"
        create_damage_image(img_path, damage_desc)

    print(f"[GEN] {claim['claim_type']} -> {folder.name}")


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main(total: int = 500):
    auto_n = total // 2
    home_n = total - auto_n

    for i in range(1, auto_n + 1):
        c = generate_auto_claim(i)
        write_claim_folder(c, i)

    for i in range(1, home_n + 1):
        c = generate_home_claim(i)
        write_claim_folder(c, i)

    print(f"\n DONE: Generated {auto_n} auto + {home_n} home claims with professional PDFs.")


if __name__ == "__main__":
    main(500)
