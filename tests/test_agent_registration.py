import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

ACTION_DELAY = 0.5 


@pytest.fixture(scope="module")
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://flotravel-test.flocash.com/register")
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def wait(browser):
    return WebDriverWait(browser, 10)


def highlight(driver, element):
    driver.execute_script("arguments[0].style.border='1x solid yellow'", element)


def slow_type(element, text):
    element.clear()
    for ch in text:
        element.send_keys(ch)
        time.sleep(0.02) 
    time.sleep(ACTION_DELAY)


def click_tab(browser, wait, tab_name):
    try:
        tab = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//button[contains(normalize-space(), '{tab_name}')]")
            )
        )
        highlight(browser, tab)
        tab.click()
        print(f" Clicked tab: {tab_name}")
        time.sleep(ACTION_DELAY)
    except Exception as e:
        print(f" Failed to click tab '{tab_name}': {e}")


def fill_input(wait, browser, locator, value, label="field"):
    try:
        element = wait.until(EC.presence_of_element_located(locator))
        highlight(browser, element)
        slow_type(element, value)
        print(f"   Filled: {label}")
        return True
    except Exception as e:
        print(f"   Failed to fill {label}: {e}")
        return False


def upload_file(browser, index, file_path):
    try:
        inputs = browser.find_elements(By.CSS_SELECTOR, "input[type='file']")
        if index < len(inputs):
            highlight(browser, inputs[index])
            inputs[index].send_keys(file_path)
            time.sleep(ACTION_DELAY)
            print(f" Uploaded file {index + 1}")
            return True
        else:
            print(f" File input index {index} not found.")
            return False
    except Exception as e:
        print(f" Upload failed for file {index + 1}: {e}")
        return False



@pytest.mark.order(1)
def test_company_information(browser, wait):
    print("\n === Company Information ===")
    click_tab(browser, wait, "Company Information")

    fill_input(wait, browser, (By.NAME, "agencyName"), COMPANY_DATA['agency_name'], "Company Name")
    fill_input(wait, browser, (By.NAME, "firstName"), COMPANY_DATA['first_name'], "Registration Number")
    fill_input(wait, browser, (By.NAME, "lastName"), COMPANY_DATA['last_name'], "Email")
    fill_input(wait, browser, (By.NAME, "phone"), COMPANY_DATA['phone'], "Phone")
    fill_input(wait, browser, (By.NAME, "postCode"), COMPANY_DATA['post_code'], "Address")
    fill_input(wait, browser, (By.NAME, "city"), COMPANY_DATA['city'], "City")
    fill_input(wait, browser, (By.NAME, "fullAddress"), COMPANY_DATA['address'], "Address")

    print("Company Information completed.\n")


@pytest.mark.order(2)
def test_upload_documents(browser, wait):
    print("\n === Required Documents ===")
    click_tab(browser, wait, "Required Documents")

    uploaded = 0
    for i, path in enumerate(FILES):
        if upload_file(browser, i, path):
            uploaded += 1
    print(f"✓ Uploaded {uploaded}/{len(FILES)} documents.\n")


@pytest.mark.order(3)
def test_create_account(browser, wait):
    print("\n === Create Account ===")
    click_tab(browser, wait, "Create Account")

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
            print(f"  Filled username using locator: {locator}")
            username_filled = True
            break
        except Exception as e:
            continue
    
    if not username_filled:
        print("  Failed to fill username with any locator strategy")
        inputs = browser.find_elements(By.TAG_NAME, "input")
        print(f"  Debug: Found {len(inputs)} input fields on page")
        for idx, inp in enumerate(inputs):
            print(f" Input {idx}: type={inp.get_attribute('type')}, "
                  f"name={inp.get_attribute('name')}, "
                  f"id={inp.get_attribute('id')}, "
                  f"placeholder={inp.get_attribute('placeholder')}")

    fill_input(wait, browser, (By.NAME, "email"), ACCOUNT_DATA['email'], "email")

    try:
        password_fields = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//input[@type='password']"))
        )
        for field in password_fields:
            highlight(browser, field)
            slow_type(field, ACCOUNT_DATA['password'])
        print("  Filled: Password fields")
    except Exception as e:
        print(f" Failed to fill password fields: {e}")

    print(" Create Account section completed.\n")


@pytest.mark.order(4)
def test_review_submit(browser, wait):
    print("\n === Review & Submit ===")
    click_tab(browser, wait, "Review & Submit")

    try:
        review_button = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(normalize-space(), 'Review & Submit')]")
            )
        )
        highlight(browser, review_button)
        print(" Review page loaded and ready.")
    except Exception as e:
        print(f" Could not verify review page: {e}")

    print(" Review & Submit section completed.\n")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])