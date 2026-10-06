# Password Hashing Demonstration

This is a separate educational module. It is not connected to analytics storage.

Concept:

```text
Synthetic Demo Password
        |
        v
      Salt
        |
        v
Password Hashing Function
        |
        v
    Stored Hash
```

The project demonstrates `hash_password()` and `verify_password()` using Werkzeug helpers.

Important distinction:

- Hashing is intended for one-way verification.
- Encryption is designed for reversible confidentiality.
- Production password storage should use a dedicated password-hashing function and appropriate configuration.
- Do not use arbitrary analyzer input as a persistent credential.
