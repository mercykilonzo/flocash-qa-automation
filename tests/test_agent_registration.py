# ...existing code...
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="module")
def driver():
    """Setup Chrome driver for the module using webdriver-manager."""
    opts = Options()
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    # uncomment the next line to run headless
    # opts.add_argument("--headless=new")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    driver.maximize_window()
    yield driver
    time.sleep(1)
    driver.quit()

@pytest.fixture(scope="module")
def wait(driver):
    return WebDriverWait(driver, 25)

@pytest.mark.order(1)
def test_company_info(driver, wait):
    """Step 1 & 2: Company Information + Required Documents"""
    driver.get("https://flotravel-test.flocash.com/register")

    # Step 1: Company Information
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@placeholder,'Agency Name')]")))
    driver.find_element(By.XPATH, "//input[contains(@placeholder,'Agency Name')]").send_keys("DairyHub Travel")
    driver.find_element(By.XPATH, "//input[contains(@placeholder,'First Name')]").send_keys("Mercy")
    driver.find_element(By.XPATH, "//input[contains(@placeholder,'Last Name')]").send_keys("Mwikali")
    driver.find_element(By.XPATH, "//input[contains(@placeholder,'Phone')]").send_keys("0707000000")
    driver.find_element(By.XPATH, "//input[contains(@placeholder,'Post Code')]").send_keys("00100")
    driver.find_element(By.XPATH, "//input[contains(@placeholder,'City')]").send_keys("Nairobi")
    driver.find_element(By.XPATH, "//input[contains(@placeholder,'Full Address')]").send_keys("Tom Mboya Street")

    # Click Continue to Required Documents
    continue_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Continue to Required Documents')]")))
    driver.execute_script("arguments[0].click();", continue_btn)

    # Step 2: Required Documents
    wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(.,'Required Documents')]")))
    files = driver.find_elements(By.XPATH, "//input[@type='file']")
    for f in files:
        # ensure input is visible/interactable; if hidden, use JS to make it visible or raise informative error
        try:
            f.send_keys("/home/student/Downloads/ID_compressed.pdf")
        except Exception as e:
            raise RuntimeError(f"Failed to upload file to input element: {e}")

    continue_btn2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Continue to Create Account')]")))
    driver.execute_script("arguments[0].click();", continue_btn2)

@pytest.mark.order(2)
def test_create_account(driver, wait):
    """Step 3: Create Account"""
    wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(.,'Create Account')]")))
    driver.find_element(By.XPATH, "//input[contains(@placeholder,'Username')]").send_keys("MercyMwiks")
    driver.find_element(By.XPATH, "//input[contains(@placeholder,'Email')]").send_keys("mwiks@example.com")
    driver.find_element(By.XPATH, "//input[contains(@placeholder,'Password')]").send_keys("@Mwiks2025")
    driver.find_element(By.XPATH, "//input[contains(@placeholder,'Confirm')]").send_keys("@Mwiks2025")

    continue_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Continue to Review & Submit')]")))
    driver.execute_script("arguments[0].click();", continue_btn)

@pytest.mark.order(3)
def test_review_submit(driver, wait):
    """Step 4: Review & Submit"""
    wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(.,'Review & Submit')]")))
    checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox']")))
    driver.execute_script("arguments[0].click();", checkbox)

    submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Submit Registration')]")))
    driver.execute_script("arguments[0].click();", submit_btn)

    # Verify success message or confirmation
    success_msg = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'successfully') or contains(text(),'Thank you')]")))
    assert success_msg.is_displayed(), "Registration submission failed!"
# ...existing code...