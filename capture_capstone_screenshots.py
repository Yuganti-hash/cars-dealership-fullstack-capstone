import os
import time
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000"

def save_both(page, filename):
    sub_path = os.path.join("submission", "screenshots", filename)
    root_path = os.path.join("evidence", filename)
    os.makedirs(os.path.dirname(sub_path), exist_ok=True)
    os.makedirs(os.path.dirname(root_path), exist_ok=True)
    page.screenshot(path=sub_path, full_page=False)
    page.screenshot(path=root_path, full_page=False)
    print(f"[CAPTURED SCREENSHOT] {filename}")

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use typical 1280x800 desktop viewport
        context = browser.new_context(viewport={"width": 1280, "height": 850})
        page = context.new_page()

        print("1. Capturing Admin Login (Task 12)...")
        page.goto(f"{BASE_URL}/admin/login/")
        page.wait_for_selector('#id_username', timeout=10000)
        page.fill('#id_username', 'admin')
        page.fill('#id_password', 'adminpassword123')
        page.click('input[type="submit"]')
        page.wait_for_load_state("networkidle")
        save_both(page, "admin_login.png")

        print("2. Capturing Admin Logout (Task 13)...")
        # In Django admin, logout URL
        page.goto(f"{BASE_URL}/admin/logout/")
        page.wait_for_load_state("networkidle")
        save_both(page, "admin_logout.png")

        print("3. Capturing Public Homepage (Task 17)...")
        page.goto(f"{BASE_URL}/")
        page.wait_for_selector(".dealers-table")
        time.sleep(1) # ensure dynamic dealers loaded
        save_both(page, "get_dealers.png")

        print("4. Capturing Kansas Filter (Task 19)...")
        page.select_option("#state-filter", "Kansas")
        time.sleep(1)
        save_both(page, "dealersbystate.png")

        print("5. Capturing Logged-in Homepage (Task 18)...")
        # Reset filter to all
        page.select_option("#state-filter", "all")
        time.sleep(0.5)
        # Click login button
        page.click(".btn-login")
        page.wait_for_selector("#login-username", state="visible")
        page.fill("#login-username", "testuser")
        page.fill("#login-password", "testpassword123")
        page.click("#login-form button[type='submit']")
        time.sleep(1)
        # Verify Review Dealer button and logged in status
        save_both(page, "get_dealers_loggedin.png")

        print("6. Capturing Dealer Reviews (Task 20)...")
        page.goto(f"{BASE_URL}/dealer/1")
        page.wait_for_selector(".review-card")
        time.sleep(1)
        save_both(page, "dealer_id_reviews.png")

        print("7. Capturing Review Form before submission (Task 21)...")
        page.goto(f"{BASE_URL}/postreview/1")
        page.wait_for_selector("#review-content")
        page.fill("#review-content", "Fantastic services and very courteous staff. The sales team made purchasing our SUV seamless and transparent.")
        page.check("#review-purchase")
        time.sleep(0.5)
        # Select Car Make Audi and Q5
        page.select_option("#car-make-select", "Audi")
        time.sleep(0.5)
        page.select_option("#car-model-select", "Q5")
        page.fill("#car-year-input", "2024")
        page.fill("#purchase-date-input", "2026-10-27")
        time.sleep(0.5)
        save_both(page, "dealership_review_submission.png")

        print("8. Capturing Added Review (Task 22)...")
        page.click("#post-review-form button[type='submit']")
        # Wait for redirect to dealer page
        time.sleep(2)
        page.wait_for_selector(".review-card")
        save_both(page, "added_review.png")

        # Capture deployed representation screenshots if requested
        print("9. Generating deployed representation screenshots (Tasks 25-28)...")
        page.goto(f"{BASE_URL}/")
        time.sleep(1)
        save_both(page, "deployed_landingpage.png")

        save_both(page, "deployed_loggedin.png")

        page.goto(f"{BASE_URL}/dealer/1")
        time.sleep(1)
        save_both(page, "deployed_dealer_detail.png")

        save_both(page, "deployed_add_review.png")

        browser.close()
        print("All genuine screenshots captured successfully!")

if __name__ == '__main__':
    run()
