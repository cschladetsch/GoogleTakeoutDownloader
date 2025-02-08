#!/usr/bin/env python3

import os
import sys
import json
import time
import logging
import traceback
import subprocess

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re

def setup_logging():
    """Configure comprehensive logging"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('token_retriever.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def get_chrome_version():
    """
    Get the installed Chrome/Chromium version
    
    :return: Version string
    """
    try:
        # Try Chromium browser first
        version_output = subprocess.check_output(
            ["chromium-browser", "--version"], 
            text=True
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # Fallback to Google Chrome
            version_output = subprocess.check_output(
                ["google-chrome", "--version"], 
                text=True
            ).strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError("No Chrome/Chromium browser found")
    
    # Extract version number
    version_match = re.search(r'\d+\.\d+\.\d+\.\d+', version_output)
    if not version_match:
        raise RuntimeError(f"Could not parse version from: {version_output}")
    
    return version_match.group(0)

def setup_webdriver():
    """
    Set up WebDriver with comprehensive options
    
    :return: Configured Chrome WebDriver
    """
    logger = logging.getLogger(__name__)
    
    # Chrome options
    chrome_options = Options()
    
    # Disable headless mode for debugging
    # chrome_options.add_argument("--headless")  # Commented out
    
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Add additional chrome options to resolve DevTools issue
    chrome_options.add_argument("--remote-debugging-port=9222")
    
    try:
        # Get the current Chromium version
        chrome_version = get_chrome_version()
        logger.info(f"Detected Chromium version: {chrome_version}")
        
        # Setup WebDriver 
        service = Service(ChromeDriverManager().install())
        
        # Create WebDriver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Set comprehensive timeouts
        driver.set_page_load_timeout(30)  # 30 seconds page load
        driver.set_script_timeout(30)     # 30 seconds script timeout
        
        logger.info("WebDriver successfully initialized")
        return driver
    
    except Exception as e:
        logger.error(f"WebDriver setup failed: {e}")
        logger.error(traceback.format_exc())
        raise

def retrieve_token():
    """
    Comprehensive token retrieval process
    """
    logger = setup_logging()
    driver = None
    
    try:
        # Load secrets
        with open('secrets.json', 'r') as f:
            config = json.load(f)
        
        # Extract credentials
        email = config['google_takeout']['email']
        password = config['google_takeout']['password']
        
        logger.info("Starting token retrieval process")
        
        # Setup WebDriver
        driver = setup_webdriver()
        
        # Navigate to Google login
        logger.info("Navigating to Google login")
        driver.get("https://accounts.google.com/signin/v2/identifier")
        
        # Wait and enter email
        logger.info("Entering email")
        email_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_input.send_keys(email)
        driver.find_element(By.ID, "identifierNext").click()
        
        # Wait and enter password
        logger.info("Entering password")
        password_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "Passwd"))
        )
        password_input.send_keys(password)
        driver.find_element(By.ID, "passwordNext").click()
        
        # Navigate to Takeout
        logger.info("Navigating to Google Takeout")
        driver.get("https://takeout.google.com/settings/takeout")
        
        # Wait for download button
        logger.info("Waiting for download button")
        download_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Download')]"))
        )
        download_button.click()
        
        # Capture URL and parameters
        logger.info("Capturing download parameters")
        current_url = driver.current_url
        
        # Extract job ID
        job_id_match = re.search(r'j=([^&]+)', current_url)
        job_id = job_id_match.group(1) if job_id_match else None
        
        # Prepare cURL command
        headers = {h.get_attribute('name'): h.get_attribute('value') 
                   for h in driver.find_elements(By.XPATH, "//meta[@name]")}
        
        curl_command = (
            f"curl 'https://takeout.google.com/settings/takeout/download?i=0&j={job_id}&download=true' "
            + " ".join([f"-H '{k}: {v}'" for k, v in headers.items()])
        )
        
        # Save cURL command
        with open('curl.txt', 'w') as f:
            f.write(curl_command)
        
        # Update configuration
        config['authentication']['job_id'] = job_id
        config['authentication']['last_token_refresh'] = time.time()
        
        # Save updated configuration
        with open('secrets.json', 'w') as f:
            json.dump(config, f, indent=4)
        
        logger.info(f"Successfully retrieved download token for job {job_id}")
        print(f"Download token retrieved for job {job_id}")
    
    except Exception as e:
        logger.error(f"Token retrieval failed: {e}")
        logger.error(traceback.format_exc())
        print(f"Error: {e}")
        raise
    
    finally:
        # Always quit the driver
        if driver:
            driver.quit()

def main():
    try:
        retrieve_token()
    except Exception as e:
        sys.exit(1)

if __name__ == "__main__":
    main()

# Path: token_retriever.py
