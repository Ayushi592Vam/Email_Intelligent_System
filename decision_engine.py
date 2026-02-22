# decision_engine.py
from typing import Dict, List


def decide_claim(
    current_claim: Dict,
    similar_claims: List[Dict]
) -> Dict:
    """
    Rule-based decision engine.
    LLM is NOT used here.
    """

    # -----------------------------
    # SAFETY CHECK
    # -----------------------------
    if not similar_claims:
        return {
            "decision": "MANUAL_REVIEW",
            "reason": "No similar claims found"
        }

    # -----------------------------
    # EXTRACT SIGNALS
    # -----------------------------
    max_similarity = max(c["similarity_score"] for c in similar_claims)

    severity = current_claim.get("severity")
    has_medical = current_claim.get("has_medical", False)
    has_legal = current_claim.get("has_legal", False)

    # -----------------------------
    # DECISION RULES
    # -----------------------------
    if (
        max_similarity >= 0.95
        and severity == "LOW"
        and not has_medical
        and not has_legal
    ):
        decision = "AUTO_APPROVE"
        reason = "Highly similar to historical low-risk claims"

    elif max_similarity >= 0.75:
        decision = "MANUAL_REVIEW"
        reason = "Moderate similarity to past claims"

    elif severity == "HIGH" or has_medical or has_legal:
        decision = "ESCALATE"
        reason = "High severity or legal/medical involvement"

    else:
        decision = "LLM_JUDGE"
        reason = "Unclear pattern, requires semantic judgment"

    return {
        "decision": decision,
        "max_similarity": round(max_similarity, 3),
        "reason": reason
    }