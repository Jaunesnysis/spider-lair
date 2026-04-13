from playwright.sync_api import sync_playwright

# Puzzle 2: The Silver Veil
# URL: https://bo7.online/the_silver_veil
#
#  TLS/JA3 fingerprint detection (same as Fractured Mirror)
# Use Playwright with channel="chrome" 

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