# import time
# import winsound  # For audio alerts on Windows
# from datetime import datetime
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import Select


# # options = webdriver.ChromeOptions()
# options = webdriver.ChromeOptions()
# # This is the magic line. It tells UTD you are a regular user on a Windows PC, not a robot.
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
# options.add_argument('--disable-blink-features=AutomationControlled')

# driver = webdriver.Chrome(options=options)
# class_num = "4349"
# CHECK_INTERVAL_MINUTES = 10  # How often to check
TARGET_PROFESSOR = "Serdar Erbatur"
# TARGET_CLASS_NUM = "4349"
# TARGET_PREFIX = "CS"

# try:
#     print("Navigating to Guided Search...")
#     driver.get("https://coursebook.utdallas.edu/guidedsearch")
#     # 1. DIRECTLY SELECT THE CLASS NUMBER
#     print(f"Selecting Class Number: {class_num}")
    
#     # Wait for the dropdown to be present
#     cp_element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "combobox_cp"))
#     )
    
#     # Select "4349" directly from the list
#     select = Select(cp_element)
#     select.select_by_visible_text("CS - Computer Science")

#     # 2. DIRECTLY SELECT THE CLASS NUMBER
#     # We skip the prefix selection based on your feedback.
#     print(f"Selecting Class Number: {class_num}")
    
#     # Wait for the dropdown to be present
#     cnum_element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "combobox_cnum"))
#     )
    
#     # Select "4349" directly from the list
#     select = Select(cnum_element)
#     select.select_by_visible_text(class_num)
#     time.sleep(5)
#     search_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Search Classes')]")
#     search_button.click()
#     prof_link = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{TARGET_PROFESSOR}')]"))
#     )

#     # 5. Get the Parent Row (TR)
#     # We found the name, now we go UP to the row so we can click it.
#     prof_row = prof_link.find_element(By.XPATH, "./ancestor::tr")
            
#     # Scroll to it and click
#     driver.execute_script("arguments[0].scrollIntoView();", prof_row)
#     try:
#         prof_row.click()
#     except:
#         # Fallback: sometimes clicking the row doesn't work, but clicking the link does
#         prof_link.click()

    
#     input("Press Enter to close browser...")

# except Exception as e:
#     print(f"An error occurred: {e}")
import time
import winsound  # Windows only
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURATION ---
CHECK_INTERVAL_MINUTES = 10
CLASS_SEARCH_TERM = "CS 4349"

# Add as many names as you want here. They must match the CourseBook text exactly.
TARGET_PROFESSORS = [
    "Serdar Erbatur",
    "Parisa Darbari", 
    "Ding Du"
]

# --- SETUP ---
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome(options=options)

def check_professor(prof_name):
    """
    Returns True if seats are found, False if full, None if error/not found.
    """
    try:
        # 1. Navigate & Search (Clean slate)
        driver.get("https://coursebook.utdallas.edu/search")
        
        input_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='srch']"))
        )
        input_box.clear()
        input_box.send_keys(CLASS_SEARCH_TERM)
        time.sleep(1) # Pause for stability

        # Click Search
        driver.find_element(By.XPATH, "//button[contains(text(), 'Search Classes')]").click()

        # 2. Find Professor Specific Link
        # We wait up to 5 seconds. If not found, we assume this prof isn't teaching this term or filter is wrong.
        try:
            prof_link = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{prof_name}')]"))
            )
        except:
            print(f"      [!] Could not find row for {prof_name}")
            return None

        # 3. Expand Row
        prof_row = prof_link.find_element(By.XPATH, "./ancestor::tr")
        driver.execute_script("arguments[0].scrollIntoView();", prof_row)
        try:
            prof_row.click()
        except:
            prof_link.click()

        # 4. Extract Data
        # Wait for the "Available Seats" text to appear
        seat_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(., 'Available Seats:')]"))
        )
        
        full_text = seat_element.text
        # Parsing: "Enrollment Status... Available Seats: 0 Enrolled..."
        text_after_label = full_text.split("Available Seats:")[1]
        seats_str = text_after_label.split("Enrolled")[0].strip()
        seats_count = int(seats_str)
        
        return seats_count

    except Exception as e:
        print(f"      [!] Error checking {prof_name}: {e}")
        return None

# --- MAIN LOOP ---
print(f"--- Monitoring {len(TARGET_PROFESSORS)} Professors for {CLASS_SEARCH_TERM} ---")
print("Press Ctrl+C to stop.\n")

try:
    while True:
        timestamp = datetime.now().strftime("%I:%M %p")
        print(f"[{timestamp}] Starting cycle...")
        
        found_any = False

        for prof in TARGET_PROFESSORS:
            print(f"   > Checking {prof}...")
            seats = check_professor(prof)
            
            if seats is not None:
                if seats > 0:
                    print(f"      ✅ OPEN! {seats} seats available.")
                    found_any = True
                else:
                    print(f"      ❌ Full (0 seats).")
            
            # Small pause between professors to be gentle on the browser
            time.sleep(2)

        # Alert Logic
        if found_any:
            print("\n🎉🎉🎉 SEATS FOUND! GO REGISTER! 🎉🎉🎉")
            try:
                # 5 Long Beeps
                for _ in range(5):
                    winsound.Beep(1000, 1000)
            except:
                pass
        
        print(f"   > Cycle complete. Sleeping {CHECK_INTERVAL_MINUTES} minutes...")
        time.sleep(CHECK_INTERVAL_MINUTES * 60)

except KeyboardInterrupt:
    print("\nMonitor stopped.")
    driver.quit()