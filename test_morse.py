#!/usr/bin/env python3
"""
Test script for HackRF Morse Code Transceiver

This script tests the core functionality without requiring HackRF hardware.
"""

import sys
from morse_code import MorseCodeEncoder, MorseCodeDecoder


def test_morse_encoding():
    """Test Morse code encoding"""
    print("=" * 60)
    print("Testing Morse Code Encoding")
    print("=" * 60)
    
    encoder = MorseCodeEncoder(wpm=20)
    
    test_cases = [
        "HELLO WORLD",
        "SOS",
        "TEST 123",
        "CQ CQ CQ",
        "MORSE CODE"
    ]
    
    for text in test_cases:
        morse = encoder.encode(text)
        print(f"\nText: {text}")
        print(f"Morse: {morse}")
        
        # Get timings
        timings = encoder.encode_to_timings(text)
        total_time = sum(duration for _, duration in timings) / 1000.0
        print(f"Duration: {total_time:.2f} seconds")


def test_morse_decoding():
    """Test Morse code decoding"""
    print("\n" + "=" * 60)
    print("Testing Morse Code Decoding")
    print("=" * 60)
    
    decoder = MorseCodeDecoder(wpm=20)
    
    test_cases = [
        (".... . .-.. .-.. --- / .-- --- .-. .-.. -..", "HELLO WORLD"),
        ("... --- ...", "SOS"),
        ("- . ... - / .---- ..--- ...--", "TEST 123"),
        ("-.-. --.- / -.-. --.- / -.-. --.-", "CQ CQ CQ"),
    ]
    
    for morse, expected in test_cases:
        decoded = decoder.decode(morse)
        status = "✓" if decoded == expected else "✗"
        print(f"\n{status} Morse: {morse}")
        print(f"  Decoded: {decoded}")
        print(f"  Expected: {expected}")


def test_round_trip():
    """Test encoding and decoding round trip"""
    print("\n" + "=" * 60)
    print("Testing Round Trip (Encode → Decode)")
    print("=" * 60)
    
    encoder = MorseCodeEncoder(wpm=20)
    decoder = MorseCodeDecoder(wpm=20)
    
    test_texts = [
        "HELLO WORLD",
        "TESTING 123",
        "THE QUICK BROWN FOX",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "0123456789"
    ]
    
    for text in test_texts:
        morse = encoder.encode(text)
        decoded = decoder.decode(morse)
        status = "✓" if decoded == text else "✗"
        print(f"\n{status} Original: {text}")
        print(f"  Decoded: {decoded}")


def test_timing_decoding():
    """Test decoding from timing sequences"""
    print("\n" + "=" * 60)
    print("Testing Timing-Based Decoding")
    print("=" * 60)
    
    encoder = MorseCodeEncoder(wpm=20)
    decoder = MorseCodeDecoder(wpm=20)
    
    test_texts = [
        "SOS",
        "HELLO",
        "TEST 123"
    ]
    
    for text in test_texts:
        # Encode to timings
        timings = encoder.encode_to_timings(text)
        
        # Decode from timings
        decoded = decoder.decode_from_timings(timings)
        
        status = "✓" if decoded == text else "✗"
        print(f"\n{status} Original: {text}")
        print(f"  Decoded: {decoded}")
        print(f"  Timing count: {len(timings)}")


def test_special_characters():
    """Test special characters and punctuation"""
    print("\n" + "=" * 60)
    print("Testing Special Characters")
    print("=" * 60)
    
    encoder = MorseCodeEncoder(wpm=20)
    decoder = MorseCodeDecoder(wpm=20)
    
    test_cases = [
        "HELLO, WORLD!",
        "TEST?",
        "3.14",
        "A=B+C",
        "TEST@EXAMPLE.COM"
    ]
    
    for text in test_cases:
        morse = encoder.encode(text)
        decoded = decoder.decode(morse)
        print(f"\nOriginal: {text}")
        print(f"Morse: {morse}")
        print(f"Decoded: {decoded}")


def test_wpm_speeds():
    """Test different WPM speeds"""
    print("\n" + "=" * 60)
    print("Testing Different WPM Speeds")
    print("=" * 60)
    
    text = "TEST"
    
    for wpm in [5, 10, 20, 30, 40]:
        encoder = MorseCodeEncoder(wpm=wpm)
        timings = encoder.encode_to_timings(text)
        total_time = sum(duration for _, duration in timings) / 1000.0
        
        print(f"\nWPM: {wpm}")
        print(f"  Dot duration: {encoder.dot_duration:.1f} ms")
        print(f"  Total time for '{text}': {total_time:.2f} seconds")


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("  HackRF Morse Code Transceiver - Test Suite")
    print("=" * 60)
    
    try:
        test_morse_encoding()
        test_morse_decoding()
        test_round_trip()
        test_timing_decoding()
        test_special_characters()
        test_wpm_speeds()
        
        print("\n" + "=" * 60)
        print("  All Tests Completed!")
        print("=" * 60)
        print()
        
    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
