#!/usr/bin/env python3

import os
import json
import getpass
import sys
import re
import logging

try:
    import keyring
    from keyring.errors import NoKeyringError
except ImportError:
    keyring = None

class SecretsValidator:
    def __init__(self, config_path='secrets.json'):
        """
        Initialize secrets validator and configuration manager
        
        :param config_path: Path to secrets configuration file
        """
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        """
        Load existing configuration or create default
        
        :return: Configuration dictionary
        """
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._create_default_config()
        except json.JSONDecodeError:
            self.logger.error(f"{self.config_path} is not a valid JSON file.")
            sys.exit(1)

    def _create_default_config(self):
        """
        Create a default configuration structure
        
        :return: Default configuration dictionary
        """
        return {
            "google_takeout": {
                "email": "",
                "password": "",
                "two_factor_secret": "",
                "max_files": 277,
                "output_directory": "/mnt/f/GoogleTakeout",
                "download_delay": 5
            },
            "authentication": {
                "job_id": "",
                "last_downloaded_index": 0,
                "last_token_refresh": None
            },
            "proxy": {
                "use_proxy": False,
                "proxy_type": "",
                "proxy_host": "",
                "proxy_port": None,
                "proxy_username": "",
                "proxy_password": ""
            },
            "logging": {
                "log_file": "takeout_download.log",
                "log_level": "INFO"
            }
        }

    def _validate_email(self, email):
        """
        Validate email format
        
        :param email: Email address to validate
        :return: Boolean indicating email validity
        """
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    def _store_credential(self, service, username, password):
        """
        Securely store credentials with fallback
        
        :param service: Service name
        :param username: Username 
        :param password: Password
        """
        # Check if keyring is available
        if keyring:
            try:
                keyring.set_password(service, username, password)
                self.logger.info(f"Credential stored securely for {username}")
                return True
            except (NoKeyringError, Exception) as e:
                self.logger.warning(f"Keyring storage failed: {e}")
        
        # Fallback to configuration file (less secure)
        try:
            # Update the specific section based on the service
            if service == 'google_takeout' and username == 'email':
                self.config['google_takeout']['email'] = password
            elif service == 'google_takeout' and username == 'password':
                self.config['google_takeout']['password'] = password
            
            self.save_config()
            self.logger.warning("Credentials stored in configuration file (not recommended)")
            return False
        except Exception as e:
            self.logger.error(f"Failed to store credential: {e}")
            return False

    def prompt_for_missing_info(self):
        """
        Interactively prompt for missing or invalid configuration
        """
        # Email validation and input
        while not self._validate_email(self.config['google_takeout']['email']):
            email = input("Enter your Google account email: ").strip()
            if self._validate_email(email):
                # Attempt to store email securely
                self._store_credential('google_takeout', 'email', email)
            else:
                print("Invalid email format. Please try again.")

        # Password input (always prompt securely)
        password = getpass.getpass("Enter your Google account password: ")
        if password:
            # Attempt to store password securely
            self._store_credential('google_takeout', 'password', password)

        # Two-factor secret (optional)
        two_factor = input("Enter two-factor secret (optional, press Enter to skip): ").strip()
        if two_factor:
            # Attempt to store two-factor secret
            self._store_credential('google_takeout', 'two_factor_secret', two_factor)

        # Output directory validation
        while True:
            output_dir = input(f"Enter output directory (current: {self.config['google_takeout']['output_directory']}): ").strip()
            if not output_dir:
                break
            
            if os.path.isdir(output_dir) or not os.path.exists(output_dir):
                self.config['google_takeout']['output_directory'] = output_dir
                break
            else:
                print("Invalid directory. Please provide a valid path.")

        # Download delay
        while True:
            delay = input(f"Enter download delay in seconds (current: {self.config['google_takeout']['download_delay']}): ").strip()
            if not delay:
                break
            
            try:
                delay_value = int(delay)
                if delay_value > 0:
                    self.config['google_takeout']['download_delay'] = delay_value
                    break
                else:
                    print("Delay must be a positive integer.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # Save updated configuration
        self.save_config()

    def save_config(self):
        """
        Save updated configuration to file
        """
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            self.logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")
            sys.exit(1)

    def validate_config(self):
        """
        Comprehensive configuration validation
        
        :return: Boolean indicating configuration validity
        """
        errors = []

        # Email validation
        if not self._validate_email(self.config['google_takeout']['email']):
            errors.append("Invalid email address")

        # Output directory validation
        output_dir = self.config['google_takeout']['output_directory']
        if not os.path.isdir(output_dir) and not os.path.exists(output_dir):
            errors.append(f"Invalid output directory: {output_dir}")

        # Download delay validation
        delay = self.config['google_takeout']['download_delay']
        if not isinstance(delay, int) or delay <= 0:
            errors.append("Download delay must be a positive integer")

        # Display errors and prompt for correction
        if errors:
            print("Configuration Errors:")
            for error in errors:
                print(f"- {error}")
            return False

        return True

def main():
    """
    Main entry point for secrets configuration
    """
    print("Google Takeout Download Configuration Wizard")
    print("-------------------------------------------")

    # Check for keyring availability
    if not keyring:
        print("\nWARNING: Keyring module not available.")
        print("Credentials will be stored in the configuration file.")
        print("This is NOT recommended for security reasons.\n")

    validator = SecretsValidator()

    # Validate existing configuration
    if not validator.validate_config():
        print("\nConfiguration needs updating.")
        validator.prompt_for_missing_info()
    else:
        print("\nConfiguration is valid.")
        choice = input("Would you like to update the configuration? (y/N): ").strip().lower()
        if choice == 'y':
            validator.prompt_for_missing_info()

if __name__ == "__main__":
    main()

# Path: configure_secrets.py
