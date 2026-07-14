from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print("Loading page...")
        page.goto("https://www.reelshort.com/episodes/episode-1-now-i-m-your-ceo-ex-husband-6a3ba36a54aeacec4308eee8-r92hxhq31m")
        page.wait_for_selector("a[href*='/episodes/']")
        links = page.eval_on_selector_all("a[href*='/episodes/']", "elements => elements.map(e => e.href)")
        print(f"Found {len(links)} episode links in DOM:")
        for link in set(links):
            print(link)
        browser.close()

if __name__ == "__main__":
    run()
