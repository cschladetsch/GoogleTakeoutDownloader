#!/usr/bin/env python3

import requests
import os
import time
import re
from pathlib import Path
from datetime import datetime

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
    # Read curl command
    if not os.path.exists('curl.txt'):
        print("Save the download request as curl command to curl.txt")
        print("1. Press F12 in Edge")
        print("2. Find request with download=true")
        print("3. Copy as cURL (bash)")
        return 1

    try:
        with open('curl.txt') as f:
            headers, cookies, rapt = parse_curl(f.read())
    except ValueError as e:
        print(f"Error: {e}")
        return 1

    # Setup session
    session = requests.Session()
    session.headers.update(headers)
    session.cookies.update(cookies)
    session.timeout = 30  # 30 second timeout

    # Create output directory
    outdir = Path('/mnt/f/GoogleTakeout')
    outdir.mkdir(parents=True, exist_ok=True)

    # Find last downloaded file
    start = 0
    for file in outdir.glob('takeout-*-*.zip'):
        match = re.search(r'-(\d{3})\.zip$', file.name)
        if match:
            start = max(start, int(match.group(1)) + 1)

    print(f"Starting from index {start}")

    # Download files
    job_id = "aad05205-2695-41f5-a4d7-b92d9a095d5e"
    for i in range(start, 278):
        print(f"\nDownloading file {i}...")
        
        url = create_url(i, job_id, rapt)
        try:
            response = session.get(url, stream=True)
            
            if response.status_code == 404:
                print("File not found - archive may not be ready")
                return 1

            if response.status_code != 200:
                print(f"Error: Status {response.status_code}")
                return 1
            
            if 'html' in response.headers.get('content-type', ''):
                print("Error: Got HTML instead of file (auth failed)")
                return 1

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
            
        print("Waiting 5 seconds...")
        time.sleep(5)
    
    return 0

if __name__ == "__main__":
    exit(main())

# File: download_takeout.py
