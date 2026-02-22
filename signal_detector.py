from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent
ENTITIES_DIR = BASE_DIR / "data" / "entities"
SIGNALS_DIR = BASE_DIR / "data" / "signals"
SIGNALS_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------
# SIGNAL DETECTION LOGIC
# -------------------------------------------------

def detect_signals(entities: dict):

    signals = []
    severity_score = 0

    amount = int(entities.get("estimated_amount") or 0)

    # ---- MEDICAL / INJURY SIGNAL
    if entities.get("injuries_reported"):
        signals.append("INJURY_REPORTED")
        severity_score += 30

    # ---- POLICE SIGNAL
    if entities.get("police_report"):
        signals.append("POLICE_INVOLVEMENT")
        severity_score += 20

    # ---- LEGAL SIGNAL
    if entities.get("legal_involvement"):
        signals.append("LEGAL_INVOLVEMENT")
        severity_score += 40

    # ---- HIGH VALUE SIGNAL
    if amount > 50000:
        signals.append("SEVERE_LOSS_AMOUNT")
        severity_score += 40
    elif amount > 25000:
        signals.append("HIGH_LOSS_AMOUNT")
        severity_score += 25

    # ---- CLAIM TYPE SPECIFIC SIGNALS
    if entities.get("claim_type") == "AUTO" and entities.get("injuries_reported"):
        signals.append("AUTO_BODILY_INJURY")
        severity_score += 20

    if entities.get("claim_type") == "HOME" and entities.get("loss_type"):
        signals.append(f"HOME_LOSS_{entities['loss_type'].upper().replace(' ', '_')}")

    # ---- FINAL SEVERITY
    if severity_score >= 80:
        severity = "CRITICAL"
    elif severity_score >= 60:
        severity = "HIGH"
    elif severity_score >= 30:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return {
        "claim_number": entities.get("claim_number"),
        "claim_type": entities.get("claim_type"),
        "severity": severity,
        "severity_score": severity_score,
        "signals_detected": signals
    }

# -------------------------------------------------
# BATCH RUNNER
# -------------------------------------------------

def main():
    print("🚀 Running Signal Detection...")

    for folder in ENTITIES_DIR.iterdir():
        if not folder.is_dir():
            continue

        entity_file = folder / "ENTITIES.json"
        if not entity_file.exists():
            continue

        with open(entity_file) as f:
            entities = json.load(f)

        signals = detect_signals(entities)

        out_folder = SIGNALS_DIR / folder.name
        out_folder.mkdir(exist_ok=True)

        with open(out_folder / "SIGNALS.json", "w") as f:
            json.dump(signals, f, indent=2)

    print(" SIGNAL DETECTION COMPLETE")

if __name__ == "__main__":
    main()