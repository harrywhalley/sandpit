"""
Web server for the cat purr model.
Provides HTTP endpoints for generating purr sounds and serving the UI.
"""

from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import numpy as np
import io
import base64
from cat_purr_model import CatPurrModel

app = Flask(__name__, static_folder='.')
CORS(app)

# Global model instance
purr_model = CatPurrModel()


@app.route('/')
def index():
    """Serve the main HTML interface."""
    return send_from_directory('.', 'purr_interface.html')


@app.route('/api/generate_purr', methods=['POST'])
def generate_purr():
    """
    Generate a purr sound with given parameters.

    Request JSON body:
    {
        "fundamental_freq": 27.0,
        "duration": 3.0,
        "amplitude": 0.5,
        "vibrato_rate": 5.0,
        "vibrato_depth": 0.5,
        "tremolo_rate": 4.0,
        "tremolo_depth": 0.1
    }

    Returns:
        JSON with audio data as base64 WAV
    """
    try:
        params = request.json

        # Update model parameters
        purr_model.set_parameters(**params)

        # Generate audio
        audio, sample_rate = purr_model.generate_purr()

        # Convert to 16-bit PCM
        audio_int16 = np.int16(audio * 32767)

        # Create WAV file in memory
        wav_buffer = io.BytesIO()
        import scipy.io.wavfile as wavfile
        wavfile.write(wav_buffer, sample_rate, audio_int16)
        wav_buffer.seek(0)

        # Encode as base64
        audio_base64 = base64.b64encode(wav_buffer.read()).decode('utf-8')

        return jsonify({
            'success': True,
            'audio': audio_base64,
            'parameters': purr_model.get_parameters()
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/parameters', methods=['GET'])
def get_parameters():
    """Get current model parameters."""
    return jsonify(purr_model.get_parameters())


@app.route('/api/download_purr', methods=['POST'])
def download_purr():
    """
    Generate and download a purr sound as WAV file.
    """
    try:
        params = request.json

        # Update model parameters
        purr_model.set_parameters(**params)

        # Generate audio
        audio, sample_rate = purr_model.generate_purr()

        # Convert to 16-bit PCM
        audio_int16 = np.int16(audio * 32767)

        # Create WAV file in memory
        wav_buffer = io.BytesIO()
        import scipy.io.wavfile as wavfile
        wavfile.write(wav_buffer, sample_rate, audio_int16)
        wav_buffer.seek(0)

        return send_file(
            wav_buffer,
            mimetype='audio/wav',
            as_attachment=True,
            download_name='cat_purr.wav'
        )

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("Starting Cat Purr Model Server...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
