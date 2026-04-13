from playwright.sync_api import sync_playwright
import time

# Rate test for Puzzle 2: The Verity Gate
def run_test(req_per_second, total_requests=5):
    interval = 1.0 / req_per_second
    results = {"success": 0, "failed": 0}

    print(f"\nTesting at {req_per_second} req/s ({total_requests} requests)...")

    for i in range(total_requests):
        start = time.time()
        try:
            with sync_playwright() as p:
                browser = p.webkit.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()
                page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                page.goto("https://bo7.online/")
                page.goto("https://bo7.online/the_verity_gate")
                page.wait_for_timeout(3000)

                if "Opened" in page.title():
                    results["success"] += 1
                    print(f"  Request {i+1}: OK")
                else:
                    results["failed"] += 1
                    print(f"  Request {i+1}: FAILED ({page.title()})")
                browser.close()
        except Exception as e:
            results["failed"] += 1
            print(f"  Request {i+1}: ERROR ({str(e)[:50]})")

        elapsed = time.time() - start
        sleep_time = max(0, interval - elapsed)
        time.sleep(sleep_time)

    print(f"Results: {results['success']}/{total_requests} success, {results['failed']} failed")

for rps in [1, 2, 5]:
    run_test(req_per_second=rps, total_requests=5)