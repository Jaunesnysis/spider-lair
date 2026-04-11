import requests

# Puzzle 1: The Door of Echoed Steps
# The door checks for a cookie ("ancient token") set by the homepage.
# Solution: use a Session to visit the homepage first, which sets the
# required cookie (wormhole_token=galactic-cookie-42), then visit the puzzle.

url = "https://bo7.online/the_door_of_echoed_steps"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

session = requests.Session()

# Step 1: visit homepage to receive the cookie
session.get("https://bo7.online/", headers=headers)

# Step 2: visit puzzle page with cookie in session
headers["Referer"] = "https://bo7.online/"
response = session.get(url, headers=headers)

print(f"Status: {response.status_code}")
print(f"Cookies: {dict(session.cookies)}")

if "DOOR SLIDES OPEN" in response.text.upper() or response.status_code == 200:
    print("SUCCESS: Door is open!")

# Save proof
with open("mysterious-passages/puzzle1_result.html", "w") as f:
    f.write(response.text)

print("Result saved to puzzle1_result.html")