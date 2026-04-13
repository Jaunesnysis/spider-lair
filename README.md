# Spider's Lair - Web Scraping Puzzles

Solutions to the scraping challenges at (https://bo7.online).
Each puzzle implements a different bot-detection mechanism that must be bypassed.

---

## Project Structure

spider-lair/
├── mysterious-passages/
│ ├── puzzle1.py # The Door of Echoed Steps
│ ├── puzzle2.py # The Clockwork Door
│ ├── puzzle3.py # The Exiled Door
│ ├── rate*test_puzzle1.py
│ ├── rate_test_puzzle2.py
│ └── *\_result.html # Proof of success
├── curious-reflections/
│ ├── puzzle1.py # The Fractured Mirror
│ ├── puzzle2.py # The Silver Veil
│ ├── puzzle3.py # The Mirrored Gaze
│ ├── rate*test_puzzle1.py
│ ├── rate_test_puzzle2.py
│ ├── rate_test_puzzle3.py
│ └── *\_result.html
├── shattered-thresholds/
│ ├── puzzle1.py # The Sleeping Vault
│ ├── puzzle2.py # The Verity Gate
│ ├── rate_test_puzzle1.py
│ ├── rate_test_puzzle2.py
│ └── \*\_result.html
├── requirements.txt
└── README.md

---

## Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/spider-lair.git
cd spider-lair

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install browsers for Playwright
playwright install chromium firefox webkit chrome
```

---

## Mysterious Passages

### Puzzle 1 — The Door of Echoed Steps

**URL:** `https://bo7.online/the_door_of_echoed_steps`

**Mechanism:** Cookie-based authentication. The server sets a session
cookie (`wormhole_token=galactic-cookie-42`) on the homepage.

**Solution:** Use a `requests.Session` to visit the homepage first,
which automatically carries the cookie to subsequent requests.

**Rate test results:**

- 1 req/s → 10/10 success
- 2 req/s → 10/10 success
- 5 req/s → 10/10 success
- Solution is resilient at all tested rates.

```bash
python mysterious-passages/puzzle1.py
python mysterious-passages/rate_test_puzzle1.py
```

---

### Puzzle 2 — The Clockwork Door

**URL:** `https://bo7.online/the_clockwork_door`

**Mechanism:** Rate limiting + cookie-based authentication. The server
sets a cookie on the homepage and enforces a request rate limit —
returning 429 Too Many Requests after ~5 requests".

**Solution:** Visit homepage first to get session cookie, then use
use waiting in case 429 is received.

**Rate test results:**

- 1 req/s → 5/10 success, then 429s after ~5 requests
- 2 req/s → 0/10 success, all 429s
- 5 req/s → 0/10 success, all 429s
- Server enforces strict rate limiting

```bash
python mysterious-passages/puzzle2.py
python mysterious-passages/rate_test_puzzle2.py
```

---

### Puzzle 3 — The Exiled Door

**URL:** `https://bo7.online/the_exiled_door`

**Mechanism:** Geo-IP blocking. The server only allows requests
originating from Mexico (MX). Identified via response header
`request-country-is-mx: False`. Server performs server-side geo-lookup
and ignores all spoofed headers (`X-Forwarded-For`, `X-Real-IP`,
`CF-IPCountry`, etc.).

**Solution:** Route requests through a Mexican HTTPS proxy.
Find fresh MX proxies at (https://free-proxy-list.net)

**Rate test results:**

- Rate tests not written for this puzzle — free Mexican proxies die
  within minutes of being listed. The proxy used to solve the puzzle
  was already dead by the time rate testing could be performed.
- However proof of successful solve is saved in `puzzle3_result.html`

```bash
python mysterious-passages/puzzle3.py
```

---

## Curious Reflections

All three mirror puzzles use **TLS/JA3 fingerprint detection**.
The server identifies the client by its TLS handshake signature
and only allows specific browser fingerprints through.

### Puzzle 1 — The Fractured Mirror

**URL:** `https://bo7.online/the_fractured_mirror`

**Mechanism:** TLS fingerprint check — only accepts Chrome's TLS
fingerprint. Safari fails.

**Solution:** Use Playwright with `channel="chrome"` and
`headless=False` — real Chrome binary with authentic TLS fingerprint.

**Rate test results:**

- 1 req/s → 5/5 success
- 2 req/s → 5/5 success
- 5 req/s → 5/5 success

```bash
python curious-reflections/puzzle1.py
python curious-reflections/rate_test_puzzle1.py
```

---

### Puzzle 2 — The Silver Veil

**URL:** `https://bo7.online/the_silver_veil`

**Mechanism:** TLS fingerprint check — requires Chrome's TLS
fingerprint.

**Solution:** Playwright with real Chrome (`channel="chrome"`),
`headless=True` sufficient.

**Rate test results:**

- 1 req/s → 5/5 success
- 2 req/s → 5/5 success
- 5 req/s → 5/5 success

```bash
python curious-reflections/puzzle2.py
python curious-reflections/rate_test_puzzle2.py
```

---

### Puzzle 3 — The Mirrored Gaze

**URL:** `https://bo7.online/the_mirrored_gaze`

**Mechanism:** TLS fingerprint check — specifically requires Firefox's
TLS fingerprint. Chrome, Safari all fail.
Firefox's unique TLS signature needed.

**Solution:** Use Playwright with Firefox engine (`headless=True`).

**Rate test results:**

- 1 req/s → 5/5 success
- 2 req/s → 5/5 success
- 5 req/s → 5/5 success

```bash
python curious-reflections/puzzle3.py
python curious-reflections/rate_test_puzzle3.py
```

---

## Shattered Thresholds

### Puzzle 1 — The Sleeping Vault

**URL:** `https://bo7.online/the_sleeping_vault`

**Mechanism:** JavaScript execution required. The page renders nothing
meaningful without JS — the door only opens after client-side scripts run.

**Solution:** Use Playwright with Chrome to fully execute JS.

**Rate test results:**

- 1 req/s → 5/5 success
- 2 req/s → 5/5 success
- 5 req/s → 5/5 success

```bash
python shattered-thresholds/puzzle1.py
python shattered-thresholds/rate_test_puzzle1.py
```

---

### Puzzle 2 — The Verity Gate

**URL:** `https://bo7.online/the_verity_gate`

**Mechanism:** JavaScript browser authenticity check via
`the_verity_gate.js`. The script:

1. Reads browser info from a JSON embedded in the page
2. Parses the User-Agent to determine claimed browser/engine
3. Detects the actual JS engine using browser APIs
4. Fails if `navigator.webdriver === true` (automation detected)
5. Fails if claimed engine doesn't match actual engine

**Solution:** Use Playwright WebKit and remove the `webdriver` flag
via `add_init_script` before page load.

**Rate test results:**

- 1 req/s → 5/5 success
- 2 req/s → 5/5 success
- 5 req/s → 5/5 success

```bash
python shattered-thresholds/puzzle2.py
python shattered-thresholds/rate_test_puzzle2.py
```
