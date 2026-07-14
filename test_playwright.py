from playwright.sync_api import sync_playwright
import time
import json

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        def handle_response(response):
            try:
                if "json" in response.headers.get("content-type", ""):
                    data = response.json()
                    with open("api_responses.txt", "a", encoding="utf-8") as f:
                        f.write(f"URL: {response.url}\n")
                        f.write(json.dumps(data)[:200] + "\n\n")
            except:
                pass

        page.on("response", handle_response)
        
        print("Navigating to page...")
        page.goto("https://www.reelshort.com/episodes/episode-1-now-i-m-your-ceo-ex-husband-6a3ba36a54aeacec4308eee8-r92hxhq31m", wait_until="networkidle")
        page.wait_for_timeout(5000)
        print("Done")
        browser.close()

if __name__ == "__main__":
    open("api_responses.txt", "w").close()
    run()
