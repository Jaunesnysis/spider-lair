# import requests

# # Puzzle 2: The Clockwork Door
# # The clue hinted at timing/rate limiting, but the door opened with
# # the same session cookie approach as puzzle 1.
# # visit homepage first to get the wormhole_token cookie,
# # then request the puzzle page within the same session.

# url = "https://bo7.online/the_clockwork_door"

# headers = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#     "Accept-Language": "en-US,en;q=0.5",
#     "Referer": "https://bo7.online/",
# }

# session = requests.Session()
# session.get("https://bo7.online/", headers=headers)

# response = session.get(url, headers=headers)

# print(f"Status: {response.status_code}")
# print(f"Cookies: {dict(session.cookies)}")

# if response.status_code == 200:
#     print("SUCCESS: Door is open!")

# with open("mysterious-passages/puzzle2_result.html", "w") as f:
#     f.write(response.text)

# print("Result saved to puzzle2_result.html")


#above is the initial solution that worked, but the server seems to have some rate limiting in place that blocks after a few requests. Below is an updated version that handles rate limiting by waiting and retrying. 
import requests
import time

url = "https://bo7.online/the_clockwork_door"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://bo7.online/",
}

def try_door(wait_between=15, max_attempts=3):
    session = requests.Session()
    session.get("https://bo7.online/", headers=headers)

    for attempt in range(1, max_attempts + 1):
        print(f"\nAttempt {attempt}...")
        response = session.get(url, headers=headers)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            print("SUCCESS: Door is open!")
            with open("mysterious-passages/puzzle2_result.html", "w") as f:
                f.write(response.text)
            print("Saved to puzzle2_result.html")
            return True

        elif response.status_code == 429:
            # Check if server tells us how long to wait
            retry_after = response.headers.get("Retry-After")
            x_reset = response.headers.get("X-RateLimit-Reset")
            print(f"Rate limited. Headers: {dict(response.headers)}")

            if retry_after:
                wait = int(retry_after)
                print(f"Server says wait {wait}s...")
            elif x_reset:
                wait = max(0, int(x_reset) - int(time.time()))
                print(f"Reset in {wait}s...")
            else:
                wait = wait_between
                print(f"No hint from server, waiting {wait}s...")

            time.sleep(wait)

        else:
            print(f"Unexpected status: {response.status_code}")
            break

    print("Max attempts reached.")
    return False

print("Waiting 2 minutes to clear any existing rate limit block...")
time.sleep(120)

try_door(wait_between=30, max_attempts=3)