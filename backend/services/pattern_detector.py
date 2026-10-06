import re

KEYBOARD_PATTERNS = (
    "qwerty", "asdf", "zxcv", "qwertyuiop", "asdfgh", "zxcvbn",
    "123qwe", "qwe123"
)

def detect_sequences(password, min_run=4):
    findings = []
    if len(password) < min_run:
        return findings

    lower = password.casefold()
    for i in range(len(lower) - min_run + 1):
        chunk = lower[i:i+min_run]
        codes = [ord(c) for c in chunk]
        if all(codes[j] + 1 == codes[j+1] for j in range(len(codes)-1)):
            findings.append({"type": "ascending_sequence", "severity": "medium",
                             "description": "Predictable ascending character sequence detected."})
            break
        if all(codes[j] - 1 == codes[j+1] for j in range(len(codes)-1)):
            findings.append({"type": "descending_sequence", "severity": "medium",
                             "description": "Predictable descending character sequence detected."})
            break
    return findings

def detect_keyboard_patterns(password):
    lower = password.casefold()
    findings = []
    for pattern in KEYBOARD_PATTERNS:
        if pattern in lower:
            findings.append({"type": "keyboard_pattern", "severity": "high",
                             "description": "Common keyboard pattern detected."})
            break
    return findings

def detect_repetition(password):
    findings = []
    if not password:
        return findings
    if re.search(r"(.)\1\1\1", password):
        findings.append({"type": "repeated_characters", "severity": "high",
                         "description": "Repeated character pattern detected."})
    # Repeated substrings of length 2-4.
    for size in range(2, 5):
        if len(password) >= size * 3:
            for i in range(len(password) - size * 2):
                unit = password[i:i+size]
                if unit * 3 in password:
                    findings.append({"type": "repeated_substring", "severity": "high",
                                     "description": "Repeated substring pattern detected."})
                    return findings
    return findings

def detect_predictable_structure(password):
    findings = []
    lower = password.casefold()
    common_words = ("password", "welcome", "admin", "hello", "letmein", "qwerty")
    if re.search(r"(password|welcome|admin|hello|letmein|qwerty)[!@#$%^&*]*\d{1,4}[!@#$%^&*]*$", lower):
        findings.append({"type": "predictable_word_number", "severity": "high",
                         "description": "Common word followed by a predictable number/symbol pattern detected."})
    if re.search(r"(19\d{2}|20\d{2})", lower):
        findings.append({"type": "year_pattern", "severity": "medium",
                         "description": "Year/date-like numeric pattern detected."})
    if any(word in lower for word in common_words) and len(password) < 16:
        findings.append({"type": "common_word", "severity": "medium",
                         "description": "Common dictionary-style word detected."})
    return findings
