#!/usr/bin/env python3

import json
import os
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging

class TakeoutTokenRetriever:
    def __init__(self, secrets_path='secrets.json', log_path='takeout_download.log'):
        """
        Initialize the Takeout Token Retriever
        
        :param secrets_path: Path to secrets configuration file
        :param log_path: Path to log file
        """
        # Configure logging
        logging.basicConfig(
            filename=log_path, 
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

        # Load secrets
        try:
            with open(secrets_path, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.logger.error(f"Secrets file not found: {secrets_path}")
            raise

        # Validate required configuration
        required_keys = ['google_takeout', 'authentication']
        for key in required_keys:
            if key not in self.config:
                raise ValueError(f"Missing required configuration section: {key}")

    def _setup_webdriver(self):
        """
        Setup Chrome WebDriver with appropriate options
        
        :return: Configured WebDriver
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), 
            options=chrome_options
        )

    def retrieve_download_token(self):
        """
        Retrieve a new download token for Google Takeout
        
        :return: Dictionary with updated authentication details
        """
        driver = self._setup_webdriver()

        try:
            # Login to Google
            driver.get("https://accounts.google.com/signin/v2/identifier")

            # Enter email
            email = self.config['google_takeout']['email']
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "identifierId"))
            )
            email_input.send_keys(email)
            driver.find_element(By.ID, "identifierNext").click()

            # Enter password
            password = self.config['google_takeout']['password']
            password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "Passwd"))
            )
            password_input.send_keys(password)
            driver.find_element(By.ID, "passwordNext").click()

            # Navigate to Takeout
            driver.get("https://takeout.google.com/settings/takeout")

            # Wait for Takeout page and Download button
            download_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Download')]"))
            )
            download_button.click()

            # Wait and capture network requests
            time.sleep(5)

            # Capture current URL for job_id and other download parameters
            current_url = driver.current_url
            
            # Extract job_id from URL
            job_id_match = re.search(r'j=([^&]+)', current_url)
            job_id = job_id_match.group(1) if job_id_match else None

            # Prepare cURL command
            headers = {h.get_attribute('name'): h.get_attribute('value') 
                       for h in driver.find_elements(By.XPATH, "//meta[@name]")}
            
            # Construct cURL command
            curl_command = (
                f"curl 'https://takeout.google.com/settings/takeout/download?i=0&j={job_id}&download=true' "
                + " ".join([f"-H '{k}: {v}'" for k, v in headers.items()])
            )

            # Update configuration
            self.config['authentication']['job_id'] = job_id
            self.config['authentication']['last_token_refresh'] = time.time()

            # Save cURL command to file
            with open('curl.txt', 'w') as f:
                f.write(curl_command)

            # Log successful token retrieval
            self.logger.info(f"Successfully retrieved new download token for job {job_id}")

            return self.config

        except Exception as e:
            self.logger.error(f"Error retrieving download token: {e}")
            raise

        finally:
            driver.quit()

    def save_config(self, secrets_path='secrets.json'):
        """
        Save updated configuration back to secrets file
        
        :param secrets_path: Path to save updated secrets
        """
        try:
            with open(secrets_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            self.logger.info(f"Updated configuration saved to {secrets_path}")
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")
            raise

def main():
    try:
        retriever = TakeoutTokenRetriever()
        retriever.retrieve_download_token()
        retriever.save_config()
        print("Download token successfully refreshed!")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()

# Path: token_retriever.py
