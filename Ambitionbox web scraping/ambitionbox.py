from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up WebDriver with options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

try:
    driver.get('https://www.ambitionbox.com/overview/tcs-overview')
    
    # Handle pop-up with better waiting mechanism
    try:
        wait = WebDriverWait(driver, 10)
        
        # Wait for and close initial pop-up (if present)
        close_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class,'close') or contains(@aria-label,'Close')]")
        ))
        close_button.click()
        print("Closed pop-up successfully")
        
    except Exception as e:
        print("No pop-up found or could not close:", str(e))

    # Optional: Add scroll to trigger potential lazy-loaded elements
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)  # Allow time for any dynamic content
    
    # Save page source
    with open('ambitionbox.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)

finally:
    driver.quit()