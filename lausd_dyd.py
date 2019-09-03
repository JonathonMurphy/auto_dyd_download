from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

def download_wait(directory, timeout, nfiles):
    """
    Wait for downloads to finish with a specified timeout.

    Args
    ----
    directory : str
        The path to the folder where the files will be downloaded.
    timeout : int
        How many seconds to wait until timing out.
    nfiles : int
        Waits for the number of files specified.

    """
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < timeout:
        time.sleep(1)
        dl_wait = False
        files = os.listdir(directory)
        if nfiles and len(files) != nfiles:
            dl_wait = True

        for fname in directory:
            if fname.endswith('.crdownload'):
                dl_wait = True

        seconds += 1
    return seconds

def auto_dyd_report(username, password, directory="./", headless=True, timeout=120, nfiles=1):
    """
    Downloads the standard 18/19 DYD Report for the specified user.

    Args
    ----
    username : str
        The username to login as.
    password : str
        The password associated with the preceding username.
    directory : str, defaults to current directory
        The path to the folder where the file(s) will be downloaded.
    headless : boolean, defaults to True
        Determines if Selenium runs in headless mode or not.
    timeout : int, defaults to 120
        How many seconds to wait until timing out.
    nfiles : int, defaults to 1
        If provided, waits for the number of files specified.


    """
    print("auto_dyd_download: Starting")
    # Setup
    prefs = {'download.default_directory' : directory}
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', prefs)
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    # Currently downloading in headless mode introduces a bug where the download does not complete
    if headless == True:
        options.add_argument('--headless')
    driver = webdriver.Chrome("./chromedriver", options=options)
    print("auto_dyd_download: Opening Selenium")
    # Links
    login_page = "https://mclass.amplify.com"
    masq_login_page = "https://mclass.amplify.com/mobilelogin/internal_educator_login" # Must be on VPN
    dyd_page = "https://mclass.amplify.com/reports/DownloadYourData#/?assmt=7&assmt_versions=32"
    # Go to masq login page
    driver.get(masq_login_page)
    print("auto_dyd_download: Navigating to login page")
    # Wait until password field exists
    # Then login with credentials
    password_field = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    username_field = driver.find_element_by_id("login-username")
    username_field.send_keys(username)
    password_field.send_keys(password)
    print("auto_dyd_download: Logging in")
    password_field.submit()
    # Navigate to dyd page
    driver.get(dyd_page)
    print("auto_dyd_download: Navigating to DYD page")
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
    print("auto_dyd_download: Initiating download of DYD report")
    # A json log gets posted to the console in what I believe is the client logs that could be used as an indicator that the download has truely started
    # I could also use the a WebDriverWait on the loading animation to become invisible
    print(driver.get_log("client"))
    download_wait(directory, timeout, nfiles)
    driver.quit()
