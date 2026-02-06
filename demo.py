#!/usr/bin/env python3
"""
Demonstration script for HackRF Morse Code Transceiver

This script demonstrates the key features of the application.
"""

from morse_code import MorseCodeEncoder, MorseCodeDecoder
from hackrf_interface import HackRFTransmitter, HackRFReceiver
import time


def demo_header():
    """Print demonstration header"""
    print("\n" + "=" * 70)
    print("  HackRF Morse Code Transceiver - Feature Demonstration")
    print("=" * 70)
    print("\nThis demonstration shows the key features of the application.")
    print("Note: Running in simulation mode (no HackRF hardware required)\n")


def demo_morse_encoding():
    """Demonstrate Morse code encoding"""
    print("\n" + "-" * 70)
    print("FEATURE 1: Text to Morse Code Encoding")
    print("-" * 70)
    
    encoder = MorseCodeEncoder(wpm=20)
    
    messages = [
        "HELLO WORLD",
        "SOS",
        "CQ CQ CQ DE W1AW"
    ]
    
    for msg in messages:
        morse = encoder.encode(msg)
        timings = encoder.encode_to_timings(msg)
        duration = sum(d for _, d in timings) / 1000.0
        
        print(f"\nMessage: '{msg}'")
        print(f"Morse Code: {morse}")
        print(f"Transmission Time: {duration:.2f} seconds at 20 WPM")


def demo_morse_decoding():
    """Demonstrate Morse code decoding"""
    print("\n" + "-" * 70)
    print("FEATURE 2: Morse Code to Text Decoding")
    print("-" * 70)
    
    decoder = MorseCodeDecoder(wpm=20)
    
    morse_messages = [
        (".... . .-.. .-.. --- / .-- --- .-. .-.. -..", "HELLO WORLD"),
        ("... --- ...", "SOS"),
        ("-.-. --.- / -.-. --.- / -.-. --.-", "CQ CQ CQ"),
    ]
    
    for morse, expected in morse_messages:
        decoded = decoder.decode(morse)
        print(f"\nMorse Code: {morse}")
        print(f"Decoded Text: '{decoded}'")
        print(f"Status: {'✓ Correct' if decoded == expected else '✗ Error'}")


def demo_transmission():
    """Demonstrate transmission mode"""
    print("\n" + "-" * 70)
    print("FEATURE 3: Morse Code Transmission")
    print("-" * 70)
    
    print("\nInitializing HackRF transmitter...")
    transmitter = HackRFTransmitter(frequency=433.92e6, sample_rate=2e6, tx_gain=20)
    transmitter.initialize()
    
    print(f"Frequency: 433.92 MHz")
    print(f"Sample Rate: 2 MHz")
    print(f"TX Gain: 20 dB")
    
    message = "HELLO WORLD"
    encoder = MorseCodeEncoder(wpm=20)
    timings = encoder.encode_to_timings(message)
    
    print(f"\nTransmitting message: '{message}'")
    print("Visual representation:")
    transmitter.transmit_morse(timings)
    
    transmitter.close()


def demo_reception():
    """Demonstrate reception mode"""
    print("\n" + "-" * 70)
    print("FEATURE 4: Morse Code Reception")
    print("-" * 70)
    
    print("\nInitializing HackRF receiver...")
    receiver = HackRFReceiver(frequency=433.92e6, sample_rate=2e6, rx_gain=20)
    receiver.initialize()
    
    print(f"Frequency: 433.92 MHz")
    print(f"Sample Rate: 2 MHz")
    print(f"RX Gain: 20 dB")
    print("\nIn actual operation:")
    print("  - Receiver would listen for Morse code signals")
    print("  - Detected signals would be demodulated")
    print("  - Timing patterns would be analyzed")
    print("  - Text would be decoded and displayed in real-time")
    
    receiver.close()


def demo_frequency_selection():
    """Demonstrate frequency selection"""
    print("\n" + "-" * 70)
    print("FEATURE 5: Flexible Frequency Selection")
    print("-" * 70)
    
    frequencies = [
        (433.92e6, "433.92 MHz - ISM Band"),
        (144.0e6, "144.00 MHz - 2m Amateur Band"),
        (446.0e6, "446.00 MHz - PMR446"),
        (28.0e6, "28.00 MHz - 10m Amateur Band"),
    ]
    
    print("\nSupported frequency range: 1 MHz to 6 GHz")
    print("\nExample frequencies:")
    
    for freq, description in frequencies:
        print(f"  • {freq/1e6:.2f} MHz - {description}")
    
    print("\nNote: Always ensure you have proper authorization to transmit!")


def demo_wpm_adjustment():
    """Demonstrate WPM adjustment"""
    print("\n" + "-" * 70)
    print("FEATURE 6: Adjustable Words Per Minute (WPM)")
    print("-" * 70)
    
    message = "HELLO"
    
    print(f"\nMessage: '{message}'")
    print("\nTransmission time at different speeds:")
    
    for wpm in [5, 10, 20, 30, 40]:
        encoder = MorseCodeEncoder(wpm=wpm)
        timings = encoder.encode_to_timings(message)
        duration = sum(d for _, d in timings) / 1000.0
        
        print(f"  • {wpm:2d} WPM: {duration:.2f} seconds")


def demo_special_features():
    """Demonstrate special features"""
    print("\n" + "-" * 70)
    print("FEATURE 7: Additional Capabilities")
    print("-" * 70)
    
    print("\n✓ Support for all International Morse Code characters:")
    print("  - Letters A-Z")
    print("  - Numbers 0-9")
    print("  - Punctuation (. , ? ' ! / ( ) & : ; = + - _ \" $ @)")
    
    print("\n✓ Simulation mode for development/testing:")
    print("  - Works without HackRF hardware")
    print("  - Visual representation of transmissions")
    print("  - Full encoding/decoding functionality")
    
    print("\n✓ User-friendly terminal interface:")
    print("  - Simple menu navigation")
    print("  - Clear mode separation (Transmit/Receive)")
    print("  - Adjustable settings")
    
    print("\n✓ Robust error handling:")
    print("  - Input validation")
    print("  - Frequency range checking")
    print("  - Graceful hardware failures")


def main():
    """Run all demonstrations"""
    demo_header()
    
    try:
        demo_morse_encoding()
        time.sleep(1)
        
        demo_morse_decoding()
        time.sleep(1)
        
        demo_transmission()
        time.sleep(1)
        
        demo_reception()
        time.sleep(1)
        
        demo_frequency_selection()
        time.sleep(1)
        
        demo_wpm_adjustment()
        time.sleep(1)
        
        demo_special_features()
        
        print("\n" + "=" * 70)
        print("  Demonstration Complete!")
        print("=" * 70)
        print("\nTo run the actual application, execute:")
        print("  python main.py")
        print("\nFor more information, see README.md")
        print()
        
    except Exception as e:
        print(f"\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
