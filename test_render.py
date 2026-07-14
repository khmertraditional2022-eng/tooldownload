from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.reelshort.com/movie/real-or-fake-i-decide-6a13c64994826c1ddf0822ab", wait_until="networkidle")
        
        # Scroll a bit to trigger lazy loading if any
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(3)
        
        html = page.content()
        with open("book_rendered.html", "w", encoding="utf-8") as f:
            f.write(html)
            
        print("Done rendering")
        browser.close()

if __name__ == "__main__":
    run()
