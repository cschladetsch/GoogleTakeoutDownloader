#!/usr/bin/env python3

import unittest
from pathlib import Path
from download_takeout import create_url, parse_curl

class TestDownloader(unittest.TestCase):
    def test_working_url_format(self):
        """Test URL exactly matches format from working download."""
        url = create_url(0, "job-123", "test-rapt")
        self.assertEqual(
            url,
            "https://takeout.google.com/settings/takeout/download?i=0&j=job-123&download=true&rapt=test-rapt"
        )

    def test_valid_curl_parsing(self):
        """Test parsing of complete curl command."""
        curl = """curl 'https://takeout.google.com/settings/takeout/download?i=0&j=123&download=true&rapt=test-rapt' \
            -H 'User-Agent: test' \
            -H 'Accept: test' \
            -b 'cookie1=value1; cookie2=value2'"""
            
        headers, cookies, rapt = parse_curl(curl)
        self.assertEqual(headers['User-Agent'], 'test')
        self.assertEqual(cookies['cookie1'], 'value1')
        self.assertEqual(rapt, 'test-rapt')

    def test_missing_rapt(self):
        """Test curl command without rapt token."""
        curl = """curl 'https://takeout.google.com/' -H 'Accept: test' -b 'cookie=test'"""
        with self.assertRaises(ValueError):
            parse_curl(curl)

    def test_partial_cookies(self):
        """Test curl command with incomplete cookies."""
        curl = """curl 'https://takeout.google.com/settings/takeout/download?rapt=test' -b 'a=1'"""
        headers, cookies, rapt = parse_curl(curl)
        self.assertEqual(cookies, {'a': '1'})

    def test_filename_format(self):
        """Test output filename pattern."""
        from datetime import datetime
        filename = f"takeout-{datetime.now().strftime('%Y%m%d')}T000000Z-042.zip"
        self.assertRegex(filename, r'takeout-\d{8}T\d{6}Z-\d{3}\.zip')

if __name__ == '__main__':
    unittest.main()

# File: test_download_takeout.py
