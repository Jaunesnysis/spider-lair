import requests

# Puzzle 2: The Clockwork Door
# The clue hinted at timing/rate limiting, but the door opened with
# the same session cookie approach as puzzle 1.
# Solution: visit homepage first to get the wormhole_token cookie,
# then request the puzzle page within the same session.

url = "https://bo7.online/the_clockwork_door"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://bo7.online/",
}

session = requests.Session()
session.get("https://bo7.online/", headers=headers)

response = session.get(url, headers=headers)

print(f"Status: {response.status_code}")
print(f"Cookies: {dict(session.cookies)}")

if response.status_code == 200:
    print("SUCCESS: Door is open!")

with open("mysterious-passages/puzzle2_result.html", "w") as f:
    f.write(response.text)

print("Result saved to puzzle2_result.html")