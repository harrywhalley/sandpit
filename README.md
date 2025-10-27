# Cat Purr Model

A scientifically-based acoustic model of domestic cat purring, with an interactive web interface.

## Scientific Background

This model is based on peer-reviewed research on domestic cat (Felis sylvestris catus) purring:

- **Fundamental Frequency**: 25-30 Hz (typical: 27 Hz)
- **Frequency Range**: 20-44 Hz (harmonics extend to 150 Hz)
- **Sound Production**: Self-sustaining oscillations in the larynx
- **Characteristics**: Low-frequency phonation with natural vibrato and tremolo

### Key Research References

- Domestic cat larynges can produce purring frequencies without neural input (Current Biology, 2023)
- The felid purr: A healing mechanism? (Journal of the Acoustical Society of America)
- Purr frequencies correspond to therapeutic vibrational/electrical frequencies (25-150 Hz)

## Features

- **Scientifically Accurate**: Based on published research on cat purr acoustics
- **Interactive Controls**: Adjust frequency, duration, volume, and modulation parameters
- **Real-time Generation**: Generate purr sounds with custom parameters
- **Web Interface**: Beautiful, responsive HTML interface
- **Export Capability**: Download generated purrs as WAV files

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Web Interface (Recommended)

1. Start the web server:
```bash
python purr_server.py
```

2. Open your browser to: `http://localhost:5000`

3. Adjust parameters using the sliders:
   - **Fundamental Frequency** (20-44 Hz): Base purr frequency
   - **Duration** (0.5-10 seconds): Length of purr sound
   - **Volume** (0.1-1.0): Overall amplitude
   - **Vibrato Rate/Depth**: Frequency modulation (natural variation)
   - **Tremolo Rate/Depth**: Amplitude modulation (rhythmic pulsing)

4. Click "Generate Purr" to create the sound

5. Play the audio or download as WAV file

### Command Line

Generate a purr with default parameters:
```bash
python cat_purr_model.py --output purr.wav
```

Customize parameters:
```bash
python cat_purr_model.py --freq 28 --duration 5 --amplitude 0.7 --output my_purr.wav
```

Using JSON parameters:
```bash
python cat_purr_model.py --json-params '{"fundamental_freq": 27, "duration": 3, "amplitude": 0.5, "vibrato_rate": 5.0}'
```

## Parameters Explained

### Fundamental Frequency (20-44 Hz)
The base frequency of the purr. Scientific literature shows most cats purr between 25-30 Hz. Lower frequencies sound deeper, higher frequencies sound lighter.

### Duration
How long the purr lasts. Cats can purr continuously for extended periods.

### Amplitude (Volume)
Overall loudness of the purr (0.0-1.0).

### Vibrato
Frequency modulation that creates natural pitch variation:
- **Rate**: How fast the pitch varies (Hz)
- **Depth**: How much the pitch varies (Hz)

### Tremolo
Amplitude modulation that creates rhythmic pulsing:
- **Rate**: How fast the volume pulses (Hz)
- **Depth**: How much the volume varies (0.0-1.0)

## Model Architecture

The purr model uses:

1. **Harmonic Synthesis**: Fundamental frequency + harmonics (up to 150 Hz)
2. **Frequency Modulation**: Vibrato for natural pitch variation
3. **Amplitude Modulation**: Tremolo for rhythmic pulsing
4. **Envelope Shaping**: Smooth attack and release
5. **Noise Addition**: Subtle noise for realism (airflow/tissue sounds)

## Files

- `cat_purr_model.py` - Core purr synthesis model
- `purr_server.py` - Flask web server
- `purr_interface.html` - Interactive web interface
- `requirements.txt` - Python dependencies

## Examples

### Contented Cat (Default)
```python
from cat_purr_model import CatPurrModel

model = CatPurrModel()
model.set_parameters(fundamental_freq=27, duration=3.0)
model.export_to_wav('contented_purr.wav')
```

### Deep, Rumbling Purr
```python
model.set_parameters(
    fundamental_freq=23,
    duration=5.0,
    vibrato_depth=1.0,
    tremolo_depth=0.15
)
model.export_to_wav('deep_purr.wav')
```

### High-Pitched, Excited Purr
```python
model.set_parameters(
    fundamental_freq=35,
    duration=2.0,
    vibrato_rate=7.0,
    tremolo_rate=6.0
)
model.export_to_wav('excited_purr.wav')
```

## Technical Details

- **Sample Rate**: 44100 Hz
- **Output Format**: 16-bit PCM WAV
- **Harmonics**: Up to 5 harmonics (within 150 Hz limit)
- **Synthesis Method**: Additive synthesis with modulation

## Future Enhancements

Possible improvements based on ongoing research:
- Individual cat variations
- Emotional state modeling (contentment vs. distress)
- Interaction with breathing patterns
- Real-time synthesis and streaming

## License

Open source - use freely for research and entertainment!

## References

1. Fraade, S. T. et al. (2023). "Domestic cat larynges can produce purring frequencies without neural input." Current Biology.
2. Von Muggenthaler, E. (2001). "The felid purr: A healing mechanism?" The Journal of the Acoustical Society of America.
3. Peters, G. (2002). "Purring and similar vocalizations in mammals." Mammal Review.
