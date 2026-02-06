"""
HackRF Interface Module

This module provides a high-level interface to the HackRF device
for transmitting and receiving Morse code signals.
"""

import numpy as np
import time
import threading
from collections import deque


class HackRFTransmitter:
    """Handles transmission of Morse code via HackRF"""
    
    def __init__(self, frequency=433.92e6, sample_rate=2e6, tx_gain=0):
        """
        Initialize HackRF transmitter
        
        Args:
            frequency: Transmission frequency in Hz (default: 433.92 MHz)
            sample_rate: Sample rate in Hz (default: 2 MHz)
            tx_gain: TX gain in dB (0-47, default: 0)
        """
        self.frequency = frequency
        self.sample_rate = sample_rate
        self.tx_gain = tx_gain
        self.hackrf = None
        
    def initialize(self):
        """Initialize HackRF device for transmission"""
        try:
            import pyhackrf
            self.hackrf = pyhackrf.HackRF()
            self.hackrf.sample_rate = self.sample_rate
            self.hackrf.center_freq = self.frequency
            self.hackrf.txvga_gain = self.tx_gain
            self.hackrf.enable_amp = False
            return True
        except ImportError:
            print("Warning: pyhackrf not available. Running in simulation mode.")
            return False
        except Exception as e:
            print(f"Error initializing HackRF: {e}")
            return False
    
    def set_frequency(self, frequency):
        """Set transmission frequency"""
        self.frequency = frequency
        if self.hackrf:
            self.hackrf.center_freq = frequency
    
    def transmit_morse(self, timings):
        """
        Transmit Morse code from timing sequence
        
        Args:
            timings: List of tuples (state, duration_ms) where state is True for ON, False for OFF
        """
        print(f"Transmitting Morse code on {self.frequency / 1e6:.3f} MHz...")
        
        if self.hackrf:
            self._transmit_with_hackrf(timings)
        else:
            self._simulate_transmission(timings)
    
    def _transmit_with_hackrf(self, timings):
        """Transmit using actual HackRF hardware"""
        # Generate signal buffer for entire transmission
        signal_buffer = self._generate_signal_buffer(timings)
        
        # Convert to IQ samples (complex64)
        iq_samples = signal_buffer.astype(np.complex64)
        
        # Start transmission
        self.hackrf.start_tx()
        
        try:
            # Send samples
            self.hackrf.send_samples(iq_samples)
        finally:
            self.hackrf.stop_tx()
    
    def _generate_signal_buffer(self, timings):
        """Generate IQ signal buffer from timings"""
        samples_list = []
        
        for state, duration_ms in timings:
            # Calculate number of samples for this duration
            num_samples = int((duration_ms / 1000.0) * self.sample_rate)
            
            if state:
                # ON - generate carrier wave (CW)
                # Simple carrier: e^(j*2*pi*f*t) but we're already at center freq
                # So just generate constant amplitude
                samples = np.ones(num_samples) * 0.5
            else:
                # OFF - no signal
                samples = np.zeros(num_samples)
            
            samples_list.append(samples)
        
        # Concatenate all samples
        return np.concatenate(samples_list)
    
    def _simulate_transmission(self, timings):
        """Simulate transmission without hardware"""
        print("SIMULATION MODE - No HackRF hardware detected")
        total_time = sum(duration for _, duration in timings) / 1000.0
        print(f"Would transmit for {total_time:.2f} seconds")
        
        # Print a visual representation
        for state, duration_ms in timings:
            if state:
                print("█" * int(duration_ms / 10), end="", flush=True)
            else:
                print(" " * int(duration_ms / 10), end="", flush=True)
            time.sleep(duration_ms / 1000.0)
        print()
    
    def close(self):
        """Close HackRF device"""
        if self.hackrf:
            try:
                self.hackrf.close()
            except Exception:
                # Silently ignore errors during cleanup as device may already be closed
                pass


class HackRFReceiver:
    """Handles reception and decoding of Morse code via HackRF"""
    
    def __init__(self, frequency=433.92e6, sample_rate=2e6, rx_gain=20):
        """
        Initialize HackRF receiver
        
        Args:
            frequency: Reception frequency in Hz (default: 433.92 MHz)
            sample_rate: Sample rate in Hz (default: 2 MHz)
            rx_gain: RX gain in dB (0-40, default: 20)
        """
        self.frequency = frequency
        self.sample_rate = sample_rate
        self.rx_gain = rx_gain
        self.hackrf = None
        self.receiving = False
        self.receive_thread = None
        self.timing_callback = None
        self.signal_buffer = deque(maxlen=int(sample_rate * 2))  # 2 seconds buffer
        
    def initialize(self):
        """Initialize HackRF device for reception"""
        try:
            import pyhackrf
            self.hackrf = pyhackrf.HackRF()
            self.hackrf.sample_rate = self.sample_rate
            self.hackrf.center_freq = self.frequency
            self.hackrf.lna_gain = self.rx_gain
            self.hackrf.vga_gain = self.rx_gain
            self.hackrf.enable_amp = False
            return True
        except ImportError:
            print("Warning: pyhackrf not available. Running in simulation mode.")
            return False
        except Exception as e:
            print(f"Error initializing HackRF: {e}")
            return False
    
    def set_frequency(self, frequency):
        """Set reception frequency"""
        self.frequency = frequency
        if self.hackrf:
            self.hackrf.center_freq = frequency
    
    def start_receiving(self, callback):
        """
        Start receiving Morse code
        
        Args:
            callback: Function to call with decoded text: callback(text)
        """
        self.timing_callback = callback
        self.receiving = True
        
        if self.hackrf:
            self.receive_thread = threading.Thread(target=self._receive_with_hackrf)
            self.receive_thread.daemon = True
            self.receive_thread.start()
        else:
            self._simulate_reception()
    
    def _receive_with_hackrf(self):
        """Receive using actual HackRF hardware"""
        self.hackrf.start_rx(self._rx_callback)
        
        while self.receiving:
            time.sleep(0.1)
        
        self.hackrf.stop_rx()
    
    def _rx_callback(self, samples):
        """Callback for received samples from HackRF"""
        # Add samples to buffer
        self.signal_buffer.extend(samples)
        
        # Process buffer to detect Morse code
        timings = self._detect_morse_timings(samples)
        
        if timings and self.timing_callback:
            self.timing_callback(timings)
    
    def _detect_morse_timings(self, samples):
        """
        Detect Morse code timings from signal samples
        
        Args:
            samples: Complex IQ samples
            
        Returns:
            List of tuples (state, duration_ms) or None
        """
        # Calculate signal power/amplitude
        amplitude = np.abs(samples)
        
        # Simple threshold-based detection
        threshold = np.mean(amplitude) + 2 * np.std(amplitude)
        signal_present = amplitude > threshold
        
        # Detect transitions and timing
        timings = []
        current_state = signal_present[0]
        state_start = 0
        
        for i in range(1, len(signal_present)):
            if signal_present[i] != current_state:
                # Transition detected
                duration_samples = i - state_start
                duration_ms = (duration_samples / self.sample_rate) * 1000.0
                
                timings.append((current_state, duration_ms))
                
                current_state = signal_present[i]
                state_start = i
        
        # Add final state
        if state_start < len(signal_present):
            duration_samples = len(signal_present) - state_start
            duration_ms = (duration_samples / self.sample_rate) * 1000.0
            timings.append((current_state, duration_ms))
        
        return timings if len(timings) > 0 else None
    
    def _simulate_reception(self):
        """Simulate reception without hardware"""
        print("SIMULATION MODE - No HackRF hardware detected")
        print(f"Listening on {self.frequency / 1e6:.3f} MHz...")
        print("Press Ctrl+C to stop")
        
        try:
            while self.receiving:
                time.sleep(1)
        except KeyboardInterrupt:
            self.receiving = False
    
    def stop_receiving(self):
        """Stop receiving"""
        self.receiving = False
        if self.receive_thread:
            self.receive_thread.join(timeout=2.0)
    
    def close(self):
        """Close HackRF device"""
        self.stop_receiving()
        if self.hackrf:
            try:
                self.hackrf.close()
            except Exception:
                # Silently ignore errors during cleanup as device may already be closed
                pass
