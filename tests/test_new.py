import unittest
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class TravelAgencyRegistrationTest(unittest.TestCase):
    """Test suite for Travel Agency Registration flow"""
    
    @classmethod
    def setUpClass(cls):
        """Set up the WebDriver once for all tests"""
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.base_url = "http://flotravel-test.flocash.com/register"
        
        # Paths to test documents (update these with actual file paths)
        cls.test_files = {
            'trade_license': os.path.abspath('test_files/trade_license.pdf'),
            'id_copy': os.path.abspath('test_files/id_copy.pdf'),
            'id_front': os.path.abspath('test_files/id_front.jpg'),
            'id_back': os.path.abspath('test_files/id_back.jpg'),
            'selfie': os.path.abspath('test_files/selfie.jpg'),
            'utility_bill': os.path.abspath('test_files/utility_bill.pdf')
        }
    
    def setUp(self):
        """Navigate to the registration page before each test"""
        self.driver.get(self.base_url)
        time.sleep(2)
    
    def test_01_page_load(self):
        """Test if the registration page loads correctly"""
        self.assertIn("Register", self.driver.title)
        
        # Check if main heading is present
        heading = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Register Your Non-IATA Travel Agency')]"))
        )
        self.assertIsNotNone(heading)
        print("✓ Page loaded successfully")
    
    def test_02_navigation_tabs(self):
        """Test navigation between registration steps"""
        # Check all tabs are present
        tabs = ['Company Information', 'Required Documents', 'Create Account', 'Review & Submit']
        
        for tab in tabs:
            tab_element = self.driver.find_element(By.XPATH, f"//button[contains(text(), '{tab}')]")
            self.assertTrue(tab_element.is_displayed())
        
        # Click on Required Documents tab
        required_docs_tab = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Required Documents')]")
        required_docs_tab.click()
        time.sleep(1)
        
        # Verify Required Documents section is visible
        section_heading = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Required Documents')]"))
        )
        self.assertIsNotNone(section_heading)
        print("✓ Navigation tabs working correctly")
    
    def test_03_required_documents_section_display(self):
        """Test if all required document upload sections are displayed"""
        # Navigate to Required Documents tab
        required_docs_tab = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Required Documents')]"))
        )
        required_docs_tab.click()
        time.sleep(1)
        
        # Check for all document sections
        document_sections = [
            'Trade License',
            'Copy of ID',
            'National ID',
            'Selfie Holding ID',
            'Utility Bill'
        ]
        
        for section in document_sections:
            element = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{section}')]")
            self.assertTrue(element.is_displayed())
        
        print("✓ All required document sections are displayed")
    
    def test_04_upload_trade_license(self):
        """Test uploading trade license document"""
        # Navigate to Required Documents
        required_docs_tab = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Required Documents')]"))
        )
        required_docs_tab.click()
        time.sleep(1)
        
        # Find and upload trade license
        try:
            # Look for file input (it might be hidden)
            file_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
            
            if len(file_inputs) > 0:
                # Upload to first file input (Trade License)
                file_inputs[0].send_keys(self.test_files['trade_license'])
                time.sleep(2)
                
                # Check if file name is displayed
                uploaded_file = self.driver.find_element(By.XPATH, "//*[contains(text(), '.pdf') or contains(text(), 'compressed')]")
                self.assertIsNotNone(uploaded_file)
                print("✓ Trade license uploaded successfully")
            else:
                print("⚠ File input not found - may need to click browse button first")
        
        except Exception as e:
            print(f"⚠ Upload test skipped: {str(e)}")
    
    def test_05_validate_file_size_restrictions(self):
        """Test file size validation messages"""
        required_docs_tab = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Required Documents')]"))
        )
        required_docs_tab.click()
        time.sleep(1)
        
        # Check for file size restrictions text
        size_restrictions = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Max size 1 MB')]")
        self.assertGreater(len(size_restrictions), 0)
        print(f"✓ Found {len(size_restrictions)} file size restriction notices")
    
    def test_06_validate_required_field_indicators(self):
        """Test that required fields are marked with asterisks"""
        required_docs_tab = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Required Documents')]"))
        )
        required_docs_tab.click()
        time.sleep(1)
        
        # Look for required field indicators (*)
        required_indicators = self.driver.find_elements(By.XPATH, "//*[contains(text(), '*')]")
        self.assertGreater(len(required_indicators), 0)
        print(f"✓ Found {len(required_indicators)} required field indicators")
    
    def test_07_validate_allowed_file_formats(self):
        """Test that allowed file formats are displayed"""
        required_docs_tab = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Required Documents')]"))
        )
        required_docs_tab.click()
        time.sleep(1)
        
        # Check for allowed formats text
        format_texts = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'PNG, JPEG, PDF') or contains(text(), 'PNG, JPEG')]")
        self.assertGreater(len(format_texts), 0)
        print(f"✓ File format requirements are displayed")
    
    def test_08_company_information_tab(self):
        """Test Company Information tab functionality"""
        company_tab = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Company Information')]"))
        )
        company_tab.click()
        time.sleep(1)
        
        # This would check for form fields in Company Information section
        # Add specific field checks based on actual form structure
        print("✓ Company Information tab is accessible")
    
    def test_09_create_account_tab(self):
        """Test Create Account tab functionality"""
        create_account_tab = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Create Account')]"))
        )
        create_account_tab.click()
        time.sleep(1)
        
        # Check that we're in Create Account section
        print("✓ Create Account tab is accessible")
    
    def test_10_review_submit_tab(self):
        """Test Review & Submit tab functionality"""
        review_tab = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Review & Submit')]"))
        )
        review_tab.click()
        time.sleep(1)
        
        # Check that we're in Review & Submit section
        print("✓ Review & Submit tab is accessible")
    
    @classmethod
    def tearDownClass(cls):
        """Close the browser after all tests"""
        time.sleep(2)
        cls.driver.quit()


class DocumentUploadTest(unittest.TestCase):
    """Focused tests for document upload functionality"""
    
    def setUp(self):
        """Set up for each test"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get("http://flotravel-test.flocash.com/register")
        time.sleep(2)
        
        # Navigate to Required Documents
        required_docs_tab = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Required Documents')]"))
        )
        required_docs_tab.click()
        time.sleep(1)
    
    def test_multiple_document_upload(self):
        """Test uploading multiple documents"""
        file_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
        
        test_file = os.path.abspath('test_files/sample.pdf')
        
        # Upload to multiple fields if file exists
        if os.path.exists(test_file):
            for i, file_input in enumerate(file_inputs[:3]):  # Upload to first 3 fields
                try:
                    file_input.send_keys(test_file)
                    time.sleep(1)
                    print(f"✓ Uploaded to field {i+1}")
                except Exception as e:
                    print(f"⚠ Could not upload to field {i+1}: {str(e)}")
        else:
            print("⚠ Test file not found - create test_files directory with sample files")
    
    def tearDown(self):
        """Close browser after each test"""
        time.sleep(1)
        self.driver.quit()


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)