# File-integratity-monitor

A lightweight Python-based file integrity monitoring tool that tracks changes to specified files using SHA-256 hashing.
Overview
This tool monitors files for modifications by computing and comparing cryptographic hashes. It detects when files are created or modified, maintaining a log of all changes with timestamps.
Features

SHA-256 Hashing: Secure file integrity verification
Change Detection: Identifies newly created and modified files
Activity Logging: Timestamped log of all file changes
Pattern Matching: Supports glob patterns for file selection
Configurable: Customizable file paths via command-line arguments

Installation
bashgit clone https://github.com/yourusername/file-integrity-monitor.git
cd file-integrity-monitor


No external dependencies required - uses Python standard library only.

#Usage

### Basic Usage

1. Create a `requested.txt` file listing the files/patterns to monitor:

/path/to/important/file.txt
/path/to/config/*.conf

Run the monitor:

bashpython main.py --cli
Command-Line Options
bashpython main.py --cli [OPTIONS]
Options:

--requested FILE - File containing list of files to monitor (default: requested.txt)
--active FILE - File storing known file hashes (default: activefile.txt)
--temp FILE - Temporary file for updates (default: activetemp.txt)
--log FILE - Log file for changes (default: fimlog.txt)
--cli - Enable CLI mode (required to run)

Example
bashpython main.py --cli --requested my_files.txt --log changes.log


#How It Works

1. Reads the list of files to monitor from the requested file
2. Computes SHA-256 hash for each file
3. Compares against previously stored hashes
4. Logs any new or modified files with timestamps
5. Updates the active hash database

## Output

The tool generates:
- **Active File** (`activefile.txt`): Current state of monitored files and their hashes
- **Log File** (`fimlog.txt`): Chronological record of all detected changes

Log entries include:

[CREATED] 2024-12-02 10:30:45: /path/to/file.txt was created with hash abc123...
[MODIFIED] 2024-12-02 11:15:20: /path/to/file.txt was modified. Old hash: abc123..., New hash: def456...
Use Cases

Monitor critical system files for unauthorized changes
Track configuration file modifications
Detect tampering in sensitive directories
Audit file changes in production environments

Requirements

Python 3.8+
No external dependencies

License
MIT License - feel free to use and modify as needed.
Contributing
Contributions welcome! Please open an issue or submit a pull request.Claude can make mistakes. Please double-check responses.
