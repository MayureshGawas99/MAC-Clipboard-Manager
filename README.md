# MAC Clipboard Manager

A lightweight, efficient clipboard history manager for macOS that lives in your menu bar. Keep track of your clipboard history and quickly access previously copied items.

## Features

- Stores up to 20 recent clipboard items
- Persistent storage across app restarts
- Menu bar quick access
- Copy notifications
- Clean and simple interface
- Automatic startup option

## Requirements

- macOS
- Python 3.x
- Required packages:
  - `rumps`
  - `pyperclip`

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/MAC-Clipboard-Manager.git
cd MAC-Clipboard-Manager
```

2. Set up virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Project Structure

```
MAC-Clipboard-Manager/
├── clipboard_manager.py     # Main application file
├── requirements.txt        # Python dependencies
├── clipboard.json         # Clipboard history storage
├── venv/                 # Virtual environment
└── README.md            # Documentation
```

## How It Works

The application:

- Monitors your clipboard for changes
- Stores up to 20 most recent items
- Saves history to `clipboard.json`
- Shows notifications when items are copied
- Provides quick access through menu bar icon

## Features Explained

1. **Clipboard Monitoring**: Continuously monitors clipboard changes
2. **History Management**: Maintains ordered list of recent items
3. **Persistent Storage**: Saves history to JSON file
4. **Menu Bar Integration**: Easy access through macOS menu bar
5. **Quick Copy**: One-click to copy any historical item

## Auto-Start Configuration

### Using Automator

1. Open Automator
2. Create new "Application"
3. Add "Run Shell Script" action
4. Enter this script:

```bash
#!/bin/bash
cd /path/to/MAC-Clipboard-Manager
source venv/bin/activate
/path/to/MAC-Clipboard-Manager/venv/bin/python3 clipboard_manager.py
```

5. Save as "ClipboardManagerStarter" to Applications

### Enable at Login

1. System Preferences → Users & Groups
2. Select your user
3. Login Items tab
4. Click '+'
5. Add "ClipboardManagerStarter"

## Usage

- Click menu bar icon to view history
- Select any item to copy it
- "Clear History" removes all items
- "Quit" exits application

## Development

1. Clone repository
2. Create virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS
```

3. Install dev dependencies:

```bash
pip install -r requirements.txt
```

4. Run application:

```bash
python clipboard_manager.py
```

## Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## Troubleshooting

- If app doesn't start: Check Python path in Automator script
- If no menu bar icon: Verify `rumps` installation
- If clipboard not updating: Check permissions
