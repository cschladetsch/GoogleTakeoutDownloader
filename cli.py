"""Command line interface for Google Takeout downloader."""

import argparse
from .downloader import TakeoutDownloader

def parse_arguments() -> argparse.Namespace:
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
                        help='Ending index for download sequence')
    
    parser.add_argument('-d', '--directory', 
                        type=str, 
                        default='/mnt/f/GoogleTakeout',
                        help='Output directory (default: /mnt/f/GoogleTakeout)')
    
    parser.add_argument('--delay', 
                        type=int, 
                        default=5,
                        help='Delay in seconds between downloads (default: 5)')
    
    parser.add_argument('--job-id',
                        type=str,
                        help='Google Takeout job ID')
                        
    parser.add_argument('--email',
                        type=str,
                        help='Google account email')
    
    args = parser.parse_args()
    
    # Handle continue flag
    if args.continue_flag:
        args.start = TakeoutDownloader.find_last_downloaded_index(args.directory) + 1
        if not args.end:
            args.end = 277
        print(f"Continuing from index {args.start}")
    
    # Validate arguments
    if args.end is None and not args.continue_flag:
        parser.error("End index is required when not using --continue")
    
    if args.end is not None and args.end > 277:
        parser.error("End index cannot exceed 277")
    
    if args.start > args.end:
        parser.error("Start index must be less than or equal to end index")
    
    if args.delay < 0:
        parser.error("Delay must be non-negative")
    
    if args.start < 1:
        parser.error("Start index must be at least 1")
        
    return args

def main() -> None:
    """Main entry point for the command line interface."""
    args = parse_arguments()
    
    # Create downloader instance
    downloader = TakeoutDownloader(
        job_id=args.job_id or "aad05205-2695-41f5-a4d7-b92d9a095d5e",
        email=args.email or "christian.schladetsch@gmail.com"
    )
    
    # Download files
    downloader.download_range(
        start=args.start,
        end=args.end,
        output_dir=args.directory,
        delay=args.delay
    )

if __name__ == "__main__":
    main()
