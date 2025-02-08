# Google Takeout Batch Downloader

## Overview

A comprehensive, secure Python solution for automating the download of large Google Takeout exports across multiple files.

## Features

- Batch download of multiple Takeout files
- Secure credential management
- Automatic authentication token refresh
- Detailed logging and error handling
- Two-factor authentication support
- Resumable downloads

## System Requirements

### Hardware & Software
- Python 3.8+
- Chrome or Chromium browser
- Selenium WebDriver
- Active Google Takeout export

### Required System Packages
```bash
sudo apt update
sudo apt install -y \
    python3-venv \
    python3-pip \
    chromium-chromedriver \
    chromium-browser \
    python3-selenium
```

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/cschladetsch/google-takeout-downloader.git
cd google-takeout-downloader
```

### 2. Create Virtual Environment
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

## Configuration

### Initial Setup
```bash
# Run configuration wizard
python configure_secrets.py
```

The configuration wizard will:
- Validate existing configuration
- Securely prompt for missing information
- Store credentials using system keyring
- Support optional two-factor authentication

### Configuration Options
- Google account email
- Secure password storage
- Two-factor authentication secret (optional)
- Download output directory
- Download delay between files
- Logging preferences

## Usage

### Basic Download
```bash
# Activate virtual environment
source venv/bin/activate

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

## Advanced Features

### Token Retrieval
```bash
# Manually refresh download token
python token_retriever.py
```

### Logging
- Logs saved to `takeout_download.log`
- Configurable log levels in `secrets.json`

## Troubleshooting

### Common Issues
- Verify Google account credentials
- Check network connectivity
- Ensure sufficient disk space
- Update Chrome/Chromium WebDriver

### Authentication Failures
- Two-factor authentication support
- Automatic token refresh
- Detailed error logging

## Security Considerations

- Credentials stored securely
- No direct storage of plain-text passwords
- Support for system keyring
- Configurable logging

## Testing

### Run Tests
```bash
# Activate virtual environment
source venv/bin/activate

# Run tests
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for details.

## Disclaimer

This tool is not affiliated with Google. Use responsibly and respect Google's terms of service.

