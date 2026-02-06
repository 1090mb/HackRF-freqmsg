# HackRF Morse Code Transceiver

A messaging application for HackRF with Mischief firmware that enables Morse code transmission and reception.

## Features

### Receive Mode
- **Frequency Selection**: Choose any frequency within HackRF's range (1 MHz - 6 GHz)
- **Morse Code Detection**: Automatically detects and decodes Morse code signals
- **Real-time Display**: Shows decoded text on screen as Morse code is received
- **Adjustable Speed**: Configure Words Per Minute (WPM) for accurate decoding

### Transmit Mode
- **Frequency Selection**: Choose transmission frequency
- **Text Input**: Enter plain text messages
- **Automatic Encoding**: Converts text to Morse code automatically
- **CW Transmission**: Transmits as Continuous Wave (CW) Morse code

## Requirements

### Hardware
- HackRF One with Mischief firmware installed
- Appropriate antenna for chosen frequency
- USB connection to host computer

### Software
- Python 3.7 or higher
- NumPy
- HackRF library (libhackrf or pyhackrf)

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/1090mb/HackRF-freqmsg.git
cd HackRF-freqmsg
```

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

3. **Install HackRF library**:

   On Ubuntu/Debian:
   ```bash
   sudo apt-get install hackrf libhackrf-dev
   ```

   On macOS:
   ```bash
   brew install hackrf
   ```

   On Windows:
   - Download and install HackRF tools from [Great Scott Gadgets](https://github.com/greatscottgadgets/hackrf/releases)

4. **Install Python HackRF bindings** (optional, for hardware support):
   ```bash
   # If available via pip
   pip install pyhackrf
   
   # Or build from source
   git clone https://github.com/dressel/pyhackrf.git
   cd pyhackrf
   python setup.py install
   ```

## Usage

### Running the Application

```bash
python main.py
```

Or make it executable:
```bash
chmod +x main.py
./main.py
```

### Main Menu

The application presents a simple terminal-based interface:

```
=============================================================
  HackRF Morse Code Transceiver
  For use with Mischief Firmware
=============================================================

--- Main Menu ---
1. Transmit Mode
2. Receive Mode
3. Settings
4. Exit
```

### Transmit Mode

1. Select option **1** from the main menu
2. Enter desired frequency in MHz (e.g., `433.92` for 433.92 MHz)
3. Type your message (e.g., `HELLO WORLD`)
4. Press Enter to confirm and transmit
5. The message will be encoded to Morse code and transmitted

**Example**:
```
=== TRANSMIT MODE ===
Current frequency: 433.920 MHz
Enter new frequency (in MHz) or press Enter to keep current:
> 433.92

Enter message to transmit (or 'back' to return to menu):
> HELLO WORLD

Message: HELLO WORLD
Morse code: .... . .-.. .-.. --- / .-- --- .-. .-.. -..

Press Enter to transmit, or 'c' to cancel:
> 

Transmitting on 433.920 MHz...
████ █ ████ ████ ███     ███ ███ ██ ████ ███
Transmission complete!
```

### Receive Mode

1. Select option **2** from the main menu
2. Enter desired frequency in MHz to monitor
3. The application will listen for Morse code signals
4. Decoded text appears on screen in real-time
5. Press Enter to stop receiving

**Example**:
```
=== RECEIVE MODE ===
Current frequency: 433.920 MHz
Enter new frequency (in MHz) or press Enter to keep current:
> 433.92

Listening for Morse code on 433.920 MHz...
Words Per Minute (WPM): 20

Decoded messages will appear below:
------------------------------------------------------------

Decoded: HELLO WORLD
Decoded: TEST MESSAGE

Press Enter to stop receiving...
```

### Settings

Adjust application settings:
- **Frequency**: Set default frequency
- **WPM**: Set Words Per Minute (5-60) for Morse code timing

## Morse Code Reference

### International Morse Code

| Character | Morse Code | Character | Morse Code |
|-----------|------------|-----------|------------|
| A | .-    | N | -.    |
| B | -... | O | ---   |
| C | -.-. | P | .--.  |
| D | -..  | Q | --.-  |
| E | .    | R | .-.   |
| F | ..-. | S | ...   |
| G | --.  | T | -     |
| H | .... | U | ..-   |
| I | ..   | V | ...-  |
| J | .--- | W | .--   |
| K | -.-  | X | -..-  |
| L | .-.. | Y | -.--  |
| M | --   | Z | --..  |

| Number | Morse Code | Punctuation | Morse Code |
|--------|------------|-------------|------------|
| 0 | ----- | . (period)  | .-.-.- |
| 1 | .---- | , (comma)   | --..-- |
| 2 | ..--- | ? (question)| ..--.. |
| 3 | ...-- | / (slash)   | -..-.  |
| 4 | ....- | - (hyphen)  | -....- |
| 5 | ..... | ( | -.--.  |
| 6 | -.... | ) | -.--.- |
| 7 | --... | & | .-...  |
| 8 | ---.. | @ | .--.-. |
| 9 | ----. | = | -...-  |

### Timing
- **Dot**: 1 unit
- **Dash**: 3 units
- **Gap between elements**: 1 unit
- **Gap between letters**: 3 units
- **Gap between words**: 7 units

At 20 WPM:
- 1 unit = 60 milliseconds
- Dot = 60 ms
- Dash = 180 ms

## Technical Details

### Architecture

The application consists of three main modules:

1. **morse_code.py**: Morse code encoding and decoding logic
   - `MorseCodeEncoder`: Converts text to Morse code and timing sequences
   - `MorseCodeDecoder`: Converts Morse code back to text

2. **hackrf_interface.py**: HackRF hardware interface
   - `HackRFTransmitter`: Handles signal transmission
   - `HackRFReceiver`: Handles signal reception and detection

3. **main.py**: User interface and application control
   - Menu system
   - User input handling
   - Mode coordination

### Signal Generation

Transmissions use **Continuous Wave (CW)** modulation:
- On-Off Keying (OOK) with carrier at center frequency
- Dots and dashes represented by carrier presence/absence
- Clean transitions for reliable reception

### Signal Detection

Reception uses envelope detection:
- Amplitude-based threshold detection
- Timing analysis to distinguish dots from dashes
- Adaptive to varying signal strengths

## Simulation Mode

If HackRF hardware is not available, the application runs in **simulation mode**:
- Visual representation of transmissions (console output)
- No actual RF transmission occurs
- Useful for testing and development

## Legal Notice

⚠️ **Important**: 
- Ensure you have proper authorization to transmit on chosen frequencies
- Comply with local radio regulations and licensing requirements
- Unauthorized transmission may be illegal in your jurisdiction
- Use responsibly and ethically

## Troubleshooting

### HackRF not detected
- Ensure HackRF is connected via USB
- Check that drivers are installed correctly
- Try running with sudo/administrator privileges
- Verify with `hackrf_info` command

### No signal detected in receive mode
- Check antenna is properly connected
- Verify correct frequency is set
- Adjust RX gain in settings
- Ensure transmitter is within range
- Check for interference

### Import errors
- Verify all dependencies are installed
- Check Python version (3.7+)
- Try reinstalling requirements

## Future Enhancements

- [ ] GUI interface with spectrum display
- [ ] Adjustable TX/RX gain controls
- [ ] Signal strength indicator
- [ ] Message logging and history
- [ ] Custom Morse code speed per transmission
- [ ] Support for prosigns (procedural signals)
- [ ] Waterfall display
- [ ] Multiple frequency monitoring

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

See LICENSE file for details.

## Acknowledgments

- HackRF project by Great Scott Gadgets
- Mischief/Havoc firmware community
- International Morse Code standards

## Support

For issues and questions:
- Open an issue on GitHub
- Check HackRF documentation at https://hackrf.readthedocs.io/
- Visit Great Scott Gadgets forums

---

**73!** (Best regards in Morse code operator lingo)
