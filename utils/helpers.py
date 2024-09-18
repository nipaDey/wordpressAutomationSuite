
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
