from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# ------------------------
# Test Data
# ------------------------
COMPANY_DATA = {
    'agency_name': 'Travel Test Agency Ltd',
    'firstName': 'John',
    'lastName': 'Doe',
    'country_text': 'Kenya (+254)',
    'phone_number': '712345678',
    'full_address': '123 Test Street',
    'city': 'Nairobi'
}

ACCOUNT_DATA = {
    'username': f'testuser_{int(time.time())}',
    'email': f'testuser_{int(time.time())}@example.com',
    'password': 'Test@Password123',
    'confirm_password': 'Test@Password123'
}

FILES = [
    '/home/student/Downloads/ID_compressed.pdf',
    '/home/student/Downloads/ID_compressed-1.pdf',
    '/home/student/Downloads/ID_compressed-2.pdf',
    '/home/student/Downloads/ID_compressed-3.pdf',
    '/home/student/Downloads/ID_compressed-4.pdf',
    '/home/student/Downloads/ID_compressed-5.pdf'
]

SIGNUP_URL = "http://flotravel-test.flocash.com/register"

# ------------------------
# Helper Functions
# ------------------------

def click_tab(driver, tab_label):
    """Click tab by data attribute or visible text, with logging"""
    try:
        # 1️⃣ Try stable data attribute
        tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f"[data-tab*='{tab_label.lower()}']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", tab)
        tab.click()
        print(f"→ Navigated to tab: {tab_label} (via data-tab)")
    except Exception:
        # 2️⃣ Fallback: Try text-based button or span
        tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), '{tab_label}')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", tab)
        tab.click()
        print(f"→ Navigated to tab: {tab_label} (via text)")
    time.sleep(1)

def fill_field(driver, selector, text):
    """Wait for a field to be visible, clear it, and fill it"""
    field = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", field)
    field.clear()
    field.send_keys(text)

def upload_files(driver, files):
    """Upload all required documents"""
    file_inputs = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='file']"))
    )
    for i, file_path in enumerate(files):
        if i < len(file_inputs) and os.path.exists(file_path):
            driver.execute_script("arguments[0].scrollIntoView(true);", file_inputs[i])
            file_inputs[i].send_keys(file_path)
            print(f"→ Uploaded: {os.path.basename(file_path)}")
    time.sleep(1)

# ------------------------
# Main Script
# ------------------------
def main():
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        driver.get(SIGNUP_URL)
        print("Opened signup page")

        # ------------------------
        # Company Information
        # ------------------------
        click_tab(driver, "Company Information")

        fill_field(driver, "input[name='agencyName']", COMPANY_DATA['agency_name'])
        fill_field(driver, "input[name='firstName']", COMPANY_DATA['firstName'])
        fill_field(driver, "input[name='lastName']", COMPANY_DATA['lastName'])

        # Country dropdown (handle select or custom)
        try:
            select_tag = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "countryCode"))
            )
            Select(select_tag).select_by_visible_text(COMPANY_DATA['country_text'])
        except:
            driver.find_element(By.CSS_SELECTOR, ".country-select").click()
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{COMPANY_DATA['country_text']}')]"))
            ).click()

        fill_field(driver, "input[name='phoneNumber']", COMPANY_DATA['phone_number'])
        fill_field(driver, "input[name='fullAddress']", COMPANY_DATA['full_address'])
        fill_field(driver, "input[name='city']", COMPANY_DATA['city'])
        print("✓ Company Information completed")

        # ------------------------
        # Required Documents
        # ------------------------
        click_tab(driver, "Required Documents")
        upload_files(driver, FILES)
        print("✓ Required Documents uploaded")

        # ------------------------
        # Create Account
        # ------------------------
        click_tab(driver, "Create Account")
        fill_field(driver, "input[name='username']", ACCOUNT_DATA['username'])
        fill_field(driver, "input[name='email']", ACCOUNT_DATA['email'])
        fill_field(driver, "input[name='password']", ACCOUNT_DATA['password'])
        fill_field(driver, "input[name='confirmPassword']", ACCOUNT_DATA['confirm_password'])
        print("✓ Create Account completed")

        # ------------------------
        # Review & Submit
        # ------------------------
        click_tab(driver, "Review & Submit")

        submit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        submit_button.click()
        print("✓ Form submitted successfully")

    except Exception as e:
        print(f"⚠️ Script failed at step: {e}")

    finally:
        time.sleep(3)
        driver.quit()


if __name__ == "__main__":
    main()
