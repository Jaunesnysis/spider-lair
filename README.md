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
│ └── _\_result.html # Proof of success
├── curious-reflections/
│ ├── puzzle1.py # The Fractured Mirror
│ ├── puzzle2.py # The Silver Veil
│ ├── puzzle3.py # The Mirrored Gaze
│ └── _\_result.html
├── shattered-thresholds/
│ ├── puzzle1.py # The Sleeping Vault
│ ├── puzzle2.py # The Verity Gate
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
cookie (`wormhole_token=galactic-cookie-42`) on the homepage. The puzzle
page requires this cookie to be present.

**Solution:** Use a `requests.Session` to visit the homepage first,
which automatically carries the cookie to subsequent requests.

```bash
python mysterious-passages/puzzle1.py
```

---

### Puzzle 2 — The Clockwork Door

**URL:** `https://bo7.online/the_clockwork_door`

**Mechanism:** Same cookie-based authentication as Puzzle 1.

**Solution:** Same session cookie approach — visit homepage first.

```bash
python mysterious-passages/puzzle2.py
```

---

### Puzzle 3 — The Exiled Door

**URL:** `https://bo7.online/the_exiled_door`

**Mechanism:** Geo-IP blocking. The server only allows requests
originating from Mexico (MX). This was identified via the response
header `request-country-is-mx: False`.

**Attempts made:**

- Spoofed headers (`X-Forwarded-For`, `X-Real-IP`, `CF-IPCountry`, etc.) — server ignores all
- Mexican public proxies — all dead or too slow for HTTPS
- curl (different JA3) — still blocked
- Checked informational pages for hints — no bypass found

**Conclusion:** Requires a real Mexican IP address (paid VPN/proxy
with MX exit node). The server performs server-side geo-lookup and
trusts no client-sent headers.

**Status:** ⚠️ Unsolved — requires paid Mexican VPN/proxy

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

**Mechanism:** TLS fingerprint check — only accepts Chrome's TLS fingerprint.
Python `requests`, curl, headless Chromium, and Safari all fail.

**Solution:** Use Playwright with `channel="chrome"` which uses the
real Chrome binary and its authentic TLS fingerprint.

```bash
python curious-reflections/puzzle1.py
```

---

### Puzzle 2 — The Silver Veil

**URL:** `https://bo7.online/the_silver_veil`

**Mechanism:** Same TLS fingerprint check as Puzzle 1 — requires Chrome.

**Solution:** Same approach — Playwright with real Chrome.

```bash
python curious-reflections/puzzle2.py
```

---

### Puzzle 3 — The Mirrored Gaze

**URL:** `https://bo7.online/the_mirrored_gaze`

**Mechanism:** TLS fingerprint check — specifically requires Firefox's
TLS fingerprint. Chrome, Safari, and Python all fail.
"The right eyes" = Firefox's unique TLS signature.

**Solution:** Use Playwright with Firefox engine.

```bash
python curious-reflections/puzzle3.py
```

---

## Shattered Thresholds

### Puzzle 1 — The Sleeping Vault

**URL:** `https://bo7.online/the_sleeping_vault`

**Mechanism:** JavaScript execution required. The page renders
nothing meaningful without JS — the door only opens after
client-side scripts run.

**Solution:** Use Playwright with Chrome to fully execute JS.

```bash
python shattered-thresholds/puzzle1.py
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

```bash
python shattered-thresholds/puzzle2.py
```

---

## Key Takeaways

| Technique                           | Puzzles                   |
| ----------------------------------- | ------------------------- |
| Session cookies                     | Mysterious Passages 1 & 2 |
| Geo-IP blocking                     | Mysterious Passages 3     |
| TLS/JA3 fingerprinting              | All Curious Reflections   |
| JS execution required               | Shattered Thresholds 1    |
| JS bot detection (`webdriver` flag) | Shattered Thresholds 2    |

## Tools Used

- `requests` — simple HTTP client with session support
- `playwright` — browser automation (Chrome, Firefox, WebKit)
- `curl_cffi` — TLS fingerprint impersonation (tested, insufficient)
- `beautifulsoup4` — HTML parsing
