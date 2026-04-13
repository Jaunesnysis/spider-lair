from playwright.sync_api import sync_playwright

# Puzzle 2: The Verity Gate
# URL: https://bo7.online/the_verity_gate
#
# JS checks that claimed browser (User-Agent) matches actual
# detected engine, AND checks navigator.webdriver is not true.
# Use WebKit + remove webdriver flag via init script

with sync_playwright() as p:
    browser = p.webkit.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Remove webdriver flag
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    page.goto("https://bo7.online/")
    page.goto("https://bo7.online/the_verity_gate")
    page.wait_for_timeout(3000)

    print(f"Title: {page.title()}")

    if "Opened" in page.title():
        print("SUCCESS: Door is open!")

    with open("shattered-thresholds/puzzle2_result.html", "w") as f:
        f.write(page.content())

    print("Saved!")
    browser.close()