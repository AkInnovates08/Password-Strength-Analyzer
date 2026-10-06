# Security Test Checklist

| Check | Expected |
|---|---|
| Password stored in SQLite | No |
| Password returned by `/api/analyze` | No |
| Password in URL | No |
| Password in application logs | No application logging |
| Password hash stored for analytics | No |
| Password column in database | No |
| Analyzer input field | `type=password` |
| localStorage password | No |
| sessionStorage password | No |
| Analytics contains only metadata | Yes |
| Generated passwords persisted | No |
| External password service | No by default |
| Password cracking feature | Not implemented |
| Account credential testing | Not implemented |

## Manual browser checks

1. Open DevTools Network.
2. Type a synthetic password.
3. Confirm the password is sent only to the local `/api/analyze` request.
4. Confirm it is not in the URL.
5. Inspect localStorage and sessionStorage.
6. Confirm no password value is persisted.
7. Inspect the SQLite schema and confirm there is no password column.
