from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time

options = Options()
options.add_argument(r"--user-data-dir=D:\selenium_profile")
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

driver.get("https://web.whatsapp.com")
print("👉 Scan QR if needed...")
time.sleep(20)

# --- Search for Contact ---
contact_name = "Monika"   # replace with actual contact

# --- Search for Contact ---
search_box = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Search or start a new chat']"))
)
search_box.click()
search_box.clear()
search_box.send_keys(contact_name)

# --- Click Contact ---
contact_el = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.XPATH, f'//span[@title="{contact_name}"]'))
)
contact_el.click()

# --- Message Box ---
msg_box = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='conversation-compose-box-input']"))
)

# --- Type + Press ENTER ---
message = "Hello, this is a test message!"
ActionChains(driver).click(msg_box).send_keys(message).send_keys(u'\ue007').perform()

print(f"📨 SENT -> {contact_name} : {message}")

time.sleep(3)

driver.quit()
