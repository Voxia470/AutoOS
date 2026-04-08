from playwright.sync_api import sync_playwright
import time

def run_browser():
    with sync_playwright() as p:
        # Browser kholna (headless=False ka matlab hai humein dikhega kya ho raha hai)
        browser = p.chromium.launch(headless = False) 
        page = browser.new_page()
        
        print("--- Browser Khul Raha Hai... ---")
        page.goto("https://www.google.com")
        
        print(f"Page Title: {page.title()}")
        
        # 5 second wait taake tum dekh sako
        time.sleep(5)
        browser.close()
        print("--- Browser Band Ho Gaya. Test Success! ---")

if __name__ == "__main__":
    run_browser()