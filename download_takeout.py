#!/usr/bin/env python3

import requests
import os
import time
import re
from pathlib import Path
from datetime import datetime
import json
import subprocess
import logging

def refresh_download_token():
    """
    Attempt to refresh the download token using token_retriever.py
    
    :return: Boolean indicating success or failure
    """
    try:
        # Run token retriever script
        result = subprocess.run(
            ['python3', 'token_retriever.py'], 
            capture_output=True, 
            text=True, 
            check=True
        )
        logging.info("Download token successfully refreshed")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Token refresh failed: {e.stderr}")
        return False

def create_url(index, job_id, rapt):
    """Create download URL with exact working format."""
    return (f"https://takeout.google.com/settings/takeout/download?"
            f"i={index}&"
            f"j={job_id}&"
            f"download=true&"
            f"rapt={rapt}")

def parse_curl(curl_text):
    """Extract auth info from curl command."""
    if not 'takeout.google.com' in curl_text:
        raise ValueError("Not a Google Takeout curl command")

    headers = {}
    for match in re.finditer(r"-H '([^:]+): ([^']+)'", curl_text):
        name, value = match.groups()
        headers[name] = value

    cookies = {}
    cookie_match = re.search(r"-b '([^']+)'", curl_text)
    if cookie_match:
        for pair in cookie_match.group(1).split('; '):
            if '=' in pair:
                name, value = pair.split('=', 1)
                cookies[name] = value

    rapt_match = re.search(r'rapt=([^&\s\']+)', curl_text)
    if not rapt_match:
        raise ValueError("No rapt token found")
    
    return headers, cookies, rapt_match.group(1)

def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Read secrets configuration
    try:
        with open('secrets.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        logging.error("secrets.json not found")
        return 1

    # Read curl command
    if not os.path.exists('curl.txt'):
        logging.error("curl.txt not found. Attempting to retrieve new token.")
        if not refresh_download_token():
            logging.error("Failed to retrieve new download token")
            return 1

    try:
        with open('curl.txt') as f:
            headers, cookies, rapt = parse_curl(f.read())
    except (ValueError, IOError) as e:
        logging.error(f"Error parsing curl.txt: {e}")
        if not refresh_download_token():
            logging.error("Failed to retrieve new download token after parsing error")
            return 1
        
        # Retry parsing after token refresh
        try:
            with open('curl.txt') as f:
                headers, cookies, rapt = parse_curl(f.read())
        except Exception as e:
            logging.error(f"Persistent error parsing curl.txt: {e}")
            return 1

    # Setup session
    session = requests.Session()
    session.headers.update(headers)
    session.cookies.update(cookies)
    session.timeout = 30  # 30 second timeout

    # Create output directory
    outdir = Path(config['google_takeout'].get('output_directory', '/mnt/f/GoogleTakeout'))
    outdir.mkdir(parents=True, exist_ok=True)

    # Find last downloaded file
    start = config['authentication'].get('last_downloaded_index', 0)
    max_files = config['google_takeout'].get('max_files', 277)

    print(f"Starting from index {start}")

    # Download files
    job_id = config['authentication'].get('job_id', 'unknown')
    download_delay = config['google_takeout'].get('download_delay', 5)

    for i in range(start, max_files):
        print(f"\nDownloading file {i}...")
        
        url = create_url(i, job_id, rapt)
        try:
            response = session.get(url, stream=True)
            
            if response.status_code == 404:
                print("File not found - archive may not be ready")
                return 1

            if response.status_code != 200:
                print(f"Error: Status {response.status_code}")
                # Attempt to refresh token
                if not refresh_download_token():
                    print("Failed to refresh download token")
                    return 1
                continue

            if 'html' in response.headers.get('content-type', ''):
                print("Error: Got HTML instead of file (auth failed)")
                # Attempt to refresh token
                if not refresh_download_token():
                    print("Failed to refresh download token")
                    return 1
                continue

            # Create unique temp filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            outfile = outdir / f"takeout-{timestamp}Z-{i:03d}.zip"
            tmpfile = outdir / f"tmp_{timestamp}_{i:03d}.zip"
            
            # Get expected size
            total_size = int(response.headers.get('content-length', 0))
            if total_size:
                print(f"Size: {total_size:,} bytes")
            
            print(f"Saving to {outfile.name}")
            try:
                with open(tmpfile, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                # Verify size if we got content-length
                if total_size and tmpfile.stat().st_size != total_size:
                    print("Error: Size mismatch")
                    tmpfile.unlink()
                    return 1
                    
                tmpfile.rename(outfile)
                
                # Update last downloaded index
                config['authentication']['last_downloaded_index'] = i + 1
                with open('secrets.json', 'w') as f:
                    json.dump(config, f, indent=4)
                
            except:
                if tmpfile.exists():
                    tmpfile.unlink()
                raise
                
        except requests.Timeout:
            print("Error: Request timed out")
            return 1
        except requests.RequestException as e:
            print(f"Error: {e}")
            return 1
            
        print(f"Waiting {download_delay} seconds...")
        time.sleep(download_delay)
    
    return 0

if __name__ == "__main__":
    exit(main())

# Path: download_takeout.py
