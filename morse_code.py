"""
Morse Code Encoder and Decoder Module

This module provides functionality to encode text to Morse code
and decode Morse code patterns back to text.
"""

# International Morse Code mapping
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--',
    '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...',
    ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-',
    '"': '.-..-.', '$': '...-..-', '@': '.--.-.', ' ': '/'
}

# Reverse mapping for decoding
MORSE_CODE_REVERSE = {v: k for k, v in MORSE_CODE_DICT.items()}


class MorseCodeEncoder:
    """Encodes text messages to Morse code"""
    
    def __init__(self, wpm=20):
        """
        Initialize encoder with specified words per minute
        
        Args:
            wpm: Words per minute (default: 20)
        """
        self.wpm = wpm
        # Calculate timing units in milliseconds
        # Standard word "PARIS" = 50 dots, timing calculation based on this
        self.dot_duration = 1200.0 / wpm  # milliseconds
        self.dash_duration = 3 * self.dot_duration
        self.element_gap = self.dot_duration
        self.letter_gap = 3 * self.dot_duration
        self.word_gap = 7 * self.dot_duration
    
    def encode(self, text):
        """
        Encode text to Morse code
        
        Args:
            text: String to encode
            
        Returns:
            String of Morse code (dots and dashes)
        """
        morse = []
        for char in text.upper():
            if char in MORSE_CODE_DICT:
                morse.append(MORSE_CODE_DICT[char])
            elif char == ' ':
                morse.append('/')
        return ' '.join(morse)
    
    def encode_to_timings(self, text):
        """
        Encode text to timing sequence for transmission
        
        Args:
            text: String to encode
            
        Returns:
            List of tuples (state, duration_ms) where state is True for ON, False for OFF
        """
        timings = []
        morse_text = text.upper()
        
        for i, char in enumerate(morse_text):
            if char == ' ':
                # Word space (already have letter space from previous char)
                # Total word gap is 7 units, we already have 3 from letter gap
                timings.append((False, self.word_gap - self.letter_gap))
                continue
                
            if char not in MORSE_CODE_DICT:
                continue
                
            morse_char = MORSE_CODE_DICT[char]
            
            for j, symbol in enumerate(morse_char):
                if symbol == '.':
                    timings.append((True, self.dot_duration))
                elif symbol == '-':
                    timings.append((True, self.dash_duration))
                elif symbol == '/':
                    # Word space
                    timings.append((False, self.word_gap))
                    continue
                
                # Add element gap between dots/dashes (but not after the last element)
                if j < len(morse_char) - 1:
                    timings.append((False, self.element_gap))
            
            # Add letter gap (but not after the last letter)
            if i < len(morse_text) - 1 and morse_text[i + 1] != ' ':
                timings.append((False, self.letter_gap))
        
        return timings


class MorseCodeDecoder:
    """Decodes Morse code to text messages"""
    
    def __init__(self, wpm=20):
        """
        Initialize decoder with specified words per minute
        
        Args:
            wpm: Words per minute (default: 20)
        """
        self.wpm = wpm
        self.dot_duration = 1200.0 / wpm  # milliseconds
        self.dash_threshold = 2 * self.dot_duration  # Threshold to distinguish dot from dash
        self.letter_gap_threshold = 2 * self.dot_duration  # Gap to separate letters
        self.word_gap_threshold = 5 * self.dot_duration  # Gap to separate words
    
    def decode(self, morse_code):
        """
        Decode Morse code string to text
        
        Args:
            morse_code: String of Morse code (dots, dashes, and spaces)
            
        Returns:
            Decoded text string
        """
        # Split by word spaces (multiple spaces or /)
        words = morse_code.split(' / ')
        decoded_words = []
        
        for word in words:
            # Split by letter spaces
            letters = word.split(' ')
            decoded_letters = []
            
            for letter in letters:
                if letter in MORSE_CODE_REVERSE:
                    decoded_letters.append(MORSE_CODE_REVERSE[letter])
            
            decoded_words.append(''.join(decoded_letters))
        
        return ' '.join(decoded_words)
    
    def decode_from_timings(self, timings):
        """
        Decode timing sequence to text
        
        Args:
            timings: List of tuples (state, duration_ms) where state is True for ON, False for OFF
            
        Returns:
            Decoded text string
        """
        morse_chars = []
        current_char = []
        
        for state, duration in timings:
            if state:  # ON - dot or dash
                if duration < self.dash_threshold:
                    current_char.append('.')
                else:
                    current_char.append('-')
            else:  # OFF - gap
                if duration >= self.word_gap_threshold:
                    # Word gap
                    if current_char:
                        morse_chars.append(''.join(current_char))
                        current_char = []
                    morse_chars.append('/')
                elif duration >= self.letter_gap_threshold:
                    # Letter gap
                    if current_char:
                        morse_chars.append(''.join(current_char))
                        current_char = []
        
        # Don't forget the last character
        if current_char:
            morse_chars.append(''.join(current_char))
        
        # Convert morse characters to text
        morse_string = ' '.join(morse_chars)
        return self.decode(morse_string)


if __name__ == "__main__":
    # Test the encoder and decoder
    encoder = MorseCodeEncoder(wpm=20)
    decoder = MorseCodeDecoder(wpm=20)
    
    test_text = "HELLO WORLD"
    print(f"Original text: {test_text}")
    
    morse = encoder.encode(test_text)
    print(f"Morse code: {morse}")
    
    decoded = decoder.decode(morse)
    print(f"Decoded text: {decoded}")
    
    # Test timing encoding
    timings = encoder.encode_to_timings(test_text)
    print(f"\nTiming sequence length: {len(timings)}")
    print(f"First 10 timings: {timings[:10]}")
