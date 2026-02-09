# NetRe

NetRe is a cross-platform Python utility that allows you to retrieve Wi-Fi network profiles and passwords from your system.

## Features
- **Cross-Platform**: Supports Windows, macOS, and Linux.
- **Export**: Export retrieved passwords to JSON or CSV formats.
- **Privacy**: Option to mask passwords in the terminal output.
- **CLI Interface**: Robust command-line interface for better user experience.

## How to use

### Requirements
- Python 3.x
- Administrative/Sudo privileges (required to access system Wi-Fi credentials).

### Execution
1. Clone the repository:
   ```bash
   git clone https://github.com/devgenix/NetRe.git
   cd NetRe
   ```
2. Run the script:
   ```bash
   # Basic run
   python3 NetRe.py

   # With masking and export to JSON
   python3 NetRe.py --mask --export json
   ```

### Command Line Options
- `--mask`: Hide passwords in the terminal output.
- `--export [json|csv]`: Export results to `wifi_passwords.json` or `wifi_passwords.csv`.

## Platform Specific Notes
- **Windows**: Uses `netsh`.
- **macOS**: Uses `networksetup` and `security`. Will trigger a Keychain authorization prompt.
- **Linux**: Uses `nmcli`. Requires `NetworkManager` to be installed and running.

## Contributing
We welcome contributions! Please refer to the contribution guidelines for more details.
