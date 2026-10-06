def calculate_score(length_metrics, char_metrics, common, sequences, keyboard,
                    repetition, predictable, personal, password):
    """Project-defined educational 0-100 score.

    The score deliberately gives strong negative weight to predictable patterns.
    It is not a universal security standard and must not be interpreted as one.
    """
    score = 0

    length = length_metrics["length"]
    if length >= 16:
        score += 35
    elif length >= 12:
        score += 28
    elif length >= 8:
        score += 18
    elif length > 0:
        score += 6

    score += min(15, char_metrics["character_type_count"] * 4)
    score += min(10, round(char_metrics["unique_character_ratio"] * 10))

    # Pattern resistance contribution is earned only when major weakness
    # signals are absent. This prevents composition rules from overpowering
    # obvious predictability such as Password123! or qwerty2026!.
    major_pattern_count = len(sequences) + len(keyboard) + len(repetition) + len(predictable) + len(personal)
    score += max(0, 20 - min(20, major_pattern_count * 8))

    if not common:
        score += 10
    else:
        score -= 40

    # Strong additional unpredictability bonus only for clean inputs.
    if length >= 20 and char_metrics["unique_character_ratio"] >= 0.65 and not predictable and not repetition:
        score += 10

    # Specific penalties. These are intentionally heuristic and educational.
    score -= len(sequences) * 12
    score -= len(keyboard) * 15
    score -= len(repetition) * 30
    score -= len(predictable) * 30
    score -= len(personal) * 15

    # Low diversity should reduce the score even when the password is long.
    if char_metrics["character_type_count"] <= 1:
        score -= 8

    return max(0, min(100, int(score)))
