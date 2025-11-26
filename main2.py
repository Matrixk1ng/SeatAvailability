import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


# options = webdriver.ChromeOptions()
options = webdriver.ChromeOptions()
# This is the magic line. It tells UTD you are a regular user on a Windows PC, not a robot.
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome(options=options)
class_num = "4349"

try:
    print("Navigating to Guided Search...")
    driver.get("https://coursebook.utdallas.edu/guidedsearch")

    # 2. DIRECTLY SELECT THE CLASS NUMBER
    # We skip the prefix selection based on your feedback.
    print(f"Selecting Class Number: {class_num}")
    
    # Wait for the dropdown to be present
    cnum_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "combobox_cnum"))
    )
    
    # Select "4349" directly from the list
    select = Select(cnum_element)
    select.select_by_visible_text(class_num)

    search_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    search_button.click()
    input("Press Enter to close browser...")

except Exception as e:
    print(f"An error occurred: {e}")
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support import expected_conditions as EC

# # 1. SETUP: Keep the User-Agent to avoid the "Infinite Loading" / Red Box error
# options = webdriver.ChromeOptions()
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
# options.add_argument('--disable-blink-features=AutomationControlled')

# driver = webdriver.Chrome(options=options)

# # ONLY use the number here, since the dropdown likely only contains numbers (e.g. "4349", not "CS 4349")
# target_class_number = "4349"

# try:
#     print("Navigating to Guided Search...")
#     driver.get("https://coursebook.utdallas.edu/guidedsearch")

#     # 2. DIRECTLY SELECT THE CLASS NUMBER
#     # We skip the prefix selection based on your feedback.
#     print(f"Selecting Class Number: {target_class_number}")
    
#     # Wait for the dropdown to be present
#     cnum_element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "combobox_cnum"))
#     )
    
#     # Select "4349" directly from the list
#     select = Select(cnum_element)
#     select.select_by_visible_text(target_class_number)

#     # 3. CLICK SEARCH
#     # The button in Guided Search is an input of type button/submit
#     print("Clicking Search...")
#     search_btn = driver.find_element(By.XPATH, "//input[@value='Search Classes']")
#     search_btn.click()

#     # 4. GET RESULTS
#     print("Waiting for results table...")
#     WebDriverWait(driver, 15).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, "table.course_list"))
#     )

#     # Print first result to confirm
#     first_row = driver.find_element(By.CSS_SELECTOR, "table.course_list tbody tr")
#     print(f"✅ Success! Found: {first_row.text}")

#     input("Press Enter to close browser...")

# except Exception as e:
#     print(f"An error occurred: {e}")