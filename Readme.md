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

## Configuration

### 1. Obtain Download URL

1. Open Google Takeout in your browser
2. Navigate to your export
3. Open browser's Developer Tools (F12)
4. Go to Network tab
5. Click "Download"
6. Find request to `takeout.google.com/settings/takeout/download`
7. Right-click and "Copy as cURL (bash)"

### 2. Prepare `curl.txt`

Paste the copied cURL command into `curl.txt` in the project directory.

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

## Contributing

1. Create your feature branch (`git checkout -b feature/AmazingFeature`)
2. Commit changes (`git commit -m 'Add some AmazingFeature'`)
3. Push to branch (`git push origin feature/AmazingFeature`)
4. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

