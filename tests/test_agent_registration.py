import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ======================================================
#  Test Data
# ======================================================
COMPANY_DATA = {
    'agency_name': 'Travel Test Agency Ltd',
    'first_name': 'John',
    'last_name': 'doe',
    'email': 'testagency@gmail.com',
    'phone': '712345678',
    'post_code': '00100',
    'address': '123 Test Street',
    'city': 'Nairobi'
}

ACCOUNT_DATA = {
    'username': 'mercy',
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


# ======================================================
#  Config
# ======================================================
ACTION_DELAY = 0.5  # seconds delay for human-visible typing


# ======================================================
#  Fixtures
# ======================================================
@pytest.fixture(scope="module")
def browser():
    """Setup browser instance (visible mode)."""
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://flotravel-test.flocash.com/register")
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def wait(browser):
    """Explicit wait object."""
    return WebDriverWait(browser, 10)


# ======================================================
#  Helper Functions
# ======================================================
def highlight(driver, element):
    """Highlight element being interacted with."""
    driver.execute_script("arguments[0].style.border='3px solid yellow'", element)


def slow_type(element, text):
    """Type text slowly for human visibility."""
    element.clear()
    for ch in text:
        element.send_keys(ch)
        time.sleep(0.02)  # small delay per character
    time.sleep(ACTION_DELAY)


def click_tab(browser, wait, tab_name):
    """Click on navigation tab using stable locator."""
    try:
        tab = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//button[contains(normalize-space(), '{tab_name}')]")
            )
        )
        highlight(browser, tab)
        tab.click()
        print(f"  ✓ Clicked tab: {tab_name}")
        time.sleep(ACTION_DELAY)
    except Exception as e:
        print(f"  ✗ Failed to click tab '{tab_name}': {e}")


def fill_input(wait, browser, locator, value, label="field"):
    """Generic stable input filler with highlight + delay."""
    try:
        element = wait.until(EC.presence_of_element_located(locator))
        highlight(browser, element)
        slow_type(element, value)
        print(f"  ✓ Filled: {label}")
        return True
    except Exception as e:
        print(f"  ✗ Failed to fill {label}: {e}")
        return False


def upload_file(browser, index, file_path):
    """Upload file into input[type=file]."""
    try:
        inputs = browser.find_elements(By.CSS_SELECTOR, "input[type='file']")
        if index < len(inputs):
            highlight(browser, inputs[index])
            inputs[index].send_keys(file_path)
            time.sleep(ACTION_DELAY)
            print(f"  ✓ Uploaded file {index + 1}")
            return True
        else:
            print(f"  ⚠ File input index {index} not found.")
            return False
    except Exception as e:
        print(f"  ✗ Upload failed for file {index + 1}: {e}")
        return False


# ======================================================
#  Test Cases
# ======================================================
@pytest.mark.order(1)
def test_company_information(browser, wait):
    """Fill out Company Information section."""
    print("\n🏢 === Company Information ===")
    click_tab(browser, wait, "Company Information")

    fill_input(wait, browser, (By.NAME, "agencyName"), COMPANY_DATA['agency_name'], "Company Name")
    fill_input(wait, browser, (By.NAME, "firstName"), COMPANY_DATA['first_name'], "Registration Number")
    fill_input(wait, browser, (By.NAME, "lastName"), COMPANY_DATA['last_name'], "Email")
    fill_input(wait, browser, (By.NAME, "phone"), COMPANY_DATA['phone'], "Phone")
    fill_input(wait, browser, (By.NAME, "postCode"), COMPANY_DATA['post_code'], "Address")
    fill_input(wait, browser, (By.NAME, "city"), COMPANY_DATA['city'], "City")
    fill_input(wait, browser, (By.NAME, "fullAddress"), COMPANY_DATA['address'], "Address")


    print("✓ Company Information completed.\n")


@pytest.mark.order(2)
def test_upload_documents(browser, wait):
    """Upload all required documents."""
    print("\n📄 === Required Documents ===")
    click_tab(browser, wait, "Required Documents")

    uploaded = 0
    for i, path in enumerate(FILES):
        if upload_file(browser, i, path):
            uploaded += 1
    print(f"✓ Uploaded {uploaded}/{len(FILES)} documents.\n")


@pytest.mark.order(3)
def test_create_account(browser, wait):
    """Fill Create Account section."""
    print("\n === Create Account ===")
    click_tab(browser, wait, "Create Account")

    # Try multiple locator strategies for username field
    username_locators = [
        (By.NAME, "username"),
        (By.ID, "username"),
        (By.XPATH, "//input[@placeholder='Username' or @placeholder='username']"),
        (By.XPATH, "//label[contains(text(), 'Username')]/following::input[1]"),
        (By.CSS_SELECTOR, "input[name*='user']"),
    ]
    
    username_filled = False
    for locator in username_locators:
        try:
            element = wait.until(EC.presence_of_element_located(locator))
            highlight(browser, element)
            slow_type(element, ACCOUNT_DATA['username'])
            print(f"  ✓ Filled username using locator: {locator}")
            username_filled = True
            break
        except Exception as e:
            continue
    
    if not username_filled:
        print("  ✗ Failed to fill username with any locator strategy")
        # Print all input fields for debugging
        inputs = browser.find_elements(By.TAG_NAME, "input")
        print(f"  Debug: Found {len(inputs)} input fields on page")
        for idx, inp in enumerate(inputs):
            print(f"    Input {idx}: type={inp.get_attribute('type')}, "
                  f"name={inp.get_attribute('name')}, "
                  f"id={inp.get_attribute('id')}, "
                  f"placeholder={inp.get_attribute('placeholder')}")

    # Fill email
    fill_input(wait, browser, (By.NAME, "email"), ACCOUNT_DATA['email'], "email")

    # Password fields
    try:
        password_fields = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//input[@type='password']"))
        )
        for field in password_fields:
            highlight(browser, field)
            slow_type(field, ACCOUNT_DATA['password'])
        print("  ✓ Filled: Password fields")
    except Exception as e:
        print(f"  ✗ Failed to fill password fields: {e}")

    print("✓ Create Account section completed.\n")


@pytest.mark.order(4)
def test_review_submit(browser, wait):
    """Navigate to Review & Submit section."""
    print("\n📝 === Review & Submit ===")
    click_tab(browser, wait, "Review & Submit")

    try:
        review_button = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(normalize-space(), 'Review & Submit')]")
            )
        )
        highlight(browser, review_button)
        print("✓ Review page loaded and ready.")
    except Exception as e:
        print(f"⚠ Could not verify review page: {e}")

    print("✓ Review & Submit section completed.\n")


# ======================================================
#  Entry Point
# ======================================================
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
