# Google Takeout Batch Downloader

A robust Python script designed to automate the download of large Google Takeout exports split across multiple files.

## Features

- Automatic batch download of multiple Takeout files
- Seamless progress tracking
- Ability to resume downloads from last completed file
- Automatic authentication token refresh
- Comprehensive error handling
- Cross-platform compatibility (tested on Linux/WSL)

## Prerequisites

- Python 3.7+
- Chrome or Chromium browser
- Selenium WebDriver
- Active Google Takeout export

## Installation

### System Dependencies

Before installation, ensure you have the following system packages:

```bash
# Update package lists
sudo apt update

# Install required system packages
sudo apt install -y \
    python3-venv \
    python3-pip \
    chromium-chromedriver \
    chromium-browser
```

### Virtual Environment Setup (Recommended)

1. Create a virtual environment:
```bash
# Create virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

2. Install Python dependencies:
```bash
# Install required Python packages
pip install -r requirements.txt
```

### Configuration

1. Copy the secrets template:
```bash
cp secrets.json.example secrets.json
```

2. Edit `secrets.json` with your Google account details:
- Add your Google email
- Add your Google password
- Configure download preferences

### Make Scripts Executable

```bash
chmod +x download_takeout.py token_retriever.py
```

## Authentication

### Initial Token Retrieval

Before first use, retrieve the initial download token:

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Retrieve download token
python3 token_retriever.py
```

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

## Troubleshooting

### Authentication Issues
- Verify Google account credentials in `secrets.json`
- Ensure two-factor authentication is handled
- Check network connectivity
- Verify Chrome/Chromium browser is installed

### Download Failures
- Confirm sufficient disk space
- Check internet connection stability
- Review `takeout_download.log` for detailed errors

## Security Considerations

- Never commit `secrets.json` to version control
- Use environment variables for sensitive information in production
- Regularly rotate Google account credentials
- Be aware of Google's terms of service

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Disclaimer

This tool is not affiliated with Google. Use responsibly and respect Google's terms of service.

---

**Note**: Always ensure you have the right to download and use the data from Google Takeout.
