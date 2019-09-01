from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# Path
download_path = "/Users/jmurphy/Downloads/GitHub/workShit"
# Setup
prefs = {'download.default_directory' : download_path}
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', prefs)
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
# options.add_argument('--headless') # Uncomment to run in headless mode
driver = webdriver.Chrome("./chromedriver", options=options)

def download_dyd_report():
    # Links
    login_page = "https://mclass.amplify.com"
    masq_login_page = "https://mclass.amplify.com/mobilelogin/internal_educator_login" # Must be on VPN
    dyd_page = "https://mclass.amplify.com/reports/DownloadYourData#/?assmt=7&assmt_versions=32"
    # Credentials
    username = ""
    password = ""
    # Go to masq login page
    driver.get(masq_login_page)
    # Wait until password field exists
    # Then login with credentials
    password_field = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    username_field = driver.find_element_by_id("login-username")
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.submit()
    # Navigate to dyd page
    driver.get(dyd_page)
    # Wait for loading screen to be invisible
    loading_icon = WebDriverWait(driver, 40).until(
        EC.invisibility_of_element_located((By.ID, "loading-icon"))
    )
    # Download button
    download_button = driver.find_element_by_class_name("download")
    download_button.click()
    # Confirm download
    confirm_download = driver.find_element_by_css_selector("button.btn.btn-primary.ng-binding")
    confirm_download.click()

download_dyd_report()
