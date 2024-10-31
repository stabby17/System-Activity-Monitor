# System-Activity-Monitor

Python-based system monitoring tool that captures keyboard input and periodic screenshots.

## Features

- Keyboard activity logging with timestamps
- Configurable screenshot intervals
- Cross-platform support (Windows/Linux)
- Simple setup and usage

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/System-Activity-Monitor.git
cd System-Activity-Monitor
```

2. Install dependencies:
```bash
# For Windows
pip install keyboard pillow

# For Linux
pip install keyboard pillow pyscreenshot
sudo apt-get install python3-tk python3-dev scrot  # Required for screenshots
```

## Usage

Basic usage with default settings (5-second screenshot interval):
```bash
python monitor.py
```

Custom screenshot interval:
```bash
python monitor.py -i 60  # Takes screenshots every 60 seconds
```

Command line arguments:
- `-i` or `--interval`: Screenshot interval in seconds (default: 5)

## Output

The tool creates:
- `system_activity.txt`: Log file containing keyboard events and timestamps
- `activity_snapshots/`: Directory containing screenshots named with timestamps

## Requirements

- Python 3.x
- See requirements.txt for Python packages

## Contributing

Feel free to fork, submit PRs, or suggest improvements.

## License

MIT License
