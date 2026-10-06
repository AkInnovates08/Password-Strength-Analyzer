# Project Report
## Password Strength Analyzer & Security Suggestion Tool

### Abstract

The Password Strength Analyzer & Security Suggestion Tool is a defensive cybersecurity application designed to educate users about password security and provide a structured assessment of password quality. The application analyzes length, character diversity, common-password exposure, repeated patterns, sequential patterns, keyboard patterns, predictable word-number structures, optional personal-context overlap, and a theoretical entropy-style estimate.

A central privacy requirement is that submitted passwords are never persisted, logged, or returned in API responses. Optional analytics stores only aggregate metadata such as score, classification, length, and finding counts.

### Introduction

Passwords remain an important component of authentication. However, simple composition rules can produce predictable credentials. A password containing uppercase, lowercase, numbers, and symbols can still be weak if it is based on a common word, keyboard sequence, or personal information.

### Problem Statement

Users need understandable feedback about password weaknesses without exposing their passwords to unnecessary storage or external services.

### Objectives

- Analyze passwords locally.
- Explain password weaknesses.
- Detect common and predictable patterns.
- Provide actionable recommendations.
- Demonstrate secure password-generation practices.
- Separate policy compliance from strength scoring.
- Provide privacy-safe aggregate analytics.
- Demonstrate security testing.

### Password Security Background

Password strength is influenced by length and unpredictability. Composition rules are useful signals but are insufficient alone. Password managers and MFA provide important additional protection.

### Authentication Security

Real-world authentication should combine password security with MFA, rate limiting, secure password hashing, abuse protection, session security, phishing resistance, and monitoring.

### Existing Approaches

Basic meters often award points for uppercase, lowercase, numbers, and symbols. This project extends that model with pattern-aware checks and common-password detection while explicitly describing the limitations of heuristic scoring.

### Proposed System

The proposed system accepts a password through a secure web interface and analyzes it in memory. The result includes a score, classification, findings, metrics, and suggestions. Only safe aggregate metadata is optionally persisted.

### Architecture

```text
Web UI -> Flask API -> Analysis Modules -> Score + Findings + Suggestions
                         |
                         +-> Safe Metadata -> SQLite -> Dashboard
```

### Feature Extraction

Features include length, character categories, unique-character count, unique-character ratio, sequences, keyboard patterns, repetitions, common words, common-password matches, year-like structures, and optional context overlap.

### Pattern Detection

The project detects ascending/descending sequences, keyboard patterns such as qwerty/asdf, repeated characters, repeated substrings, and predictable word-number structures.

### Common Password Detection

A small local educational list is used. It is intentionally not a leaked credential corpus.

### Entropy Concepts

The application demonstrates:

`Entropy ≈ L × log2(N)`

This is a theoretical estimate under random selection assumptions. Human-generated passwords may have substantially lower effective unpredictability.

### Strength Scoring

The score is 0–100 and uses project-defined contributions and penalties for length, diversity, unique ratio, pattern resistance, common-password status, and additional unpredictability. The score is not a universal security standard.

### Recommendation Engine

Recommendations are tied to observed findings, such as avoiding keyboard sequences, repeated patterns, common words, predictable years, and personal information.

### Password Generator

The optional generator uses Python's `secrets` module rather than `random` because security-sensitive random generation requires a cryptographically secure source.

### Policy Checker

Policy is evaluated separately from the strength score. Example policy: minimum 12 characters, common-password rejection, optional personal-information checks, and configurable space handling.

### Secure Password Storage Concepts

Production systems should not store plaintext passwords. Appropriate password hashing concepts include Argon2id, bcrypt, scrypt, and PBKDF2 with salts and appropriate work factors. Hashing is not encryption.

### Privacy Design

The analyzer never creates a password database column. Analytics records only score, classification, length, unique ratio, weakness count, timestamps, and finding metadata.

### Dashboard

The dashboard presents total analyses, average score, classification distribution, and weakness frequency. It never reveals actual passwords.

### Testing

The automated suite covers empty input, short passwords, common passwords, repetitions, sequences, keyboard patterns, predictable structures, mixed characters, personal context, generator behavior, policy behavior, API responses, and analytics privacy.

### Security Testing

Security checks verify that:

- passwords are not stored;
- passwords are not returned;
- password strings are not placed in URLs;
- application code does not log passwords;
- analytics has no password column;
- frontend uses password input fields;
- no browser persistence is used for analyzer input.

### Results

The project provides a reproducible defensive demonstration of password analysis, privacy-safe analytics, secure random generation, and authentication-security education.

### Limitations

Heuristic scoring cannot perfectly determine password strength. The common-password list is intentionally small. Entropy estimates can be optimistic for human-generated passwords. Real attacker resistance depends on the attacker model, password predictability, hashing algorithm, work factor, rate limiting, and whether the attack is online or offline.

### Future Scope

Potential improvements include privacy-preserving breach checks, stronger password-strength libraries, enterprise policy configuration, IAM integration, passkey/WebAuthn education, localization, accessibility, and privacy-preserving organization-level reporting.

### Conclusion

The project demonstrates that password security assessment should consider length, unpredictability, pattern resistance, common-password exposure, and context rather than composition rules alone. Its privacy-first architecture makes it suitable as a defensive cybersecurity course project and portfolio artifact.
