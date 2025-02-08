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
- `requests` library
- WSL Ubuntu (for accessing Windows paths like `/mnt/f/`)

## Installation

1. Install the required Python package:
```bash
pip3 install requests
```

2. Clone or download this repository
3. Make the script executable:
```bash
chmod +x download_takeout.py
```

## Usage

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

- Maximum supported file index is 277
- The script requires you to be logged into your Google account
- Downloads are saved with timestamps in the filename
- The script includes error handling and will skip failed downloads

## Error Handling

- Validates all input parameters
- Handles network errors gracefully
- Skips already downloaded files when using --continue
- Prevents invalid index ranges

## Contributing

Feel free to submit issues and enhancement requests.
