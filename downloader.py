"""Google Takeout file downloader module."""

import os
import time
import re
from pathlib import Path
from typing import Optional, Tuple
import requests
from urllib.parse import quote

class TakeoutDownloader:
    """Handles downloading of Google Takeout files."""
    
    def __init__(self, job_id: str, email: str, max_files: int = 277):
        """Initialize the downloader with job details.
        
        Args:
            job_id: The Google Takeout job ID
            email: The Google account email
            max_files: Maximum number of files in the takeout
        """
        self.job_id = job_id
        self.email = email
        self.max_files = max_files

    def create_url(self, index: int) -> str:
        """Generate the URL for a specific index."""
        base_url = "https://accounts.google.com/AccountChooser"
        continue_param = "https://takeout.google.com/settings/takeout/download"
        
        takeout_url = f"{continue_param}?j%3D{self.job_id}%26i%3D{index}"
        encoded_takeout_url = quote(takeout_url, safe='')
        
        return f"{base_url}?continue={encoded_takeout_url}&Email={self.email}"

    @staticmethod
    def find_last_downloaded_index(directory: str) -> int:
        """Scan the output directory to find the last downloaded file index."""
        if not os.path.exists(directory):
            return 0
            
        pattern = re.compile(r'takeout-\d{8}T\d{6}Z-(\d{3})\.zip')
        max_index = 0
        
        for filename in os.listdir(directory):
            match = pattern.match(filename)
            if match:
                index = int(match.group(1))
                max_index = max(max_index, index)
                
        return max_index

    def download_file(self, url: str, output_dir: Path, index: int) -> bool:
        """Download a file from the given URL and save it to the output directory."""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            filename = f"takeout-{time.strftime('%Y%m%d')}T{time.strftime('%H%M%S')}Z-{index:03d}.zip"
            if 'Content-Disposition' in response.headers:
                cd = response.headers['Content-Disposition']
                if 'filename=' in cd:
                    filename = cd.split('filename=')[1].strip('"')
            
            output_path = output_dir / filename
            
            print(f"Downloading {filename}...")
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print(f"Successfully downloaded {filename}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Error downloading file {index}: {str(e)}")
            return False

    def download_range(self, start: int, end: int, output_dir: str, delay: int = 5) -> None:
        """Download a range of files.
        
        Args:
            start: Starting index
            end: Ending index
            output_dir: Directory to save files
            delay: Delay between downloads in seconds
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        total_files = end - start + 1
        print(f"Downloading files {start} through {end}")
        print(f"Output directory: {output_path}")
        print(f"Delay between downloads: {delay} seconds")
        print(f"Total files to download: {total_files}")
        
        for index in range(start, end + 1):
            url = self.create_url(index)
            print(f"\nProcessing index {index} ({index - start + 1}/{total_files})")
            
            success = self.download_file(url, output_path, index)
            
            if success and index < end:
                print(f"Waiting {delay} seconds before next download...")
                time.sleep(delay)
