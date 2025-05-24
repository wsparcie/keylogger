# Advanced Python Keylogger

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Pynput](https://img.shields.io/badge/Pynput-1.7.7-green.svg)](https://pypi.org/project/pynput/)
[![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-0.9.54-red.svg)](https://pypi.org/project/PyAutoGUI/)
[![Tesseract](https://img.shields.io/badge/Tesseract-OCR5.5.0-orange.svg)](https://github.com/tesseract-ocr/tesseract)
[![Status](https://img.shields.io/badge/Status-Beta-yellow.svg)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Last Updated](https://img.shields.io/badge/Last%20Updated-May%202025-brightgreen.svg)](https://github.com/yourusername/keylogger)

A simple Python-based keylogger with monitoring capabilities including keystroke logging, clipboard monitoring, screenshot capture, and OCR-based login form detection.

## Features in Detail

### Monitoring Capabilities
- **Keystroke Logging**: Real-time capture of keyboard inputs
- **Clipboard Tracking**: Monitors clipboard content changes
- **Screenshot Capture**: Automated screen captures on specific events
- **Login Detection**: OCR-based detection of login forms
- **Window Tracking**: Active window title monitoring
- **Email Reporting**: Automated data delivery via SMTP

### Data Collection Features
- **Text Logging**:
  - Raw keystroke data
  - Formatted text content
  - Active window information
  
- **File Management**:
  - Organized data storage
  - Temporary and permanent logs
  - Screenshot management
  - Automated cleanup

### Technical Features
- **Error Handling**:
  - Exception management
  - Graceful failure recovery
  - Detailed error logging
  - Automated retries
  - Network issue management
  - Automatic retry system
  - Graceful data fallbacks

### Output Features
- **Data Export**:
  - Organized log files
  - Screenshot storage
  - Email reporting system
  - Real-time monitoring
  - Automated cleanup routines

## Prerequisites

- Python 3.13
- Tesseract OCR 5.5.0
- Required Python packages:
 ```bash
 pynput==1.7.7
 pyautogui==0.9.54
 pytesseract==0.3.13
 Pillow==10.2.0
 pyperclip==1.9.0
 pywin32==308
 ```

## Installation and Setup

1. Install required packages:
 ```bash
 pip install -r requirements.txt
 ```
2. Install Tesseract OCR if not already present

## Usage

1. Configure email settings in main.py:
```bash
mail_to = "your-email@example.com"
```

2. Run the keylogger:
```bash
python main.py
```

3. Monitor collected data:
   - Real-time logs in program directory
   - Email reports at specified intervals
   - Screenshots in 'screenshots' directory
   - Raw keystroke data in log files
   - Clipboard content in separate logs

## Data Output

### Log Files
- `log.txt`: Real-time keystroke data
- `text.txt`: Formatted text content
- `cboard.txt`: Clipboard monitoring data
- Screenshots: Time-stamped PNG files

### Email Reports
- Configurable intervals
- Compressed log attachments
- Screenshot compilations
- Activity summaries

## License
MIT License - feel free to use and modify as needed.

## Disclaimer
This tool is for educational purposes only. Always obtain proper authorization before monitoring any system or user activity.
