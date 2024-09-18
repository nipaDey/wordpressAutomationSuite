
# WordPress Automation Test Suite

This automation suite is built using Python and Selenium to perform end-to-end testing on a WordPress site. The suite checks if the "WP Dark Mode" plugin is installed and active, configures various settings, and verifies if dark mode is applied to the frontend.


## Features

- Logs into the WordPress admin panel
- Checks if the "WP Dark Mode" plugin is active
- Installs and activates the plugin if not already installed
- Enables dark mode in the WordPress admin dashboard and frontend
- Customizes dark mode settings
- Validates whether dark mode is active on both admin and frontend

## Prerequisites
Make sure you have the following installed:
- Python 3.x
- Git
- Google Chrome browser for supported by Selenium
- ChromeDriver

## Setup Instructions
 ### 1.Clone the repository







```bash
  git clone < 'https://github.com/nipaDey/wordpressAutomationSuite.git'>

  cd <wordpressAutomationSuite>

```
 ### 2. Install Dependencies

```bash
  pip install python-dotenv

```
```bash
  pip install selenium

```
```bash
  pip install -r requirements.txt

```
 ### 3.Create a .env file
Create a .env file in the root directory with the following content:

```bash
  WORDPRESS_URL=your-wordpress-url
  WORDPRESS_USERNAME=your-username
  WORDPRESS_PASSWORD=your-password


```


### 4.Test Structure
- test_dark_mode.py: The main test suite.
- utils/helpers.py: Helper functions such as login, checking plugin status, and installing/activating plugins.

##  Code Overview
### 1. test_dark_mode.py
This file is the main test file
```bash
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.helpers import login, is_plugin_active, install_and_activate_plugin
driver = webdriver.Chrome()

try:
    # Step 1: Log in
    login(driver)

    if not is_plugin_active(driver):
        time.sleep(2)
        # driver.get(os.getenv("WORDPRESS_URL") + "/wp-admin/plugins.php")
        # driver.find_element(By.XPATH,"//a[@class='page-title-action']").click()
        # driver.find_element(By.ID,"search-plugins").click()
        # driver.find_element(By.ID,"search-plugins").send_keys("wp dark mode")
        # time.sleep(2)
        install_and_activate_plugin(driver)
        time.sleep(10)
    else:
        print("Plagin Active ")


    driver.get(os.getenv("WORDPRESS_URL") + "/wp-admin/admin.php?page=wp-dark-mode-settings")
    time.sleep(5)

    #Enable Admin Dashboard Dark Mode
    driver.find_element(By.XPATH, "//a[text()='Admin Panel Dark Mode']").click()
    driver.find_element(By.XPATH, "//div[text()='Enable Admin Dashboard Dark Mode']").click()
    driver.find_element(By.XPATH, "//button[text()='Save Changes']").click()


    assert "Enable Admin Dashboard Dark Mode" in driver.page_source

    # Change Floating Switch Style
    driver.find_element(By.XPATH, "//h4[text()='Customization']").click()
    driver.find_element(By.XPATH, "//a[text()='Switch Settings']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//div[contains(@class,'wp-dark-mode-ignore wp-dark-mode-switch ignore dummy wp-dark-mode-switch-2')]").click()
    driver.find_element(By.XPATH, "//button[text()='Save Changes']").click()
    time.sleep(2)

    # Set switch size to "M"
    driver.find_element(By.XPATH, "//span[text()='M']").click()
    driver.find_element(By.XPATH, "//button[text()='Save Changes']").click()
    time.sleep(2)

    # Change Floating Switch Position to Left
    driver.find_element(By.XPATH, "//span[text()='Left']").click()
    driver.find_element(By.XPATH, "//button[text()='Save Changes']").click()
    time.sleep(2)

    # Disable keyboard shortcuts
    driver.find_element(By.XPATH, "//a[text()='Accessibility']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[text()='Keyboard Shortcut']").click()
    driver.find_element(By.XPATH, "//button[text()='Save Changes']").click()
    time.sleep(2)

    # Enable Page-Transition Animation
    driver.find_element(By.XPATH, "//a[text()='Site Animation']").click()
    driver.find_element(By.XPATH, "//div[text()='Enable Page Transition Animation']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//span[text()='Fade In']").click()
    driver.find_element(By.XPATH, "//button[text()='Save Changes']").click()
    time.sleep(1)

    #Validate Dark Mode on Front
    driver.get(os.getenv("WORDPRESS_URL"))
    assert "wp-dark-mode-active" in driver.page_source
    print("Active")

finally:
    driver.quit()


```
###  2. utils/helpers.py
This file contains helper functions that support the main test file:
```bash
   
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()

def login(driver):
    """Log in to the WordPress admin panel."""
    driver.get(os.getenv("WORDPRESS_URL") + "/wp-login.php")
    driver.find_element(By.ID, "user_login").send_keys(os.getenv("WORDPRESS_USERNAME"))
    driver.find_element(By.ID, "user_pass").send_keys(os.getenv("WORDPRESS_PASSWORD"))
    driver.find_element(By.ID, "wp-submit").click()

def is_plugin_active(driver):
    """Checks if the 'WP Dark Mode' plugin is active."""
    driver.get(os.getenv("WORDPRESS_URL") + "/wp-admin/plugins.php")
    try:
        # Find the "Deactivate" button for the 'WP Dark Mode' plugin
        plugin_row = driver.find_element(By.XPATH, "//tr[contains(@class, 'active') and contains(., 'WP Dark Mode')]")
        deactivate_button = plugin_row.find_element(By.LINK_TEXT, "Deactivate")
        return True if deactivate_button else False
    except Exception:
        return False

def install_and_activate_plugin(driver):
    """Installs and activates the 'WP Dark Mode' plugin"""
    driver.get(os.getenv("WORDPRESS_URL") + "/wp-admin/plugin-install.php?tab=search&s=wp+dark+mode")

    #"Install Now" button
    install_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'install-now'))
    )
    install_button.click()

    # "Activate Now" button
    activate_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'activate-now'))
    )
    activate_button.click()

    # Wait until the "Activate Now" button is no longer visible to ensure activation is complete
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element((By.CLASS_NAME, 'activate-now'))
    )

    print("Plugin installed and activated successfully.")


```
###  3. .env file
This file is an .env file to store sensitive information such as WordPress URL, username, and password.
```bash
  WORDPRESS_URL=your-wordpress-url
  WORDPRESS_USERNAME=your-username
  WORDPRESS_PASSWORD=your-password

```
 ### 4. .env file example
This file is an example .env file with dammy information 

```bash
  WORDPRESS_URL=http://shopnow.local
  WORDPRESS_USERNAME=nipa
  WORDPRESS_PASSWORD=nipa


```
###  5.requirements.txt
```bash
  selenium==4.24.0
  python-dotenv==1.0.1
  chromedriver==2.24.1

```
## Pushing to GitHub
### 1. Initialize a Git Repository
```bash
  git init

```
###  2. Add Files to the Repository
```bash
  git add .

```
### 3. Commit the Changes
```bash
  git commit -m "first commit"


```
### 5. Add GitHub Remote
```bash
 git remote add origin https://github.com/nipaDey/wordpressAutomationSuite.git/


```
###  6.Push the Code to GitHub
```bash
  git push -u origin master

```
###  7. Sharing the Repository
```bash
  https://github.com/nipaDey/wordpressAutomationSuite.git

```







