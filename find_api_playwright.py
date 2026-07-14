from playwright.sync_api import sync_playwright
import time

def intercept_api():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        def handle_request(route, request):
            if "/api/" in request.url or "graphql" in request.url:
                print(f"API Request: {request.url}")
            route.continue_()

        page.route("**/*", handle_request)
        print("Navigating to DramaBox...")
        page.goto("https://www.dramabox.com/video/41000102839_A-Breath-Away-From-Forever/568203144_Episode-1")
        
        # Wait for some time to allow API calls
        time.sleep(5)
        
        browser.close()

if __name__ == "__main__":
    intercept_api()
