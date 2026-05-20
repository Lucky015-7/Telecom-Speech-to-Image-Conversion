import librosa
import numpy as np

def extract_audio_features(file_path: str) -> dict:
    """
    Extracts key audio features using librosa:
    - Root Mean Square (RMS) energy: measures signal volume/power.
    - Spectral Centroid: measures the 'brightness' or center of gravity of the spectrum.
    - Zero Crossing Rate (ZCR): measures the rate of sign changes in the signal.
    
    Parameters:
        file_path (str): The absolute or relative path to the audio file.
        
    Returns:
        dict: A dictionary containing mean features and raw time-series arrays.
    """
    # Load audio file (resampling dynamically using native sample rate)
    y, sr = librosa.load(file_path, sr=None, mono=True)
    
    # Calculate features
    rms = librosa.feature.rms(y=y)
    spec_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y=y)
    
    return {
        "rms_mean": float(np.mean(rms)),
        "spectral_centroid_mean": float(np.mean(spec_centroid)),
        "zcr_mean": float(np.mean(zcr)),
        "rms_series": rms[0].tolist(),
        "spectral_centroid_series": spec_centroid[0].tolist(),
        "zcr_series": zcr[0].tolist(),
        "duration": float(librosa.get_duration(y=y, sr=sr))
    }
