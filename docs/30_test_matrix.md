# 30-Test Matrix

| ID | Scenario | Input | Expected |
|---|---|---|---|
| T01 | Empty password | empty | score 0 / ready-safe result |
| T02 | One character | `a` | very weak |
| T03 | Short numeric | `123456` | very weak |
| T04 | Common password | `password` | common-password finding |
| T05 | Long repeated | `aaaaaaaaaaaaaaaa` | repetition finding |
| T06 | Lowercase only | `abcdefghijklmno` | low diversity |
| T07 | Uppercase only | `ABCDEFGHIJKLMNO` | low diversity |
| T08 | Numbers only | `1234567890123456` | low diversity/predictability |
| T09 | Symbols only | `!!!!!!!!!!!!!!!!!` | repetition |
| T10 | Mixed characters | synthetic mixed string | higher score |
| T11 | Ascending numbers | `abcd1234` | sequence |
| T12 | Reverse numbers | `987654` | sequence |
| T13 | Sequential letters | `abcdefXYZ` | sequence |
| T14 | Keyboard sequence | `qwerty` | keyboard pattern |
| T15 | Repeated characters | `AAAAAA123!` | repetition |
| T16 | Repeated substring | `abcabcabc` | repeated substring |
| T17 | Common word + number | `welcome123` | predictable structure |
| T18 | Word + year | `admin2026` | year/predictability |
| T19 | Personal name overlap | context `Rahul`, password `Rahul@123` | personal info |
| T20 | Birth year overlap | context `2002`, password `Demo2002!` | personal info |
| T21 | Long passphrase-like | synthetic long input | length contribution |
| T22 | Unicode | `Pässwörd!123456` | handled without crash |
| T23 | Spaces | `long demo phrase 2026!` | handled according to policy |
| T24 | Max supported | 128 chars | accepted |
| T25 | Score boundaries | calibrated synthetic inputs | 0–100 |
| T26 | Suggestions | predictable demo | specific suggestions |
| T27 | Generator | length 20 | secure random output |
| T28 | Password not stored | API analysis | no password field |
| T29 | Password not logged | source review | no application password logging |
| T30 | Analytics | several analyses | metadata only |
