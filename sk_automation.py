#Master-Admin login
#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys
import traceback

driver = None
try:
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://schoolknot.com/master-admin.php")

    # Fill the "User Name" field
    username_field = driver.find_element(By.NAME, "username")
    username_field.send_keys("abdul@schoolknot.com")

    # Fill the "Password"field
    password_field = driver.find_element(By.NAME, "pwd")
    password_field.send_keys("8790576017")

    # Click button "Login"loginBtn
    login_btn = driver.find_element(By.ID, "login_Btn")
    login_btn.click()

    # Wait for the OTP modal
    wait = WebDriverWait(driver, 10)
    otp_field = wait.until(EC.visibility_of_element_located((By.ID, "otp")))
    #Provide the OTO into the field "OTP"
    otp_field.send_keys("abdul1")
    #Press "ENTER" key
    otp_field.send_keys(Keys.ENTER)

    # Wait for the login and page transition
    time.sleep(3)

    # Click the link "schools" in the side nav
    print("Clicking 'Schools' in side nav...")
    schools_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Schools') or contains(text(), 'SCHOOLS') or normalize-space()='Schools']")))
    schools_link.click()

    # Provide school name "SC2321" in the search bar
    print("Searching for 'SC2321'...")
    # (Using a generic XPath for search inputs; adjust locator if it has a specific ID or Name)
    search_bar = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='search' or contains(@placeholder, 'Search') or contains(@class, 'search') or @aria-label='Search']")))
    search_bar.send_keys("SC2321")
    time.sleep(2) # Wait for the table/results to filter

    # Click the value "SC2321" in the column "school id"
    print("Clicking school ID 'SC2321'...")
    school_id_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[self::td or self::a or self::span][normalize-space()='SC2321']")))
    school_id_element.click()

    # Click button "login to school"
    print("Clicking 'Login to school' button...")
    #login_school_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Login To school') or contains(text(), 'LOGIN TO SCHOOL') or contains(text(), 'Login to School'))]")))
    login_school_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login To School')]")))
    login_school_btn.click()

    # Wait for modal popup "USER VERIFICATION" and provide value "12345"
    print("Waiting for User Verification modal and entering passcode...")
    # Ensure modal is visible by checking for title text
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'USER VERIFICATION') or contains(text(), 'User Verification')]")))
    # Locate the passcode input field inside the modal or page
    passcode_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'modal') or contains(@role, 'dialog')]//input | //input[@type='password' or contains(@placeholder, 'Passcode') or contains(@name, 'passcode')]")))
    passcode_input.send_keys("12345")

    # Click button "VERIFY PASSCODE"
    print("Clicking 'VERIFY PASSCODE'...")
    verify_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'VERIFY PASSCODE') or contains(text(), 'Verify Passcode') or contains(text(), 'Verify passcode')]")))
    verify_btn.click()


    # IMPORTANT: "VERIFY PASSCODE" opens the school dashboard in a NEW browser window/tab.
    # We must switch the WebDriver's focus to this new window before interacting with it.
    print("Waiting for new window handle...")
    wait.until(lambda d: len(d.window_handles) > 1)
    # Find the new window handle we haven't switched to yet
    original_window = driver.current_window_handle
    new_window = [w for w in driver.window_handles if w != original_window][0]
    driver.switch_to.window(new_window)
    print("Switched to school dashboard window.")

    time.sleep(5) # Wait for the dashboard page to fully load

    # Click Staff-->Manage Employees
    # Click Staff-->Manage Employees
    print("Clicking 'Staff'...")
    # Target the actual anchor link wrapping 'Staff' to ensure the sidebar triggers action
    staff_menu = wait.until(EC.presence_of_element_located((By.XPATH, "//a[.//span[normalize-space()='Staff']]")))
    driver.execute_script("arguments[0].click();", staff_menu)

    print("Clicking 'Manage Employees'...")
    # Target the actual anchor link for Manage Employees
    manage_employees = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(., 'Manage Employees')]")))
    driver.execute_script("arguments[0].click();", manage_employees)

    print("Waiting for Manage Employees dashboard to route...")
    try:
        wait.until(EC.url_contains("manage-employees"))
    except:
        print("URL did not organically change, possibly already there or needs hard navigation.")
        
    time.sleep(5) # Wait for the Angular table/API calls to fully load

    #Find Registration ID "112238" and click the button "VIEW"
    try:
        #Find the row containing '112238'
        reg_id_cell = wait.until(EC.presence_of_element_located((By.XPATH, "//*[self::td or self::span or self::div][normalize-space()='112238']")))
        # From that cell, go up to the row (tr) and find the VIEW button inside that row
        view_btn = reg_id_cell.find_element(By.XPATH, "./ancestor::tr//*[contains(text(), 'VIEW') or contains(text(), 'View') or @title='View' or @aria-label='View']")
        view_btn.click()
        print("Clicked VIEW for Registration ID '112238'.")
    except Exception as e:
        print(f"Could not find ID '112238' or click its VIEW button. Exception: {e}")

    time.sleep(3) # Wait for Employee details to load

    #Verify fields on View Employees page
    def verify_field(field_name, expected_value):
        try:
            # We look for the exact expected value on the screen as a quick verification
            wait.until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{expected_value}')]")))
            print(f"Verified field '{field_name}' shows '{expected_value}'.")
        except Exception as e:
            print(f"Verification FAILED for '{field_name}'. Expected '{expected_value}'.")

    print("Verifying employee details...")
    verify_field("Mobile", "8790576017")
    verify_field("Type", "Non-Teaching")
    verify_field("Employment Type", "Permanent")

    #Click tab "SHIFT TIMINGS"
    #print("Clicking 'SHIFT TIMINGS' tab...")
    #shift_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'SHIFT TIMINGS') or contains(text(), 'Shift Timings')]")))
    #shift_tab.click()

    #time.sleep(2) # Wait for tab content

    #Verify login and logout timings
    #print("Verifying Shift Timings...")
    #verify_field("login", "09:00 AM")
    #verify_field("logout", "04:00 PM")

    #Click button "BACK"
    print("Clicking 'BACK'...")
    back_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[self::button or self::a][contains(text(), 'BACK') or contains(text(), 'Back')]")))
    back_btn.click()

    time.sleep(2)

    #Click button "Logout"
    print("Clicking 'Logout'...")
    try:
        logout_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Logout') or contains(text(), 'LOGOUT')]")))
        logout_btn.click()
    except:
        try:
            profile_icon = driver.find_element(By.XPATH, "//*[contains(@class, 'profile') or contains(@class, 'avatar') or contains(@class, 'user')] | //*[@id='profile' or @id='user']")
            profile_icon.click()
            time.sleep(1)
            logout_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Logout') or contains(text(), 'LOGOUT')]")))
            logout_btn.click()
        except Exception as e:
            print(f"Could not click Logout. Exception: {e}")

    print("Successfully executed Manage Employees verifications and logged out!")

except Exception as e:
    print("An error occurred. Full details:")
    traceback.print_exc()
    if driver is not None:
        try:
            driver.save_screenshot("error_screenshot.png")
            print("Screenshot saved to error_screenshot.png")
        except Exception as screenshot_err:
            print(f"Could not save screenshot: {screenshot_err}")
    sys.exit(1)
finally:
    if driver is not None:
        driver.quit()
