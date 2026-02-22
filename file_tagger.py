from pathlib import Path
import json
import re

BASE_DIR = Path(__file__).resolve().parent
OCR_DIR = BASE_DIR / "data" / "ocr"
OUT_DIR = BASE_DIR / "data" / "file_tags"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------
# STRICT FILE TAGGING (NO MIXING)
# -------------------------------------------------

def tag_single_file(text: str, filename: str):
    name = filename.lower()

    # 🖼️ Photos
    if name.startswith("damage"):
        return {"PHOTOS"}

    # 🚨 Police
    if name.startswith("police"):
        return {"POLICE"}

    # ⚖️ Legal 
    if name.startswith("legal"):
        return {"LEGAL"}

    # 🏥 Medical
    if name.startswith("medical"):
        return {"MEDICAL"}

    # 🛠️ Repair
    if name.startswith("repair"):
        return {"REPAIR_ESTIMATE"}

    # 📄 ACORD
    if name.startswith("acord"):
        return {"ACORD"}

    return {"OTHER"}

# -------------------------------------------------
# BATCH RUN
# -------------------------------------------------

def main():
    for claim_folder in OCR_DIR.iterdir():
        if not claim_folder.is_dir():
            continue

        out_folder = OUT_DIR / claim_folder.name
        out_folder.mkdir(exist_ok=True)

        results = {}
        combined_tags = set()

        for txt_file in claim_folder.glob("*.txt"):
            text = txt_file.read_text(errors="ignore")
            tags = tag_single_file(text, txt_file.name)

            results[txt_file.name] = sorted(tags)

            if txt_file.name != "combined.txt":
                combined_tags.update(tags)

        #  combined = claim-level truth
        results["combined.txt"] = sorted(combined_tags)

        with open(out_folder / "FILE_TAGS.json", "w") as f:
            json.dump(results, f, indent=2)

    print(" FILE TAGGING COMPLETE")

if __name__ == "__main__":
    main()