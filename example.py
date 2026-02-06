#!/usr/bin/env python3
"""
Example usage script showing transmit and receive functionality
"""

from morse_code import MorseCodeEncoder, MorseCodeDecoder
from hackrf_interface import HackRFTransmitter

def example_transmit():
    """Example of transmitting Morse code"""
    print("=" * 60)
    print("EXAMPLE: Transmitting Morse Code")
    print("=" * 60)
    
    # Create encoder and transmitter
    encoder = MorseCodeEncoder(wpm=20)
    transmitter = HackRFTransmitter(frequency=433.92e6, tx_gain=20)
    transmitter.initialize()
    
    # Message to send
    message = "HELLO WORLD"
    
    print(f"\nMessage: {message}")
    print(f"Frequency: 433.92 MHz")
    
    # Encode to Morse
    morse = encoder.encode(message)
    print(f"Morse Code: {morse}")
    
    # Convert to timing sequence
    timings = encoder.encode_to_timings(message)
    duration = sum(d for _, d in timings) / 1000.0
    print(f"Duration: {duration:.2f} seconds")
    
    # Transmit
    print("\nTransmitting...")
    transmitter.transmit_morse(timings)
    print("Transmission complete!")
    
    transmitter.close()


def example_decode():
    """Example of decoding Morse code"""
    print("\n" + "=" * 60)
    print("EXAMPLE: Decoding Morse Code")
    print("=" * 60)
    
    decoder = MorseCodeDecoder(wpm=20)
    
    # Example morse code
    morse = "... --- ..."
    print(f"\nMorse Code: {morse}")
    
    decoded = decoder.decode(morse)
    print(f"Decoded: {decoded}")


if __name__ == "__main__":
    example_transmit()
    example_decode()
