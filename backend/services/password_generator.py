import secrets
import string

def generate_password(length=20, uppercase=True, lowercase=True, digits=True, symbols=True):
    pools = []
    if uppercase: pools.append(string.ascii_uppercase)
    if lowercase: pools.append(string.ascii_lowercase)
    if digits: pools.append(string.digits)
    if symbols: pools.append("!@#$%^&*()-_=+[]{}:,.?")

    if not pools:
        raise ValueError("At least one character type is required.")
    if length < len(pools):
        raise ValueError("Length is too short for the selected character types.")

    # Guarantee at least one character from each selected category.
    result = [secrets.choice(pool) for pool in pools]
    combined = "".join(pools)
    result.extend(secrets.choice(combined) for _ in range(length - len(result)))

    # Secure Fisher-Yates shuffle.
    for i in range(len(result) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        result[i], result[j] = result[j], result[i]
    return "".join(result)
