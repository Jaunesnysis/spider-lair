import requests

url = "https://bo7.online/the_exiled_door"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-MX,es;q=0.9",
    "Referer": "https://bo7.online/",
}

mexican_proxies = [
    "201.159.97.25:8081",
]

for proxy_addr in mexican_proxies:
    try:
        print(f"Trying {proxy_addr}...")
        proxies = {
            "http": f"http://{proxy_addr}",
            "https": f"http://{proxy_addr}",
        }
        session = requests.Session()
        session.get("https://bo7.online/", headers=headers, proxies=proxies, timeout=10)
        response = session.get(url, headers=headers, proxies=proxies, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"MX: {response.headers.get('request-country-is-mx')}")
        if response.status_code == 200:
            print("SUCCESS!")
            with open("mysterious-passages/puzzle3_result.html", "w") as f:
                f.write(response.text)
            break
    except Exception as e:
        print(f"FAILED: {str(e)[:80]}\n")
        continue

print("Done.")