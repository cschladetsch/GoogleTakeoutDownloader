# Google Takeout Batch Downloader

A robust Python script designed to automate the download of large Google Takeout exports split across multiple files.

## Features

- Batch download of multiple Takeout files
- Seamless progress tracking
- Ability to resume downloads from last completed file
- Comprehensive error handling
- Cross-platform compatibility (tested on WSL Ubuntu)

## Prerequisites

- Python 3.7+
- `requests` library
- Active Google Takeout export
- Modern web browser

## Installation

### Set Up Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Make Script Executable

```bash
chmod +x download_takeout.py
```

## Authentication and Token Management

### Common Authentication Issues

Google Takeout uses short-lived authentication tokens. If you encounter an authentication error (typically "Got HTML instead of file"), you'll need to refresh the download URL.

### Obtaining a New Authentication Token

1. Open Google Takeout in your browser
2. Ensure you are logged into the correct Google account
3. Navigate to your current export
4. Open browser's Developer Tools (F12)
5. Go to the Network tab
6. Click the "Download" button
7. Find the request to `takeout.google.com/settings/takeout/download`
8. Right-click and choose "Copy as cURL (bash)"

### Updating `curl.txt`

```bash
# Update curl.txt with the new authentication token
cat > curl.txt
# Paste the entire copied cURL command
# Press Ctrl+D when finished
```

### Troubleshooting Authentication

- Verify you're logged into the correct Google account
- Ensure your Google Takeout export is still active
- Check that you have permission to download the files
- If persistent issues occur, try:
  - Logging out and back into Google
  - Clearing browser cookies
  - Regenerating the Google Takeout export

## Usage

### Basic Download

```bash
# Download files from index 1 to 10
./download_takeout.py -s 1 -e 10
```

### Continue Previous Download

```bash
# Resume from last downloaded file
./download_takeout.py --continue
```

### Custom Output Directory

```bash
# Specify a different download location
./download_takeout.py -s 1 -e 10 -d /path/to/output
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-s, --start` | Starting file index | Required |
| `-e, --end` | Ending file index | Required |
| `-d, --directory` | Output directory | `/mnt/f/GoogleTakeout` |
| `--delay` | Seconds between downloads | 5 |
| `--continue` | Resume from last file | False |
| `-h, --help` | Show help message | - |

## Output Format

Files are saved with a timestamp-based naming convention:
```
takeout-YYYYMMDDTHHMMSSZ-NNN.zip
```
Example: `takeout-20250206T053943Z-016.zip`

## Troubleshooting

- Ensure browser cookies and RAPT token are current
- Check network connectivity
- Verify Google Takeout export is complete
- Refresh download URL if authentication fails
- Ensure you have sufficient disk space
- Check internet connection stability

## Contributing

1. Create your feature branch (`git checkout -b feature/AmazingFeature`)
2. Commit changes (`git commit -m 'Add some AmazingFeature'`)
3. Push to branch (`git push origin feature/AmazingFeature`)
4. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

