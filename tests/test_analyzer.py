import pytest
from services.password_analyzer import analyze_password, analyze_length, analyze_characters

@pytest.mark.parametrize("password, expected_type", [
    ("", "empty"),
    ("a", "short"),
    ("123456", "common"),
    ("password123", "predictable"),
    ("aaaaaaaaaaaaaaaa", "repetition"),
    ("qwerty2026!", "keyboard"),
    ("abcd1234", "sequence"),
    ("Welcome2026!", "predictable"),
    ("AbC!93xP#71mQ2z@", "mixed"),
    ("A B c 7 ! x Y 2", "spaces"),
])
def test_demo_cases(password, expected_type):
    result = analyze_password(password)
    assert "score" in result
    assert 0 <= result["score"] <= 100
    assert result["classification"] in {"VERY WEAK","WEAK","MODERATE","STRONG","VERY STRONG"}

def test_length_bands():
    assert analyze_length("a")["band"] == "Very short"
    assert analyze_length("abcdefgh")["band"] == "Short"
    assert analyze_length("abcdefghijkl")["band"] == "Better length"
    assert analyze_length("a"*16)["band"] == "Strong length contribution"

def test_character_metrics():
    m = analyze_characters("Aa1!")
    assert m["character_type_count"] == 4
    assert m["unique_character_count"] == 4
    assert m["unique_character_ratio"] == 1.0

def test_common_password_never_returned():
    result = analyze_password("password123")
    serialized = str(result)
    assert "password123" not in serialized

def test_personal_context():
    result = analyze_password("Rahul@123", {"first_name": "Rahul"})
    assert any(f["type"] == "personal_information" for f in result["findings"])

def test_entropy_is_not_the_only_signal():
    result = analyze_password("Password123!")
    assert result["metrics"]["theoretical_entropy_bits"] > 0
    assert result["metrics"]["finding_count"] > 0
