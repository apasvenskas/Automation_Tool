from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from dotenv import load_dotenv
import os

load_dotenv()
USERNAME = os.getenv("DEMOQA_USERNAME")
PASSWORD = os.getenv("DEMOQA_PASSWORD")

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Set path to your chromedriver executable
service = Service("chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the login page
driver.get("https://demoqa.com/login")

try:
    username_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "userName"))
    )
    password_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "password"))
    )

    driver.execute_script(f"arguments[0].value = '{USERNAME}';", username_field)
    driver.execute_script(f"arguments[0].value = '{PASSWORD}';", password_field)

    time.sleep(5)

except Exception as e:
    print("Error:", e)

input("Press Enter to close the browser...")
driver.quit()
