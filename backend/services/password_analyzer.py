import math
import re
from pathlib import Path
from .pattern_detector import (
    detect_keyboard_patterns,
    detect_repetition,
    detect_sequences,
    detect_predictable_structure,
)
from .entropy_estimator import estimate_theoretical_entropy
from .scoring_engine import calculate_score
from .suggestion_engine import generate_suggestions

BASE_DIR = Path(__file__).resolve().parents[2]
COMMON_FILE = BASE_DIR / "data" / "common_passwords.txt"

def load_common_passwords():
    if not COMMON_FILE.exists():
        return set()
    return {
        line.strip().casefold()
        for line in COMMON_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }

COMMON_PASSWORDS = load_common_passwords()

def analyze_length(password):
    length = len(password)
    if length < 8:
        band = "Very short"
    elif length <= 11:
        band = "Short"
    elif length <= 15:
        band = "Better length"
    else:
        band = "Strong length contribution"
    return {"length": length, "band": band}

def analyze_characters(password):
    types = {
        "lowercase": any(c.islower() for c in password),
        "uppercase": any(c.isupper() for c in password),
        "digits": any(c.isdigit() for c in password),
        "symbols": any(not c.isalnum() and not c.isspace() for c in password),
        "spaces": any(c.isspace() for c in password),
    }
    unique = len(set(password))
    length = len(password)
    return {
        **types,
        "unique_character_count": unique,
        "character_type_count": sum(types[k] for k in ("lowercase", "uppercase", "digits", "symbols")),
        "unique_character_ratio": round(unique / length, 3) if length else 0,
    }

def is_common_password(password):
    return password.casefold() in COMMON_PASSWORDS

def detect_personal_context(password, context):
    findings = []
    normalized = password.casefold()
    labels = {
        "first_name": "first name",
        "birth_year": "birth year",
        "company_college": "company or college name",
    }
    for key, label in labels.items():
        value = str(context.get(key, "")).strip().casefold()
        if value and len(value) >= 3 and value in normalized:
            findings.append({
                "type": "personal_information",
                "severity": "high",
                "description": f"Password appears to contain the supplied {label}."
            })
    return findings

def analyze_password(password, context=None):
    context = context or {}
    length_metrics = analyze_length(password)
    char_metrics = analyze_characters(password)
    common = is_common_password(password)
    sequences = detect_sequences(password)
    keyboard = detect_keyboard_patterns(password)
    repetition = detect_repetition(password)
    predictable = detect_predictable_structure(password)
    personal = detect_personal_context(password, context)
    entropy = estimate_theoretical_entropy(password, char_metrics)

    findings = []
    if length_metrics["length"] < 8:
        findings.append({"type": "short_length", "severity": "high", "description": "Password is very short."})
    elif length_metrics["length"] < 12:
        findings.append({"type": "short_length", "severity": "medium", "description": "Password is shorter than the recommended educational target."})

    if char_metrics["character_type_count"] <= 1 and password:
        findings.append({"type": "low_diversity", "severity": "medium", "description": "Password uses only one character category."})
    if common:
        findings.append({"type": "common_password", "severity": "critical",
                         "description": "Your password matches a commonly used password pattern and should not be used."})
    findings.extend(sequences)
    findings.extend(keyboard)
    findings.extend(repetition)
    findings.extend(predictable)
    findings.extend(personal)

    score = calculate_score(
        length_metrics, char_metrics, common, sequences, keyboard,
        repetition, predictable, personal, password
    )
    classification = (
        "VERY WEAK" if score <= 20 else
        "WEAK" if score <= 40 else
        "MODERATE" if score <= 60 else
        "STRONG" if score <= 80 else
        "VERY STRONG"
    )
    suggestions = generate_suggestions(findings, length_metrics, char_metrics, common)

    return {
        "score": score,
        "classification": classification,
        "findings": findings,
        "suggestions": suggestions,
        "metrics": {
            **length_metrics,
            **char_metrics,
            "common_password": common,
            "sequence_count": len(sequences),
            "keyboard_pattern_count": len(keyboard),
            "repetition_count": len(repetition),
            "predictable_structure_count": len(predictable),
            "personal_information_count": len(personal),
            "finding_count": len(findings),
            "theoretical_entropy_bits": entropy,
            "entropy_note": "Educational estimate only; it assumes random character selection and can be optimistic for human-created passwords."
        }
    }
