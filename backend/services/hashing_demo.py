"""Separate educational password-hashing demonstration.

This module is intentionally not connected to the analyzer's persistent
analytics path. It demonstrates the concept using Werkzeug's password
hashing helpers and should only be used with synthetic demo passwords.
"""
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(demo_password):
    return generate_password_hash(demo_password)

def verify_password(stored_hash, demo_password):
    return check_password_hash(stored_hash, demo_password)
