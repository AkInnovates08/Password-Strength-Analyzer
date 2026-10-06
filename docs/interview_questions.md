# Interview Preparation — 10 Questions and Answers

## 1. Explain your project.

I built a defensive Password Strength Analyzer and Security Suggestion Tool using Python Flask, JavaScript, and SQLite. It analyzes password length, character diversity, common-password matches, sequences, keyboard patterns, repetition, predictable structures, optional personal-context overlap, and a theoretical entropy estimate. It produces a project-defined 0–100 score, classification, findings, and specific security recommendations. A key design decision is privacy: passwords are processed transiently and are not stored, logged, returned, or used in analytics.

## 2. How do you measure password strength?

I do not rely only on uppercase, lowercase, numbers, and symbols. I combine length, diversity, unique-character ratio, common-password detection, pattern resistance, repetition, keyboard sequences, predictable word-number structures, and optional context overlap. The final score is a project-defined heuristic.

## 3. What is entropy?

Entropy is a theoretical measure of uncertainty. A simple educational estimate is `L × log2(N)`, where L is length and N is the estimated character pool. It assumes random selection, so it can overestimate the strength of human-created passwords.

## 4. Why detect patterns?

Predictable sequences, keyboard walks, repetitions, and common word-number combinations reduce effective unpredictability even when the password appears complex.

## 5. Why should plaintext passwords not be stored?

Plaintext storage means a database compromise can directly expose credentials. Production authentication systems should use dedicated password-hashing functions with salts and appropriate work factors.

## 6. What is salting?

A salt is a unique value combined with a password before hashing. It helps prevent identical passwords from producing identical stored hashes and makes precomputed lookup attacks less useful.

## 7. What is the difference between policy and strength?

A policy is a configurable set of requirements, such as minimum length. Strength is an assessment of unpredictability and weaknesses. A password can pass a policy while still being predictable.

## 8. How does your project protect privacy?

The analyzer does not persist passwords. The API response excludes the password. Analytics stores only aggregate metadata. Optional personal context is processed locally and is not stored.

## 9. Why use `secrets` instead of `random`?

`secrets` is designed for security-sensitive random generation and uses a cryptographically secure source. The standard `random` module is intended for general-purpose randomness and should not be used for security-sensitive secrets.

## 10. Why is MFA still needed?

A strong password does not eliminate phishing, credential theft, session attacks, or other authentication threats. MFA adds another authentication factor and reduces the impact of a compromised password.
