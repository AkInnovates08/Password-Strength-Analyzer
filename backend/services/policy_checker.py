from .password_analyzer import is_common_password, detect_personal_context

DEFAULT_POLICY = {
    "minimum_length": 12,
    "common_password_check": True,
    "personal_info_check": True,
    "allow_spaces": True,
    "maximum_length": 128,
}

def check_policy(password, policy=None):
    p = {**DEFAULT_POLICY, **(policy or {})}
    failures = []

    if len(password) < int(p["minimum_length"]):
        failures.append(f"Minimum length is {p['minimum_length']}.")
    if len(password) > int(p["maximum_length"]):
        failures.append(f"Maximum supported length is {p['maximum_length']}.")
    if p["common_password_check"] and is_common_password(password):
        failures.append("Password is on the local common-password blocklist.")
    if not p["allow_spaces"] and any(c.isspace() for c in password):
        failures.append("Spaces are not allowed by this policy.")

    # Personal information requires explicit context, so no silent collection occurs.
    context = p.get("context") or {}
    if p["personal_info_check"] and detect_personal_context(password, context):
        failures.append("Password overlaps with supplied personal context.")

    return {
        "policy_pass": not failures,
        "status": "POLICY PASS" if not failures else "POLICY FAIL",
        "failures": failures,
        "policy": p,
    }
