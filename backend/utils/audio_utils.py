"""
Audio processing utilities
"""

import librosa
import numpy as np
import soundfile as sf
from pathlib import Path


def load_audio(file_path, sample_rate=48000):
    """
    Load audio file and resample to target sample rate
    
    Args:
        file_path: Path to audio file
        sample_rate: Target sample rate (default: 48000 Hz)
    
    Returns:
        audio: Audio waveform as numpy array
        sr: Sample rate
    """
    try:
        audio, sr = librosa.load(file_path, sr=sample_rate)
        return audio, sr
    except Exception as e:
        raise ValueError(f"Error loading audio file: {str(e)}")


def extract_acoustic_features(audio, sr):
    """
    Extract acoustic features from audio signal
    
    Args:
        audio: Audio waveform
        sr: Sample rate
    
    Returns:
        dict: Dictionary containing energy, brightness, and zero-crossing rate
    """
    # Energy (RMS)
    energy = librosa.feature.rms(y=audio)[0]
    energy_mean = float(np.mean(energy))
    
    # Brightness (Spectral Centroid)
    spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]
    brightness = float(np.mean(spectral_centroid) / sr)
    
    # Zero-Crossing Rate
    zcr = librosa.feature.zero_crossing_rate(audio)[0]
    zcr_mean = float(np.mean(zcr))
    
    return {
        "energy": energy_mean,
        "brightness": brightness,
        "zero_crossing_rate": zcr_mean,
        "duration": float(len(audio) / sr)
    }


def validate_audio_file(file_path):
    """
    Validate if file is a valid audio file
    
    Args:
        file_path: Path to audio file
    
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        audio, sr = librosa.load(file_path, duration=1.0)
        return len(audio) > 0
    except:
        return False


def get_audio_duration(file_path):
    """
    Get duration of audio file in seconds
    
    Args:
        file_path: Path to audio file
    
    Returns:
        float: Duration in seconds
    """
    try:
        duration = librosa.get_duration(path=file_path)
        return duration
    except:
        return 0.0
