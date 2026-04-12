from playwright.sync_api import sync_playwright

# Puzzle 2: The Silver Veil
# URL: https://bo7.online/the_silver_veil
#
# MECHANISM: TLS/JA3 fingerprint detection (same as Fractured Mirror)
# The server checks the TLS fingerprint of the client.
# SOLUTION: Use Playwright with channel="chrome" (real Chrome TLS fingerprint)
# Works in both headless and non-headless mode.

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel="chrome")
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://bo7.online/")
    page.goto("https://bo7.online/the_silver_veil")
    page.wait_for_timeout(2000)

    print(f"Title: {page.title()}")

    if "Aligned" in page.title():
        print("SUCCESS: Mirror is aligned!")

    with open("curious-reflections/puzzle2_result.html", "w") as f:
        f.write(page.content())

    print("Saved!")
    browser.close()