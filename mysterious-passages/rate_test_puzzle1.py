import requests
import time
import threading

# Rate test for Puzzle 1: The Door of Echoed Steps
# Tests scraper resilience at different requests per second

url = "https://bo7.online/the_door_of_echoed_steps"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://bo7.online/",
}

def run_test(req_per_second, total_requests=10):
    interval = 1.0 / req_per_second
    results = {"success": 0, "failed": 0}

    print(f"\nTesting at {req_per_second} req/s ({total_requests} requests)...")

    for i in range(total_requests):
        start = time.time()
        try:
            session = requests.Session()
            session.get("https://bo7.online/", headers=headers)
            response = session.get(url, headers=headers)
            if response.status_code == 200:
                results["success"] += 1
            else:
                results["failed"] += 1
                print(f"  Request {i+1}: FAILED ({response.status_code})")
        except Exception as e:
            results["failed"] += 1
            print(f"  Request {i+1}: ERROR ({str(e)[:50]})")

        elapsed = time.time() - start
        sleep_time = max(0, interval - elapsed)
        time.sleep(sleep_time)

    print(f"Results: {results['success']}/{total_requests} success, {results['failed']} failed")
    return results

for rps in [1, 2, 5]:
    run_test(req_per_second=rps, total_requests=10)