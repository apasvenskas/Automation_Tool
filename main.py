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
print(f"Attempting to log in with Username: '{USERNAME}'") # Added quotes for clarity
print(f"Attempting to log in with Password: '{PASSWORD}'") # Added quotes for clarity

if not USERNAME or not PASSWORD:
    print("🔴 Error: Username or Password not found in .env file. Please check your .env configuration.")
    exit()

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

service = Service("chromedriver-win64/chromedriver.exe") # Ensure this path is correct
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the login page
driver.get("https://demoqa.com/login")

try:
    print("Attempting to locate username and password fields...")
    username_field = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "userName"))
    )
    password_field = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "password"))
    )
    print("✅ Username and password fields located.")

    username_field.clear() # Clear the field first
    username_field.send_keys(USERNAME)
    
    password_field.clear() # Clear the field first
    password_field.send_keys(PASSWORD)

    print("✅ Username and password entered using send_keys().")

    # Add a small pause to visually confirm fields are filled before clicking login
    print("Pausing for 2 seconds to allow visual confirmation of credentials...")
    time.sleep(2) 

    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'login'))
    )

    login_button.click()
    print("✅ Login button clicked.")

    print("Waiting for 'Book Store' header to confirm successful login...")
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='main-header' and contains(text(),'Book Store')]"))
    )
    print("✅ Successfully logged in and dashboard loaded.")

    print("Attempting to navigate to 'Elements' section...")
    elements_card = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'card-body')]//h5[text()='Elements']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", elements_card)
    time.sleep(0.5)
    elements_card.click()
    print("✅ Clicked on 'Elements' category.")

    print("Attempting to navigate to 'Forms' section...")
    forms_card = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'card-body')]//h5[text()='Forms']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", forms_card)
    time.sleep(0.5)
    forms_card.click()
    print("✅ Clicked on 'Forms' category card.")

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
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    error_filename = f"error_screenshot_{timestamp}.png"
    try:
        driver.save_screenshot(error_filename)
        print(f"📸 Screenshot saved as {error_filename}")
    except Exception as E2:
        print(f"Could not save screenshot due to: {E2}")


# Keep this input to manually inspect the browser before it closes
input("Press Enter to close the browser...")
driver.quit()
print("Browser closed.")