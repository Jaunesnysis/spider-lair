import requests

# Puzzle 3: The Exiled Door
# URL: https://bo7.online/the_exiled_door
#
# MECHANISM: Geo-IP blocking — server only allows requests from Mexico (MX)
# DISCOVERY: Response header revealed "request-country-is-mx: False"
#
# ATTEMPTS MADE:
# 1. Spoofed headers (X-Forwarded-For, X-Real-IP, CF-IPCountry, X-Country-Code etc) — FAILED
#    Server ignores all geo headers and checks real connecting IP
# 2. Tested Mexican public proxies — FAILED (all dead/timeout)
# 3. Checked informational pages (Simple Relic, Crystal JA3 Cave) for hints — no bypass found
#
# CONCLUSION: Requires a real Mexican IP address (paid VPN/proxy with MX exit node)
# The server uses server-side geo-lookup and trusts no client-sent headers.

url = "https://bo7.online/the_exiled_door"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-MX,es;q=0.9",
    "Referer": "https://bo7.online/",
}

session = requests.Session()
session.get("https://bo7.online/", headers=headers)
response = session.get(url, headers=headers)

print(f"Status: {response.status_code}")
print(f"MX header: {response.headers.get('request-country-is-mx')}")

# Save whatever response we get
with open("mysterious-passages/puzzle3_result.html", "w") as f:
    f.write(response.text)