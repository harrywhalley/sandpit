"""
Cat Purr Model
Based on scientific literature:
- Fundamental frequency: 25-30 Hz
- Harmonics extend to 150 Hz
- Self-sustaining oscillations with natural variation
"""

import numpy as np
import json
import sys
from typing import Dict, Tuple


class CatPurrModel:
    """
    Models the acoustic characteristics of a domestic cat's purr.

    Based on research showing purrs have fundamental frequencies of 25-30 Hz
    with harmonics extending up to 150 Hz.
    """

    def __init__(self, sample_rate: int = 44100):
        """
        Initialize the cat purr model.

        Args:
            sample_rate: Audio sample rate in Hz (default: 44100)
        """
        self.sample_rate = sample_rate

        # Default parameters based on literature
        self.fundamental_freq = 27.0  # Hz
        self.duration = 3.0  # seconds
        self.amplitude = 0.5  # 0-1 range

        # Harmonic structure
        self.num_harmonics = 5
        self.harmonic_amplitudes = [1.0, 0.6, 0.4, 0.25, 0.15]

        # Modulation parameters for natural sound
        self.vibrato_rate = 5.0  # Hz (slight frequency modulation)
        self.vibrato_depth = 0.5  # Hz
        self.tremolo_rate = 4.0  # Hz (amplitude modulation)
        self.tremolo_depth = 0.1  # 0-1 range

    def set_parameters(self, **kwargs):
        """
        Update model parameters.

        Supported parameters:
        - fundamental_freq: Base frequency in Hz (20-44)
        - duration: Sound duration in seconds
        - amplitude: Overall volume (0-1)
        - vibrato_rate: Frequency modulation rate in Hz
        - vibrato_depth: Frequency modulation depth in Hz
        - tremolo_rate: Amplitude modulation rate in Hz
        - tremolo_depth: Amplitude modulation depth (0-1)
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def generate_purr(self) -> Tuple[np.ndarray, int]:
        """
        Generate a cat purr sound.

        Returns:
            Tuple of (audio_data, sample_rate)
            audio_data: numpy array of audio samples
            sample_rate: sample rate in Hz
        """
        # Time array
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)

        # Initialize audio signal
        audio = np.zeros_like(t)

        # Add fundamental frequency and harmonics
        for i in range(self.num_harmonics):
            harmonic_freq = self.fundamental_freq * (i + 1)

            # Skip harmonics above 150 Hz (as per literature)
            if harmonic_freq > 150:
                break

            # Apply vibrato (frequency modulation)
            vibrato = self.vibrato_depth * np.sin(2 * np.pi * self.vibrato_rate * t)
            instantaneous_freq = harmonic_freq + vibrato

            # Generate harmonic
            phase = 2 * np.pi * np.cumsum(instantaneous_freq) / self.sample_rate
            harmonic_amplitude = self.harmonic_amplitudes[i] if i < len(self.harmonic_amplitudes) else 0.1
            audio += harmonic_amplitude * np.sin(phase)

        # Normalize harmonics
        audio = audio / self.num_harmonics

        # Apply tremolo (amplitude modulation)
        tremolo = 1.0 + self.tremolo_depth * np.sin(2 * np.pi * self.tremolo_rate * t)
        audio *= tremolo

        # Apply overall amplitude and envelope
        envelope = self._create_envelope(len(audio))
        audio *= envelope * self.amplitude

        # Add subtle noise for realism (soft tissue/air noise)
        noise = np.random.normal(0, 0.01, len(audio))
        audio += noise * self.amplitude * 0.05

        # Normalize to prevent clipping
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = audio / max_val * 0.9

        return audio, self.sample_rate

    def _create_envelope(self, num_samples: int) -> np.ndarray:
        """
        Create an amplitude envelope with smooth attack and release.

        Args:
            num_samples: Number of samples in the envelope

        Returns:
            Envelope array
        """
        envelope = np.ones(num_samples)

        # Attack time (fade in)
        attack_samples = int(0.1 * num_samples)
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)

        # Release time (fade out)
        release_samples = int(0.1 * num_samples)
        envelope[-release_samples:] = np.linspace(1, 0, release_samples)

        return envelope

    def export_to_wav(self, filename: str):
        """
        Generate purr and save to WAV file.

        Args:
            filename: Output WAV filename
        """
        try:
            import scipy.io.wavfile as wavfile
        except ImportError:
            raise ImportError("scipy is required for WAV export. Install with: pip install scipy")

        audio, sample_rate = self.generate_purr()

        # Convert to 16-bit PCM
        audio_int16 = np.int16(audio * 32767)

        wavfile.write(filename, sample_rate, audio_int16)

    def get_parameters(self) -> Dict:
        """
        Get current model parameters.

        Returns:
            Dictionary of parameters
        """
        return {
            'fundamental_freq': self.fundamental_freq,
            'duration': self.duration,
            'amplitude': self.amplitude,
            'vibrato_rate': self.vibrato_rate,
            'vibrato_depth': self.vibrato_depth,
            'tremolo_rate': self.tremolo_rate,
            'tremolo_depth': self.tremolo_depth,
            'sample_rate': self.sample_rate
        }


def main():
    """Command-line interface for the cat purr model."""
    import argparse

    parser = argparse.ArgumentParser(description='Generate a cat purr sound')
    parser.add_argument('--freq', type=float, default=27.0, help='Fundamental frequency (20-44 Hz)')
    parser.add_argument('--duration', type=float, default=3.0, help='Duration in seconds')
    parser.add_argument('--amplitude', type=float, default=0.5, help='Amplitude (0-1)')
    parser.add_argument('--output', type=str, default='purr.wav', help='Output WAV file')
    parser.add_argument('--json-params', type=str, help='JSON string with parameters')

    args = parser.parse_args()

    # Create model
    model = CatPurrModel()

    # Set parameters from JSON if provided
    if args.json_params:
        params = json.loads(args.json_params)
        model.set_parameters(**params)
    else:
        model.set_parameters(
            fundamental_freq=args.freq,
            duration=args.duration,
            amplitude=args.amplitude
        )

    # Generate and save
    print(f"Generating purr with parameters: {model.get_parameters()}")
    model.export_to_wav(args.output)
    print(f"Purr saved to {args.output}")


if __name__ == '__main__':
    main()
