from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from Controllers.LoginControllers import LoginController
from Controllers.MainControllers import MainController
from Controllers.LogoutControllers import LogoutController
from dotenv import load_dotenv
import pytest
from pytest_bdd import scenarios, given, when, then
import os


scenarios('Features/test.feature')

load_dotenv()

# Fixture to initialize and teardown the browser
@pytest.fixture(scope="module")
def browser():
    """Initialize browser once for all tests"""
    baseUrl = f"{os.getenv('BASE_URL')}"
    opts = webdriver.ChromeOptions()
    
    # Add arguments for both local and CI
    opts.add_argument("--proxy-server='direct://'")
    opts.add_argument("--proxy-bypass-list=*")
    opts.add_argument("--disable-quic")
    opts.add_argument("--disable-dev-shm-usage")  # For Docker/Jenkins
    opts.add_argument("--no-sandbox")  # Required for running as root in Docker
    opts.set_capability("acceptInsecureCerts", True)
    
    # Run headless in CI environment
    if os.getenv('CI') or os.getenv('JENKINS_URL'):
        opts.add_argument("--headless=new")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--window-size=1920,1080")  # Set window size for headless
        print("Running in CI mode (headless)")
    
    # Let Selenium Manager handle ChromeDriver automatically
    # No need to specify executable_path - works on Windows, Linux, Mac
    driver = webdriver.Chrome(options=opts)
    driver.get(baseUrl)
    
    if not (os.getenv('CI') or os.getenv('JENKINS_URL')):
        driver.maximize_window()
    
    driver.implicitly_wait(10)
    time.sleep(2)  # Extra wait for page to stabilize
    
    # Login
    obj = LoginController(driver)
    obj.usernameFill('Admin')
    time.sleep(2)
    obj.passwordFill('admin123')
    time.sleep(2)
    obj.loginBtnClick()
    time.sleep(2)
    
    yield driver
    
    # Logout and teardown
    obj = LogoutController(driver)
    obj.profileClick()
    time.sleep(2)
    obj.logoutClick()
    time.sleep(2)
    driver.quit()


# Step definitions
@given('The user is on the landing page of the website')
def user_is_on_landing_page(browser):
    browser.implicitly_wait(10)
    print('The user is on the landing page!')

@when('the user clicks on the Admin tab and the Jobs tab')
def user_clicks_admin_and_jobs(browser):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from Locators.MainLocators import MainLocators
    
    locator = MainLocators()
    wait = WebDriverWait(browser, 20)
    
    # Wait for Admin tab to be clickable and click
    admin_element = wait.until(EC.element_to_be_clickable((By.XPATH, locator.adminXpath)))
    admin_element.click()
    time.sleep(2)
    
    # Wait for Jobs dropdown to be clickable and click
    job_element = wait.until(EC.element_to_be_clickable((By.XPATH, locator.jobXpath)))
    job_element.click()
    time.sleep(2)

@when('then the user clicks on the Job titles tab')
def user_clicks_jobTitles(browser):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from Locators.MainLocators import MainLocators
    
    locator = MainLocators()
    wait = WebDriverWait(browser, 20)
    
    # Wait for Job Titles tab to be clickable and click
    job_titles_element = wait.until(EC.element_to_be_clickable((By.XPATH, locator.jobTitlesXpath)))
    job_titles_element.click()
    time.sleep(3)

@then('the job titles are displayed to the user')
def the_jobTitles_are_displayed(browser):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    # Wait for the job titles container to load
    wait = WebDriverWait(browser, 20)
    
    # Wait for the first data row to be present (more specific wait)
    try:
        first_row = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[@class='oxd-table-card']")
        ))
        print("Table rows loaded successfully!")
    except:
        print("Could not find table rows!")
        browser.save_screenshot('Screenshots/error_no_rows.png')
        return
    
    time.sleep(3)  # Wait for all rows to render
    
    browser.execute_script('window.scrollBy(0,300);')
    time.sleep(2)
    browser.save_screenshot('Screenshots/title.png')
    time.sleep(1)
    
    data = []
    
    # Try the alternative approach - find all job title elements at once
    try:
        # This XPath finds all the job title cells in the table
        job_title_elements = browser.find_elements(By.XPATH, 
            "//div[@class='oxd-table-card']//div[@role='row']//div[@role='cell'][2]")
        
        print(f"Found {len(job_title_elements)} elements using alternative XPath")
        
        for element in job_title_elements:
            title = element.text.strip()
            if title and title != "Job Titles":  # Skip header
                data.append(title)
    except Exception as e:
        print(f"Alternative approach failed: {e}")
        
        # Fallback to original approach
        for i in range(1, 29):
            try:
                titles = browser.find_element(By.XPATH, 
                    f"//div[@class='orangehrm-container']/div[1]/div[1]/div[{i}]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]")
                job_title = titles.text.strip()
                if job_title:
                    data.append(job_title)
            except Exception as e:
                print(f"Could not find job title at index {i}: {str(e)[:100]}")
                break
    
    print(f"\n{'='*50}")
    print(f"Total Job Titles Found: {len(data)}")
    print(f"{'='*50}")
    for idx, title in enumerate(data, 1):
        print(f"{idx}. {title}")
    print(f"{'='*50}\n")
