from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

# Configure headless browser
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

try:
    driver.get("https://unstop.com/jobs")
    
    # Wait for jobs to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.job-card"))
    )
    
    # Scroll to trigger lazy-loading (if needed)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    
    # Save final HTML
    with open("unstop_jobs_final.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("HTML saved with job data.")
    
    # Parse jobs from the HTML
    soup = BeautifulSoup(driver.page_source, "html.parser")
    jobs = soup.find_all("div", class_="job-card")
    print(f"Found {len(jobs)} jobs.")
    
except Exception as e:
    print("Error:", e)
finally:
    driver.quit()