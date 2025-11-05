# MAC Clipboard Manager

A lightweight macOS menu-bar clipboard history manager. Monitors the clipboard, keeps the most recent 20 entries, supports bookmarks, saves history to disk, and provides quick one-click re-copy with notifications.

## Features

- Stores up to 20 recent clipboard items
- Persistent storage in `clipboard.json`
- Menu bar quick access (rumps)
- Copy notifications
- Bookmark items for quick access
- Clear history and Quit controls
- Automatic startup via Automator (optional)

## Requirements

- macOS
- Python 3.8+
- Packages:
  - rumps
  - pyperclip

Install packages with:

```bash
pip install -r requirements.txt
```

## Installation

1. Clone the repo:

```bash
git clone https://github.com/yourusername/MAC-Clipboard-Manager.git
cd MAC-Clipboard-Manager
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

With your virtualenv activated:

```bash
python clipboard_manager.py
```

A menu-bar icon (📋) will appear. Click it to view bookmarks and clipboard history.

## Project Structure

```
MAC-Clipboard-Manager/
├── clipboard_manager.py     # Main application
├── requirements.txt         # Python dependencies
├── clipboard.json           # Saved history (created at runtime)
├── venv/                    # Virtual environment (not committed)
└── README.md                # This file
```

## How it works (short)

- monitor_clipboard polls the system clipboard and records changes
- The most recent unique items are stored in memory and persisted to `clipboard.json`
- Menu items let you re-copy historical entries or bookmark them
- Bookmarked items appear at the top section of the menu

## Automator (Auto-start) — example

Create an Automator Application that runs this script to start at login:

Automator → New → Application → Run Shell Script:

```bash
#!/bin/bash
cd /path/to/MAC-Clipboard-Manager
source venv/bin/activate
/path/to/MAC-Clipboard-Manager/venv/bin/python3 clipboard_manager.py
```

Save the Automator app, then add it to System Preferences → Users & Groups → Login Items.

## Troubleshooting

- No menu icon: ensure `rumps` is installed in the active Python environment.
- Clipboard not updating: check that nothing is interfering with the clipboard and that the script is running.
- Permission prompts: allow any needed permissions in System Settings → Privacy & Security if macOS requests them.

## Development

- Create feature branches, add tests, and open a PR.
- Run the app locally while developing; use logging/print for quick debugging.

## Contributing

1. Fork
2. Create a branch
3. Commit and push
4. Open a Pull Request
