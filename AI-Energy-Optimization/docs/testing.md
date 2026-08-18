# Software Testing & Validation

## 1. Testing Strategy
A comprehensive multi-tier testing strategy was implemented to verify system reliability, correctness, and security across the entire stack:
1. **Unit Testing:** Validates mathematical integrity of cost calculations, dataset preprocessing, and ML prediction inference.
2. **Integration Testing:** Verifies interaction between Flask controllers, SQLite database sessions, and Scikit-Learn pipelines.
3. **Security Testing:** Verifies authentication guards, password hashing, and session management.
4. **Data Validation Testing:** Verifies CSV file format validation, missing value imputation, and error handling for malformed inputs.

---

## 2. Automated Test Suite (`tests/test_app.py`)

| Test Case ID | Test Category | Description | Expected Result | Status |
|---|---|---|---|---|
| `TC-01` | Authentication | Register a new user with valid credentials | User created, seeded with baseline records, session initiated | PASS |
| `TC-02` | Authentication | Duplicate email registration attempt | Error flashed, duplicate account blocked | PASS |
| `TC-03` | Authentication | Login with invalid password | Error flashed, access denied | PASS |
| `TC-04` | Security | Access `/dashboard` without active session | Redirected to `/login` | PASS |
| `TC-05` | Machine Learning | Run single ML prediction with valid inputs | Output between 0.35 kWh and 20 kWh, cost computed correctly | PASS |
| `TC-06` | Machine Learning | Run prediction with extreme temperature (45°C) | Increased cooling load predicted, High usage category assigned | PASS |
| `TC-07` | Preprocessing | Validate empty CSV file upload | Validation error returned with informative message | PASS |
| `TC-08` | Preprocessing | Validate valid CSV file upload | CSV parsed, cleaned, missing values imputed, records ingested | PASS |
| `TC-09` | Cost Calculator | Flat rate calculation (10 kWh @ ₹8/kWh) | Cost equals ₹80.00 | PASS |
| `TC-10` | Cost Calculator | Tiered slab billing calculation | Correct subtotal calculated across Tier 1, 2, and 3 | PASS |
| `TC-11` | Optimization | Energy Saving Simulator slider changes | Proportional kWh and money reductions calculated correctly | PASS |

---

## 3. Running Automated Tests
The automated test suite can be executed using Pytest:

```bash
pytest tests/test_app.py -v
```
