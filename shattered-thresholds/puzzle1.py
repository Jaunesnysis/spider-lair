from playwright.sync_api import sync_playwright

# Puzzle 1: The Sleeping Vault
# URL: https://bo7.online/the_sleeping_vault
#
# equires JavaScript execution to render content
# "shows nothing until you truly look" = needs a real browser to execute JS
# Playwright with real Chrome - JS executes and door opens

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel="chrome")
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://bo7.online/")
    page.goto("https://bo7.online/the_sleeping_vault")
    page.wait_for_timeout(2000)

    print(f"Title: {page.title()}")

    if "Opened" in page.title():
        print("SUCCESS: Door is open!")

    with open("shattered-thresholds/puzzle1_result.html", "w") as f:
        f.write(page.content())

    print("Saved!")
    browser.close()