import math

def estimate_theoretical_entropy(password, char_metrics=None):
    if not password:
        return 0.0
    char_metrics = char_metrics or {}
    pool = 0
    if char_metrics.get("lowercase"): pool += 26
    if char_metrics.get("uppercase"): pool += 26
    if char_metrics.get("digits"): pool += 10
    if char_metrics.get("symbols"): pool += 33
    if char_metrics.get("spaces"): pool += 1
    if pool <= 1:
        pool = max(1, len(set(password)))
    return round(len(password) * math.log2(pool), 2)
