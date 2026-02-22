from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent

SIGNAL_DIR = BASE_DIR / "data" / "signals"
FILE_TAG_DIR = BASE_DIR / "data" / "file_tags"
OUT_DIR = BASE_DIR / "data" / "feature_store"

OUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------
# HELPERS
# ---------------------------------------

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

# ---------------------------------------
# FEATURE STORE BUILDER
# ---------------------------------------

def build_feature_store():
    for claim_folder in SIGNAL_DIR.iterdir():
        if not claim_folder.is_dir():
            continue

        claim_id = claim_folder.name

        # -------- Load signal output --------
        signal_file = claim_folder / "SIGNALS.json"
        if not signal_file.exists():
            continue

        signal_data = load_json(signal_file)

        # -------- Load file tags --------
        file_tag_file = FILE_TAG_DIR / claim_id / "FILE_TAGS.json"
        if not file_tag_file.exists():
            continue

        file_tags = load_json(file_tag_file)

        # -----------------------------------
        # FEATURE ENGINEERING
        # -----------------------------------

        all_tags = set()
        num_photos = 0

        for filename, tags in file_tags.items():
            # collect tags
            for t in tags:
                all_tags.add(t)

            # ✅ PHOTO COUNT — filename based ONLY
            fname = filename.lower()
            if any(x in fname for x in ["damage", "photo", "img", "image"]):
                num_photos += 1

        features = {
            "claim_number": signal_data["claim_number"],
            "claim_type": signal_data["claim_type"],

            # Presence flags
            "has_medical": "MEDICAL" in all_tags,
            "has_police": "POLICE" in all_tags,
            "has_legal": "LEGAL" in all_tags,

            # Counts
            "num_attachments": len(file_tags),
            "num_photos": num_photos,

            # Risk output
            "severity": signal_data["severity"],
            "severity_score": signal_data["severity_score"],

            # Explainability
            "signals": signal_data["signals_detected"],
            "files_present": sorted(list(all_tags))
        }

        # -----------------------------------
        # SAVE FEATURE STORE
        # -----------------------------------

        out_file = OUT_DIR / f"{claim_id}.json"
        with open(out_file, "w") as f:
            json.dump(features, f, indent=2)

    print("✅ FEATURE STORE CREATED SUCCESSFULLY (PHOTO COUNT FIXED)")

# ---------------------------------------
# RUN
# ---------------------------------------

if __name__ == "__main__":
    build_feature_store()