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

# For debugging .env load
print(f"Attempting to log in with Username: {USERNAME}")
if not USERNAME or not PASSWORD:
    print("🔴 Error: Username or Password not found in .env file. Please check your .env configuration.")
    exit()

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

service = Service("chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the login page
driver.get("https://demoqa.com/login")

try:
    print("Attempting to locate username and password fields...")
    username_field = WebDriverWait(driver, 20).until( # Increased wait time
        EC.visibility_of_element_located((By.ID, "userName"))
    )
    password_field = WebDriverWait(driver, 20).until( # Increased wait time
        EC.visibility_of_element_located((By.ID, "password"))
    )
    print("✅ Username and password fields located.")

    driver.execute_script(f"arguments[0].value = '{USERNAME}';", username_field)
    driver.execute_script(f"arguments[0].value = '{PASSWORD}';", password_field)
    print("✅ Username and password entered.")

    login_button = WebDriverWait(driver, 20).until( # Wait for login button to be clickable
        EC.element_to_be_clickable((By.ID, 'login'))
    )
    login_button.click()
    print("✅ Login button clicked.")

   
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='main-header' and contains(text(),'Book Store')]"))
    )
    print("✅ Successfully logged in and dashboard loaded.")


    print("Attempting to navigate to 'Elements' section...")
   
    elements_card = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'card-body')]//h5[text()='Elements']"))
    )
    # Scroll into view if necessary
    driver.execute_script("arguments[0].scrollIntoView(true);", elements_card)
    time.sleep(0.5) # Brief pause after scroll
    elements_card.click()
    print("✅ Clicked on 'Elements' category.")

    # If "Forms" is a separate main category card similar to "Elements":
    print("Attempting to navigate to 'Forms' section...")
    forms_card = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'card-body')]//h5[text()='Forms']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", forms_card)
    time.sleep(0.5) # Brief pause after scroll
    forms_card.click() # Click the "Forms" category card
    print("✅ Clicked on 'Forms' category card.")

    # Then click on "Practice Form" under "Forms"
    practice_form_menu_item = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Practice Form']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", practice_form_menu_item)
    time.sleep(0.5)
    practice_form_menu_item.click()
    print("✅ Clicked on 'Practice Form' under Forms.")


    print("✨ Actions completed. Pausing for 5 seconds.")
    time.sleep(5)

except Exception as e:
    print(f"🔴 An error occurred: {e}")
    # Optional: Save a screenshot on error
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    driver.save_screenshot(f"error_screenshot_{timestamp}.png")
    print(f"📸 Screenshot saved as error_screenshot_{timestamp}.png")


input("Press Enter to close the browser...")
driver.quit()
print("Browser closed.")