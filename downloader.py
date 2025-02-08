#!/usr/bin/env python3

import os
import time
import requests
import argparse
import re
from pathlib import Path
from urllib.parse import quote

MAX_FILES = 277

def create_url(index):
    """Generate the URL for a specific index."""
    base_url = "https://accounts.google.com/AccountChooser"
    continue_param = "https://takeout.google.com/settings/takeout/download"
    job_id = "aad05205-2695-41f5-a4d7-b92d9a095d5e"  # From your example URL
    email = "christian.schladetsch@gmail.com"
    
    takeout_url = f"{continue_param}?j%3D{job_id}%26i%3D{index}"
    encoded_takeout_url = quote(takeout_url, safe='')
    
    return f"{base_url}?continue={encoded_takeout_url}&Email={email}"

def find_last_downloaded_index(directory):
    """Scan the output directory to find the last downloaded file index."""
    if not os.path.exists(directory):
        return 0
        
    # Pattern for 'takeout-20250206T053943Z-016.zip'
    pattern = re.compile(r'takeout-\d{8}T\d{6}Z-(\d{3})\.zip')
    max_index = 0
    
    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            # Convert file number (e.g., '016') to integer
            index = int(match.group(1))
            max_index = max(max_index, index)
            
    return max_index

def download_file(url, output_dir, index):
    """Download a file from the given URL and save it to the output directory."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Get filename from Content-Disposition header, or create a default one
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

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Download Google Takeout files in sequence.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
  %(prog)s -s 50 -e 52
  %(prog)s -s 1 -e 10 -d /custom/output/directory
  %(prog)s -s 1 -e 5 --delay 10
  %(prog)s --continue
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-s', '--start', 
                      type=int,
                      help='Starting index for download sequence')
    group.add_argument('--continue', 
                      action='store_true',
                      dest='continue_flag',
                      help='Continue from last downloaded file')
    
    parser.add_argument('-e', '--end', 
                        type=int,
                        help=f'Ending index for download sequence (max {MAX_FILES})')
    
    parser.add_argument('-d', '--directory', 
                        type=str, 
                        default='/mnt/f/GoogleTakeout',
                        help='Output directory (default: /mnt/f/GoogleTakeout)')
    
    parser.add_argument('--delay', 
                        type=int, 
                        default=5,
                        help='Delay in seconds between downloads (default: 5)')
    
    args = parser.parse_args()
    
    # Handle continue flag
    if args.continue_flag:
        args.start = find_last_downloaded_index(args.directory) + 1
        if not args.end:
            args.end = MAX_FILES
        print(f"Continuing from index {args.start}")
    
    # Validate arguments
    if args.end is None:
        parser.error("End index is required when not using --continue")
    
    if args.end > MAX_FILES:
        parser.error(f"End index cannot exceed {MAX_FILES}")
    
    if args.start > args.end:
        parser.error("Start index must be less than or equal to end index")
    
    if args.delay < 0:
        parser.error("Delay must be non-negative")
    
    if args.start < 1:
        parser.error("Start index must be at least 1")
        
    return args

def main():
    # Parse command line arguments
    args = parse_arguments()
    
    # Create output directory if it doesn't exist
    output_dir = Path(args.directory)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Downloading files {args.start} through {args.end}")
    print(f"Output directory: {output_dir}")
    print(f"Delay between downloads: {args.delay} seconds")
    
    # Calculate and show progress information
    total_files = args.end - args.start + 1
    print(f"Total files to download: {total_files}")
    
    # Download files
    for index in range(args.start, args.end + 1):
        url = create_url(index)
        print(f"\nProcessing index {index} ({index - args.start + 1}/{total_files})")
        
        success = download_file(url, output_dir, index)
        
        if success and index < args.end:
            # Wait between downloads to avoid overwhelming the server
            print(f"Waiting {args.delay} seconds before next download...")
            time.sleep(args.delay)

if __name__ == "__main__":
    main()
