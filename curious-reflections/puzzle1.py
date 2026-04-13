from playwright.sync_api import sync_playwright

# Puzzle 1: The Fractured Mirror
# URL: https://bo7.online/the_fractured_mirror
#
# TLS/JA3 fingerprint detection
# SOLUTION: Use Playwright with channel="chrome" 

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        channel="chrome",
    )
    context = browser.new_context()
    page = context.new_page()

    # Step 1: visit homepage
    page.goto("https://bo7.online/")

    # Step 2: visit puzzle
    page.goto("https://bo7.online/the_fractured_mirror")
    page.wait_for_timeout(2000)

    print(f"Title: {page.title()}")

    if "Aligned" in page.title():
        print("SUCCESS: Mirror is aligned!")

    with open("curious-reflections/puzzle1_result.html", "w") as f:
        f.write(page.content())

    print("Saved!")
    browser.close()