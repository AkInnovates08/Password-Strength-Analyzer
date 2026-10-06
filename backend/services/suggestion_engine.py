def generate_suggestions(findings, length_metrics, char_metrics, common):
    suggestions = []
    types = {f["type"] for f in findings}

    if length_metrics["length"] < 16:
        suggestions.append("Consider using a longer password or passphrase.")
    if common:
        suggestions.append("Do not use a commonly used password.")
    if "ascending_sequence" in types or "descending_sequence" in types:
        suggestions.append("Your password contains a predictable numeric or character sequence.")
    if "keyboard_pattern" in types:
        suggestions.append("Avoid common keyboard sequences such as qwerty.")
    if "repeated_characters" in types or "repeated_substring" in types:
        suggestions.append("Avoid repeated characters or repeated substrings.")
    if "predictable_word_number" in types or "year_pattern" in types:
        suggestions.append("Avoid predictable words, years, and date-like suffixes.")
    if "personal_information" in types:
        suggestions.append("Avoid including your name, birth year, company, or college information.")
    if char_metrics["character_type_count"] <= 1:
        suggestions.append("Use a more varied character set when it does not reduce usability.")
    suggestions.extend([
        "Avoid reusing passwords across different accounts.",
        "Use a password manager to generate and store unique passwords.",
        "Enable MFA where available."
    ])
    # Preserve order while removing duplicates.
    return list(dict.fromkeys(suggestions))
