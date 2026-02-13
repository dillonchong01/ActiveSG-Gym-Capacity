from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://huggingface.co/spaces/dillonchong01/gym_chatbot")

    try:
        # Playwright auto-waits
        restart_button = page.locator("button:has-text('Restart this Space')")

        if restart_button.is_visible():
            restart_button.click()
            print("Restart button clicked.")
            time.sleep(60)

    except:
        print("Restart button not found.")

    browser.close()
