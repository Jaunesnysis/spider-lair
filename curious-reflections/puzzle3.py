from playwright.sync_api import sync_playwright

# Puzzle 3: The Mirrored Gaze
# URL: https://bo7.online/the_mirrored_gaze
#
# MECHANISM: TLS/JA3 fingerprint detection - specifically requires Firefox
# "The right eyes" = Firefox's unique TLS fingerprint
# Chrome, Safari, Python requests all fail - only Firefox passes
# SOLUTION: Use Playwright with Firefox engine

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://bo7.online/")
    page.goto("https://bo7.online/the_mirrored_gaze")
    page.wait_for_timeout(2000)

    print(f"Title: {page.title()}")

    if "Aligned" in page.title():
        print("SUCCESS: Mirror is aligned!")

    with open("curious-reflections/puzzle3_result.html", "w") as f:
        f.write(page.content())

    print("Saved!")
    browser.close()