#!/usr/bin/env python3
"""
HackRF Morse Code Transceiver

Main application for transmitting and receiving Morse code via HackRF.
Provides a terminal-based user interface for frequency selection,
text input, and Morse code transmission/reception.
"""

import sys
import time
from morse_code import MorseCodeEncoder, MorseCodeDecoder
from hackrf_interface import HackRFTransmitter, HackRFReceiver


class MorseCodeApp:
    """Main application class for HackRF Morse Code Transceiver"""
    
    def __init__(self):
        self.encoder = MorseCodeEncoder(wpm=20)
        self.decoder = MorseCodeDecoder(wpm=20)
        self.transmitter = None
        self.receiver = None
        self.current_frequency = 433.92e6  # Default: 433.92 MHz
        self.wpm = 20
        self.decoded_buffer = []
        
    def print_header(self):
        """Print application header"""
        print("\n" + "=" * 60)
        print("  HackRF Morse Code Transceiver")
        print("  For use with Mischief Firmware")
        print("=" * 60)
        print()
    
    def print_menu(self):
        """Print main menu"""
        print("\n--- Main Menu ---")
        print("1. Transmit Mode")
        print("2. Receive Mode")
        print("3. Settings")
        print("4. Exit")
        print()
    
    def get_frequency_input(self, current_freq):
        """
        Get frequency input from user
        
        Args:
            current_freq: Current frequency in Hz
            
        Returns:
            New frequency in Hz
        """
        print(f"\nCurrent frequency: {current_freq / 1e6:.3f} MHz")
        print("Enter new frequency (in MHz) or press Enter to keep current:")
        
        try:
            freq_input = input("> ").strip()
            if freq_input:
                freq_mhz = float(freq_input)
                if 1 <= freq_mhz <= 6000:  # HackRF range: 1 MHz to 6 GHz
                    return freq_mhz * 1e6
                else:
                    print("Frequency out of range (1-6000 MHz). Keeping current frequency.")
            return current_freq
        except ValueError:
            print("Invalid input. Keeping current frequency.")
            return current_freq
    
    def transmit_mode(self):
        """Handle transmit mode operations"""
        print("\n=== TRANSMIT MODE ===")
        
        # Get frequency
        self.current_frequency = self.get_frequency_input(self.current_frequency)
        
        # Initialize transmitter
        if not self.transmitter:
            self.transmitter = HackRFTransmitter(
                frequency=self.current_frequency,
                sample_rate=2e6,
                tx_gain=20
            )
            self.transmitter.initialize()
        else:
            self.transmitter.set_frequency(self.current_frequency)
        
        # Get message to transmit
        print("\nEnter message to transmit (or 'back' to return to menu):")
        message = input("> ").strip()
        
        if message.lower() == 'back':
            return
        
        if not message:
            print("No message entered.")
            return
        
        # Encode and transmit
        print(f"\nMessage: {message}")
        morse = self.encoder.encode(message)
        print(f"Morse code: {morse}")
        
        # Get confirmation
        print("\nPress Enter to transmit, or 'c' to cancel:")
        confirm = input("> ").strip().lower()
        
        if confirm == 'c':
            print("Transmission cancelled.")
            return
        
        # Transmit
        timings = self.encoder.encode_to_timings(message)
        print(f"\nTransmitting on {self.current_frequency / 1e6:.3f} MHz...")
        self.transmitter.transmit_morse(timings)
        print("Transmission complete!")
        
        input("\nPress Enter to continue...")
    
    def receive_mode(self):
        """Handle receive mode operations"""
        print("\n=== RECEIVE MODE ===")
        
        # Get frequency
        self.current_frequency = self.get_frequency_input(self.current_frequency)
        
        # Initialize receiver
        if not self.receiver:
            self.receiver = HackRFReceiver(
                frequency=self.current_frequency,
                sample_rate=2e6,
                rx_gain=20
            )
            self.receiver.initialize()
        else:
            self.receiver.set_frequency(self.current_frequency)
        
        print(f"\nListening for Morse code on {self.current_frequency / 1e6:.3f} MHz...")
        print("Words Per Minute (WPM): {}".format(self.wpm))
        print("\nDecoded messages will appear below:")
        print("-" * 60)
        
        # Clear buffer
        self.decoded_buffer = []
        
        # Start receiving
        self.receiver.start_receiving(self._on_morse_detected)
        
        print("\nPress Enter to stop receiving...")
        try:
            input()
        except KeyboardInterrupt:
            pass
        
        # Stop receiving
        self.receiver.stop_receiving()
        print("\nStopped receiving.")
        
        # Show decoded messages
        if self.decoded_buffer:
            print("\n--- Decoded Messages ---")
            for msg in self.decoded_buffer:
                print(f"  {msg}")
        else:
            print("\nNo Morse code detected.")
        
        input("\nPress Enter to continue...")
    
    def _on_morse_detected(self, timings):
        """
        Callback when Morse code is detected
        
        Args:
            timings: List of tuples (state, duration_ms)
        """
        try:
            # Decode timings to text
            decoded_text = self.decoder.decode_from_timings(timings)
            
            if decoded_text and decoded_text.strip():
                print(f"\nDecoded: {decoded_text}")
                self.decoded_buffer.append(decoded_text)
        except Exception as e:
            print(f"Error decoding: {e}")
    
    def settings_mode(self):
        """Handle settings operations"""
        print("\n=== SETTINGS ===")
        print(f"1. Current frequency: {self.current_frequency / 1e6:.3f} MHz")
        print(f"2. Words per minute (WPM): {self.wpm}")
        print("3. Back to main menu")
        print()
        
        choice = input("Select option: ").strip()
        
        if choice == '1':
            self.current_frequency = self.get_frequency_input(self.current_frequency)
        elif choice == '2':
            try:
                wpm_input = input(f"Enter WPM (current: {self.wpm}): ").strip()
                if wpm_input:
                    wpm = int(wpm_input)
                    if 5 <= wpm <= 60:
                        self.wpm = wpm
                        self.encoder = MorseCodeEncoder(wpm=wpm)
                        self.decoder = MorseCodeDecoder(wpm=wpm)
                        print(f"WPM set to {wpm}")
                    else:
                        print("WPM must be between 5 and 60.")
            except ValueError:
                print("Invalid input.")
    
    def cleanup(self):
        """Clean up resources"""
        if self.transmitter:
            self.transmitter.close()
        if self.receiver:
            self.receiver.close()
    
    def run(self):
        """Main application loop"""
        self.print_header()
        
        try:
            while True:
                self.print_menu()
                choice = input("Select option: ").strip()
                
                if choice == '1':
                    self.transmit_mode()
                elif choice == '2':
                    self.receive_mode()
                elif choice == '3':
                    self.settings_mode()
                elif choice == '4':
                    print("\nExiting...")
                    break
                else:
                    print("Invalid option. Please try again.")
        
        except KeyboardInterrupt:
            print("\n\nInterrupted by user.")
        
        finally:
            self.cleanup()
            print("Goodbye!")


def main():
    """Entry point for the application"""
    app = MorseCodeApp()
    app.run()


if __name__ == "__main__":
    main()
