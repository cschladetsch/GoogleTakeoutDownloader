# Google Takeout Batch Downloader

A Python script to automate downloading multiple Google Takeout files in sequence. Useful when you have a large Google Takeout export split across many files.

## Features

- Download multiple Takeout files sequentially
- Continue from last downloaded file
- Customizable delay between downloads
- Progress tracking
- Handles Google Takeout's standard filename format
- Supports WSL Ubuntu environment

## Prerequisites

- Python 3.x
- WSL Ubuntu (for accessing Windows paths like `/mnt/f/`)
- python3-full (for virtual environment support)

## Installation

You have several options for installation:

### Option 1: Using a Virtual Environment (Recommended)

1. Install Python virtual environment support:
```bash
sudo apt install python3-full
```

2. Create a virtual environment:
```bash
python3 -m venv venv
```

3. Activate the virtual environment:
```bash
source venv/bin/activate
```

4. Install the required package:
```bash
pip install requests
```

### Option 2: Using pipx

1. Install pipx:
```bash
sudo apt install pipx
```

2. Install the requests package:
```bash
pipx install requests
```

### Option 3: Using System Packages

Install the Python requests package directly through apt:
```bash
sudo apt install python3-requests
```

After choosing an installation method:

1. Clone or download this repository
2. Make the script executable:
```bash
chmod +x download_takeout.py
```

## Configuration

Before using the script, you need to configure it for your Google account and Takeout URLs:

1. Open one of your Google Takeout download URLs in a browser. It should look something like:
```
https://accounts.google.com/AccountChooser?continue=https://takeout.google.com/settings/takeout/download?j%3Daad05205-2695-41f5-a4d7-b92d9a095d5e%26i%3D52&Email=example@gmail.com
```

2. Open `download_takeout.py` and modify these values in the `create_url()` function:
```python
job_id = "aad05205-2695-41f5-a4d7-b92d9a095d5e"  # Extract from your URL
email = "example@gmail.com"  # Your Google email
```

3. If your Takeout export has a different number of files, update:
```python
MAX_FILES = 277  # Set to your total number of files
```

## Usage

If you're using a virtual environment, make sure to activate it first:
```bash
source venv/bin/activate
```

### Basic Usage

Download a range of files:
```bash
./download_takeout.py -s 1 -e 10
```

### Continue from Last Download

To continue from where you left off:
```bash
./download_takeout.py --continue
```

### Specify Custom Directory

Use a different output directory:
```bash
./download_takeout.py -s 1 -e 10 -d /path/to/custom/directory
```

### Adjust Download Delay

Change the waiting time between downloads:
```bash
./download_takeout.py -s 1 -e 10 --delay 10
```

## Command Line Options

- `-s, --start`: Starting index for download sequence
- `-e, --end`: Ending index for download sequence (max 277)
- `-d, --directory`: Output directory (default: /mnt/f/GoogleTakeout)
- `--delay`: Delay in seconds between downloads (default: 5)
- `--continue`: Continue from last downloaded file
- `-h, --help`: Show help message

## File Naming

The script handles Google Takeout's standard file naming format:
```
takeout-YYYYMMDDTHHMMSSZ-NNN.zip
```
Example: `takeout-20250206T053943Z-016.zip`

## Notes

- Maximum supported file index is configurable (default 277)
- The script requires you to be logged into your Google account in your browser
- Downloads are saved with timestamps in the filename
- The script includes error handling and will skip failed downloads
- URLs expire after some time - if downloads fail, you may need to get a new URL from Google Takeout and update the job_id
- If using a virtual environment, remember to activate it before running the script

## Error Handling

- Validates all input parameters
- Handles network errors gracefully
- Skips already downloaded files when using --continue
- Prevents invalid index ranges

## Contributing

Feel free to submit issues and enhancement requests.
