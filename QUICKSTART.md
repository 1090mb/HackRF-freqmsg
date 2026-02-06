# Quick Start Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/1090mb/HackRF-freqmsg.git
cd HackRF-freqmsg

# Install dependencies
pip install -r requirements.txt

# Optional: Install HackRF support
# Ubuntu/Debian:
sudo apt-get install hackrf libhackrf-dev

# macOS:
brew install hackrf
```

## Quick Usage

### Run the Application

```bash
python main.py
```

### Transmit a Message

1. Choose option `1` (Transmit Mode)
2. Enter frequency (e.g., `433.92` for 433.92 MHz)
3. Type your message (e.g., `HELLO WORLD`)
4. Press Enter to transmit

### Receive Messages

1. Choose option `2` (Receive Mode)
2. Enter frequency to monitor (e.g., `433.92`)
3. Decoded messages appear in real-time
4. Press Enter to stop

### Adjust Settings

1. Choose option `3` (Settings)
2. Change frequency or WPM (Words Per Minute)

## Examples

### Example 1: Send SOS

```bash
python example.py
```

### Example 2: Run Demonstration

```bash
python demo.py
```

### Example 3: Run Tests

```bash
python test_morse.py
```

## Morse Code Quick Reference

### Common Messages

| Message | Morse Code |
|---------|------------|
| SOS | `... --- ...` |
| CQ (Calling any station) | `-.-. --.-` |
| OK | `--- -.-` |
| TEST | `- . ... -` |

### Timing (at 20 WPM)
- Dot: 60 ms
- Dash: 180 ms
- Gap between elements: 60 ms
- Gap between letters: 180 ms
- Gap between words: 420 ms

## Frequencies

### Amateur Radio Bands (license required)
- 160m: 1.8 - 2.0 MHz
- 80m: 3.5 - 4.0 MHz
- 40m: 7.0 - 7.3 MHz
- 20m: 14.0 - 14.35 MHz
- 15m: 21.0 - 21.45 MHz
- 10m: 28.0 - 29.7 MHz
- 2m: 144 - 148 MHz
- 70cm: 420 - 450 MHz

### ISM Bands (check local regulations)
- 433.05 - 434.79 MHz (Europe)
- 902 - 928 MHz (Americas)
- 2.4 - 2.5 GHz (Global)

**⚠️ WARNING**: Always ensure you have proper authorization to transmit!

## Troubleshooting

### Cannot import pyhackrf
The application will run in simulation mode. Visual output will be shown instead of actual RF transmission.

### HackRF not detected
- Check USB connection
- Run `hackrf_info` to verify
- Try with sudo: `sudo python main.py`

### No signal received
- Verify antenna is connected
- Check frequency is correct
- Adjust RX gain in settings
- Ensure transmitter is within range

## Support

For issues, see the main [README.md](README.md) or open an issue on GitHub.
