from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()

# Use separate profile (IMPORTANT)
options.add_argument(r"--user-data-dir=D:\selenium_profile")

driver = webdriver.Chrome(options=options)

driver.get("https://web.whatsapp.com")
