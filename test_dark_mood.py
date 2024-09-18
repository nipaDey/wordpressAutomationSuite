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
