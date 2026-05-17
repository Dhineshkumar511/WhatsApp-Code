from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import pandas as pd
import time

# ==========================================
# CHROME SETUP
# ==========================================

options = Options()
options.add_argument(r"--user-data-dir=D:\selenium_profile")  # persistent login
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

# ==========================================
# OPEN WHATSAPP
# ==========================================

driver.get("https://web.whatsapp.com")
print("\n👉 Scan QR if needed...")
time.sleep(20)
print("✅ WhatsApp Loaded")

# ==========================================
# EXCEL FILE PATH
# ==========================================

excel_path = r"D:\DEVELOPMENT\Whatsapp code\CBE08_05_2026Summary/group_names.xlsx"
print(f"\n📂 Excel Loaded : {excel_path}")

df = pd.read_excel(excel_path)

# ==========================================
# FIND GROUP COLUMN
# ==========================================

possible_columns = ["group_name", "Group Name", "group", "GROUP", "Group", "Whatsapp name"]
group_column = None
for col in df.columns:
    if col in possible_columns:
        group_column = col
        break

if group_column is None:
    print("\n❌ Group column not found in Excel")
    print("\nAvailable Columns:\n")
    for c in df.columns:
        print(c)
    driver.quit()
    exit()

# ==========================================
# MATCH + SEND MESSAGE
# ==========================================

print("\n===================================")
print("MATCHED GROUPS + MESSAGE SENDING")
print("===================================\n")

matched = 0

for idx, row in df.iterrows():
    excel_group = str(row[group_column]).strip()
    custom_message = str(row.get("message", "hi")).strip()

    try:
        # --- SEARCH FOR GROUP ---
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Search or start a new chat']"))
        )
        search_box.click()
        search_box.clear()
        search_box.send_keys(excel_group)

        # --- CLICK GROUP CHAT ---
        group_el = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//span[@title="{excel_group}"]'))
        )
        group_el.click()

        # --- WAIT for chat to fully load ---
        # --- WAIT for chat to fully load ---
        time.sleep(3)

        # --- MESSAGE BOX (footer <p>) ---
        msg_box = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//footer//p[@class="selectable-text copyable-text"]'))
        )

        # --- TYPE + PRESS ENTER ---
        custom_message = str(row.get("message", "hi")).strip()
        msg_box.click()
        msg_box.send_keys(custom_message + u'\ue007')

        print(f"📨 SENT -> {excel_group} : {custom_message}")
        time.sleep(2)


    except Exception as e:
        print(f"❌ SEND FAILED -> {excel_group}")
        print(e)

# ==========================================
# FINAL RESULT
# ==========================================

print("\n===================================")
print("FINAL RESULT")
print("===================================\n")
print(f"✅ TOTAL MATCHED & SENT : {matched}")

input("\nPress ENTER to Exit...")
driver.quit()
