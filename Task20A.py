from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize WebDriver
driver = webdriver.Chrome()

try:
    # Step 1: Open the CoWIN homepage
    driver.get("https://www.cowin.gov.in/")

    # Step 2: Wait for the page to load by waiting for a reliable element
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "a"))
    )

    # Step 3: Print out all link texts for debugging
    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        print(link.text)

    # Step 4: Find and click the "FAQ" link
    faq_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "FAQ"))
    )
    faq_link.click()

    # Step 5: Find and click the "Partners" link
    partners_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Partners"))
    )
    partners_link.click()

    # Step 6: Get all window handles
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
    window_handles = driver.window_handles

    # Display the window handles
    print("Window Handles:")
    for handle in window_handles:
        print(handle)

    # Close the new windows (FAQ and Partners)
    for handle in window_handles:
        if handle != driver.current_window_handle:
            driver.switch_to.window(handle)
            driver.close()

    # Step 7: Switch back to the original window
    driver.switch_to.window(driver.window_handles[0])
    print("Returned to the original window")

finally:
    # Close the WebDriver
    driver.quit()
