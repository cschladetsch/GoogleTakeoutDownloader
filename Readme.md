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

### Configure Secrets

1. Copy the `secrets.json.example` to `secrets.json`
```bash
cp secrets.json.example secrets.json
```

2. Edit `secrets.json` with your configuration:
- Add your Google account details
- Configure download preferences
- Set up optional proxy settings if needed

### Make Script Executable

```bash
chmod +x download_takeout.py
```

## Secrets Configuration

The `secrets.json` file contains several configuration sections:

### Google Takeout Settings
- `email`: Your Google account email
- `password`: Your Google account password
- `max_files`: Maximum number of files to download
- `output_directory`: Where downloaded files will be saved
- `download_delay`: Seconds between downloads

### Authentication
- `rapt_token`: Current authentication token
- `job_id`: Google Takeout job identifier
- `last_downloaded_index`: Tracking for resume functionality

### Advanced Options
- Proxy configuration
- Logging settings
- Optional credential encryption

### Security Recommendations
- Do NOT commit `secrets.json` to version control
- Use environment variables or secure credential management in production
- Consider encrypting sensitive information

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

## Troubleshooting

- Ensure `secrets.json` is correctly configured
- Verify browser cookies and RAPT token are current
- Check network connectivity
- Ensure you have sufficient disk space
- Confirm internet connection stability

## Security Notes

- Keep `secrets.json` private
- Use `.gitignore` to prevent accidental commits
- Consider using environment variables for sensitive data
- Implement credential rotation and secure storage

## Contributing

1. Create your feature branch (`git checkout -b feature/AmazingFeature`)
2. Commit changes (`git commit -m 'Add some AmazingFeature'`)
3. Push to branch (`git push origin feature/AmazingFeature`)
4. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/google-takeout-downloader](https://github.com/yourusername/google-takeout-downloader)

---

**Disclaimer**: This tool is not affiliated with Google. Use responsibly and respect Google's terms of service.
