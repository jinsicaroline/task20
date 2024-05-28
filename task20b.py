import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Setup WebDriver
driver = webdriver.Chrome()  # Ensure chromedriver is in your PATH or provide the executable path

# Go to the website
driver.get("https://labour.gov.in/")

# Create directory to store downloaded files
os.makedirs("downloads/photos", exist_ok=True)

# Function to download a file from a URL
def download_file(url, filepath):
    response = requests.get(url)
    with open(filepath, 'wb') as file:
        file.write(response.content)

# Download Monthly Progress Report
try:
    # Wait for the "Documents" menu and hover over it
    documents_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[text()='Documents']"))
    )
    ActionChains(driver).move_to_element(documents_menu).perform()

    # Click on the Monthly Progress Report link
    monthly_report_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Monthly Progress Report']"))
    )
    monthly_report_link.click()

    # Get the link of the latest report (assuming the first one is the latest)
    latest_report_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "(//a[contains(text(), 'Monthly Progress Report')])[1]"))
    )
    report_url = latest_report_link.get_attribute('href')

    # Download the file
    download_file(report_url, "downloads/Monthly_Progress_Report.pdf")
    print("Monthly Progress Report downloaded successfully.")
except Exception as e:
    print(f"Failed to download Monthly Progress Report: {e}")

# Download 10 photos from the Photo Gallery
try:
    # Navigate to "Media" > "Photo Gallery"
    media_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[text()='Media']"))
    )
    ActionChains(driver).move_to_element(media_menu).perform()

    photo_gallery_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Photo Gallery']"))
    )
    photo_gallery_link.click()

    # Wait for the photo gallery page to load and find the images
    image_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='view-content']//img"))
    )

    # Download the first 10 images
    for i, img in enumerate(image_elements[:10]):
        img_url = img.get_attribute('src')
        img_response = requests.get(img_url)
        with open(f"downloads/photos/photo_{i + 1}.jpg", 'wb') as file:
            file.write(img_response.content)

    print("10 photos downloaded successfully.")
except Exception as e:
    print(f"Failed to download photos: {e}")

# Close the browser
driver.quit()
