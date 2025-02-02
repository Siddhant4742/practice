from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
from random import randint

# Function to generate the job search URL
def generate_url(index):
    if index == 1:
        return "https://www.naukri.com/machine-learning-engineer-jobs-in-india"
    else:
        return f"https://www.naukri.com/machine-learning-engineer-jobs-in-india-{index}"

# Function to extract the rating from a job's details
def extract_rating(rating_a):
    if rating_a is None or rating_a.find('span', class_="main-2") is None:
        return "None"
    else:
        return rating_a.find('span', class_="main-2").text

# Function to parse job data from the soup object
def parse_job_data_from_soup(page_jobs):
    print("********PAGE_JOBS***********")
    for job in page_jobs:
        job = BeautifulSoup(str(job), 'html.parser')
        row1 = job.find('div', class_="row1")
        row2 = job.find('div', class_="row2")
        row3 = job.find('div', class_="row3")
        row4 = job.find('div', class_="row4")
        row5 = job.find('div', class_="row5")
        row6 = job.find('div', class_="row6")
        
        job_title = row1.a.text
        company_name = row2.span.a.text
        rating_a = row2.span
        rating = extract_rating(rating_a)
        
        job_details = row3.find('div', class_="job-details")
        ex_wrap = job_details.find('span', class_="exp-wrap").span.span.text
        location = job_details.find('span', class_="loc-wrap ver-line").span.span.text

        min_requirements = row4.span.text

        all_tech_stack = []
        for tech_stack in row5.ul.find_all('li', class_="dot-gt tag-li "):
            tech_stack = tech_stack.text
            all_tech_stack.append(tech_stack)

        print(f"Job Title : {job_title}")
        print(f"Company Name : {company_name}")
        print(f"Rating : {rating}")
        print(f"Experience : {ex_wrap}")
        print(f"Location : {location}")
        print(f"Minimum Requirements : {min_requirements}")
        print(f"All Tech Stack : {all_tech_stack}")
        print("***************END***************")
    print("********PAGE_JOBS END***********")

# Chrome options to run in headless mode (without GUI)
options = Options()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--enable-unsafe-swiftshader")


# Setting up the Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Start scraping from page 1 and go up to page 2
start_page = 1
page_end = 2
for i in range(start_page, page_end):
    print(i)
    url = generate_url(i)
    driver.get(url)
    
    # Sleep to let the page load fully, simulating human behavior
    sleep(randint(5, 10))  # Random sleep for the page to load fully
    
    # Fetch the page source
    page_source = driver.page_source
    # print(page_source)
    
    # Generate the soup to parse
    soup = BeautifulSoup(page_source, 'html.parser')
    page_soup = soup.find_all("div", class_="srp-jobtuple-wrapper")
    
    # Parse the job data from the soup object
    parse_job_data_from_soup(page_soup)

# Close the driver after the job scraping is done
driver.quit()
