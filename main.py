import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(options=options)
UTD_NETID=""
UTD_PASSWORD=""

try:
    print("Navigating to Galaxy...")
    driver.get("https://www.utdallas.edu/galaxy/")

    orion_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Orion"))
    )
    orion_link.click()
    print("Clicking on Orion link...")
    print("-------------------------------------------------")
    print("Script paused. Please manually enter your NetID, Password, and approve Duo 2FA.")
    print("Once you are fully logged in and see the Student Center/Tiles, press ENTER here to continue.")
    print("-------------------------------------------------")
    username_input = driver.find_element(By.ID, "netid")   
    password_input = driver.find_element(By.ID, "password")   
    print("Looking for 'Manage My Classes' tile...")
    username_input.clear()
    username_input.send_keys(UTD_NETID)

    password_input.clear()
    password_input.send_keys(UTD_PASSWORD)
    password_input.send_keys(Keys.RETURN)  
    time.sleep(15)
    manage_classes_tile = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Manage My Classes')]"))
    )
    manage_classes_tile.click()

    print("Looking for 'Schedule Planner' link...")
    # This is often in the sidebar
    schedule_planner_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="PTGP_STEP_DVW_PTGP_STEP_LABEL$2"]'))
    )

    schedule_planner_link.click()

    launch_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="PRJCS_DERIVED_PRJCS_LAUNCH_CS"]'))
    )
    launch_button.click()

    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2)) # Wait for new window to open
    original_window = driver.current_window_handle
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break

    print(f"Switched to new window: {driver.title}")
    class_options = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@aria-label, 'Options for CS 3162')]"))
    )
    class_options.click()
    print("Success! Options clicked.")
    time.sleep(2)  # Wait for the options to load
    #instructor_name = "John Cole"
    open_classes = driver.find_element(By.XPATH, "//span[contains(@class,'css-1np60a3-highlightCss')]")
    
    print(f"Seats Open: {open_classes.text}")
    input("Press Enter to close browser...")
# //a[contains(@aria-label,'Options for CS 3162 - PROF RESPONSIBILITY IN CS & SE')]
# //*[@id="scheduler-app"]/div/div[1]/div/div/div[2]/div[1]/div/div[2]/table/tbody[1]/tr[1]/td[3]/div/div/div[1]/a/span[3]
# //*[@id="scheduler-app"]/div/div[1]/div/div/div[2]/div[1]/div/div[2]/table/tbody[2]/tr[1]/td[3]/div/div/div[1]/a/span[3]
# //*[@id="scheduler-app"]/div/div[1]/div/div/div[2]/div[1]/div/div[2]/table/tbody[3]/tr[1]/td[3]/div/div/div[1]/a/span[3]
except Exception as e:
    print(f"An error occurred: {e}")
    
# //button[contains(@aria-label,'Hide Section Details for CS - PROF RESPONSIBILITY IN CS & SE #23868')]//span[contains(@class,'css-1lg9h8p-iconCss')]
# //button[contains(@aria-label,'Show Section Details for CS - OPERATING SYSTEMS CONCEPTS #27964')]//span[contains(@class,'css-1lg9h8p-iconCss')]
