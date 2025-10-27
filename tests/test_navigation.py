import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, InvalidSessionIdException


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://flotravel-test.flocash.com/register")
    time.sleep(2)
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def wait(driver):
    return WebDriverWait(driver, 15)


def check_session(driver):
    try:
        driver.current_url
        return True
    except InvalidSessionIdException:
        return False


@pytest.mark.order(1)
def test_company_info(driver, wait):
    if not check_session(driver):
        pytest.fail("Browser session is invalid")
    
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(.,'Register Your Non-IATA Travel Agency')]")))
        print("Registration page loaded")
        company_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Company Information')]")))
        company_tab.click()
        time.sleep(1)
        print("Company Information tab clicked")
        assert company_tab.is_displayed()
        print("Company Information section is accessible")
        
    except Exception as e:
        pytest.fail(f"Company Information test failed: {str(e)}")


@pytest.mark.order(2)
def test_create_account(driver, wait):
    if not check_session(driver):
        pytest.fail("Browser session is invalid")
    
    try:
        create_account_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Create Account')]")))
        create_account_tab.click()
        time.sleep(2)
        print(" Create Account tab clicked")
        assert create_account_tab.is_displayed()
        print("Create Account section is accessible")
        
    except TimeoutException:
        pytest.fail("Could not find or click Create Account tab")
    except Exception as e:
        pytest.fail(f"Create Account test failed: {str(e)}")


@pytest.mark.order(3)
def test_review_submit(driver, wait):
    if not check_session(driver):
        pytest.fail("Browser session is invalid")
    
    try:
        review_tab = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Review & Submit')]")))
        review_tab.click()
        time.sleep(2)
        print("Review & Submit tab clicked")
        assert review_tab.is_displayed()
        print(" Review & Submit section is accessible")
        
    except TimeoutException:
        pytest.fail("Could not find or click Review & Submit tab")
    except Exception as e:
        pytest.fail(f"Review & Submit test failed: {str(e)}")


@pytest.mark.order(4)
def test_required_documents(driver, wait):
    if not check_session(driver):
        pytest.fail("Browser session is invalid")
    
    try:
        required_docs_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Required Documents')]")))
        required_docs_tab.click()
        time.sleep(2)
        print("Required Documents tab clicked")
        
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Trade License')]")))
        print("✓ Required Documents tab loaded successfully")
        
        document_sections = [
            'Trade License',
            'Copy of ID',
            'National ID',
            'Selfie Holding ID',
            'Utility Bill'
        ]
        
        for section in document_sections:
            element = driver.find_element(By.XPATH, f"//*[contains(text(), '{section}')]")
            assert element.is_displayed(), f"{section} is not displayed"
            print(f"  ✓ {section} section visible")
        
    except Exception as e:
        pytest.fail(f"Required Documents test failed: {str(e)}")



@pytest.mark.order(5)
def test_required_field_indicators(driver, wait):
    if not check_session(driver):
        pytest.fail("Browser session is invalid")
    
    try:
        required_docs_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Required Documents')]")))
        required_docs_tab.click()
        time.sleep(1)
        
        required_indicators = driver.find_elements(By.XPATH, "//*[contains(text(), '*')]")
        print(f"Found {len(required_indicators)} required field indicators (*)")
        assert len(required_indicators) > 0, "No required field indicators found"
        
        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(1)
        
        validation_messages = driver.find_elements(By.XPATH, "//*[contains(text(), 'is required')]")
        print(f"Found {len(validation_messages)} validation messages")
        
    except Exception as e:
        pytest.fail(f"Required field indicators test failed: {str(e)}")


@pytest.mark.order(6)
def test_file_size_restrictions(driver, wait):
    if not check_session(driver):
        pytest.fail("Browser session is invalid")
    
    try:
        required_docs_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Required Documents')]")))
        required_docs_tab.click()
        time.sleep(1)
        
        size_restrictions = driver.find_elements(By.XPATH, "//*[contains(text(), 'Max size 1 MB')]")
        print(f"Found {len(size_restrictions)} file size restriction notices")
        assert len(size_restrictions) > 0, "No file size restrictions found"
        
    except Exception as e:
        pytest.fail(f"File size restrictions test failed: {str(e)}")


@pytest.mark.order(7)
def test_allowed_file_formats(driver, wait):
    if not check_session(driver):
        pytest.fail("Browser session is invalid")
    
    try:
        required_docs_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Required Documents')]")))
        required_docs_tab.click()
        time.sleep(1)
        
        format_texts = driver.find_elements(By.XPATH, "//*[contains(text(), 'PNG, JPEG, PDF') or contains(text(), 'PNG, JPEG')]")
        print(f"Found {len(format_texts)} file format requirement texts")
        assert len(format_texts) > 0, "No file format requirements found"
        
    except Exception as e:
        pytest.fail(f"Allowed file formats test failed: {str(e)}")


@pytest.mark.order(9)
def test_tab_navigation_order(driver, wait):
    if not check_session(driver):
        pytest.fail("Browser session is invalid")
    
    try:
        tabs = [
            'Company Information',
            'Required Documents',
            'Create Account',
            'Review & Submit'
        ]
        
        for tab_name in tabs:
            tab = wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{tab_name}')]"))
            )
            tab.click()
            time.sleep(1)
            print(f"Successfully navigated to {tab_name}")
        
        print("All tabs are navigable")
        
    except Exception as e:
        pytest.fail(f"Tab navigation order test failed: {str(e)}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])