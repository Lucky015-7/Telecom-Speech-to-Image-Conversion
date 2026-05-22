# 🏗️ System Architecture

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                         │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Streamlit Frontend (Port 8501)                │  │
│  │                                                             │  │
│  │  • Audio Upload Interface                                  │  │
│  │  • Mode Selection (A/B)                                    │  │
│  │  • Real-time Progress Tracking                             │  │
│  │  • Results Visualization                                   │  │
│  │  • Processing History                                      │  │
│  │  • Documentation                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP/REST API
                            │ (JSON + Multipart)
┌───────────────────────────▼─────────────────────────────────────┐
│                      API GATEWAY LAYER                           │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              FastAPI Backend (Port 8000)                   │  │
│  │                                                             │  │
│  │  Endpoints:                                                │  │
│  │  • POST /process/mode-a    → Audio-Direct Processing      │  │
│  │  • POST /process/mode-b    → Speech-Guided Processing     │  │
│  │  • GET  /image/{filename}  → Retrieve Generated Image     │  │
│  │  • GET  /health            → Health Check                 │  │
│  │  • GET  /scenes            → Scene Vocabulary             │  │
│  │  • GET  /docs              → API Documentation            │  │
│  └───────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                    PROCESSING LAYER                              │
│                                                                   │
│  ┌─────────────────────┐         ┌─────────────────────┐        │
│  │   MODE A PIPELINE   │         │   MODE B PIPELINE   │        │
│  │                     │         │                     │        │
│  │  1. Audio Input     │         │  1. Audio Input     │        │
│  │  2. CLAP Encoding   │         │  2. Whisper ASR     │        │
│  │  3. Scene Matching  │         │  3. Transcript      │        │
│  │  4. SD Generation   │         │  4. SD Generation   │        │
│  └─────────────────────┘         └─────────────────────┘        │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Shared Components                             │  │
│  │                                                             │  │
│  │  • Audio Feature Extraction (librosa)                      │  │
│  │  • CLIP Evaluation                                         │  │
│  │  • Image Post-processing                                   │  │
│  │  • File I/O Management                                     │  │
│  └───────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                       AI MODEL LAYER                             │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Whisper    │  │     CLAP     │  │     CLIP     │          │
│  │   (OpenAI)   │  │    (LAION)   │  │   (OpenAI)   │          │
│  │              │  │              │  │              │          │
│  │  ASR Model   │  │ Audio-Text   │  │  Image-Text  │          │
│  │  ~150MB      │  │  Embedding   │  │  Similarity  │          │
│  │              │  │   ~1GB       │  │   ~600MB     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │           Stable Diffusion v1.5 (RunwayML)                │  │
│  │                                                             │  │
│  │  • Text-to-Image Generation                                │  │
│  │  • 512x512 Resolution                                      │  │
│  │  • ~4GB Model Size                                         │  │
│  │  • FP16 Precision (GPU) / FP32 (CPU)                       │  │
│  │  • Attention Slicing Enabled                               │  │
│  └───────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                      DATA STORAGE LAYER                          │
│                                                                   │
│  ┌─────────────────────┐         ┌─────────────────────┐        │
│  │   Input Storage     │         │  Output Storage     │        │
│  │                     │         │                     │        │
│  │  data/inputs/       │         │  data/outputs/      │        │
│  │  • Audio files      │         │  • Generated images │        │
│  │  • Temporary cache  │         │  • Metadata JSON    │        │
│  └─────────────────────┘         └─────────────────────┘        │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Scene Vocabulary Database                     │  │
│  │                                                             │  │
│  │  • 66 Pre-defined Scenes                                   │  │
│  │  • 8 Domain Categories                                     │  │
│  │  • Pre-encoded CLAP Embeddings                             │  │
│  │  • Pre-encoded CLIP Embeddings                             │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Detailed Component Architecture

### 1. Frontend Layer (Streamlit)

```
┌─────────────────────────────────────┐
│        Streamlit Application        │
├─────────────────────────────────────┤
│                                     │
│  ┌───────────────────────────────┐ │
│  │      Main Interface           │ │
│  │  • Header & Branding          │ │
│  │  • Tab Navigation             │ │
│  │  • Sidebar Controls           │ │
│  └───────────────────────────────┘ │
│                                     │
│  ┌───────────────────────────────┐ │
│  │    Process Audio Tab          │ │
│  │  • File Uploader              │ │
│  │  • Mode Selector              │ │
│  │  • Generate Button            │ │
│  │  • Progress Display           │ │
│  │  • Results Viewer             │ │
│  └───────────────────────────────┘ │
│                                     │
│  ┌───────────────────────────────┐ │
│  │    Results Dashboard Tab      │ │
│  │  • Processing History         │ │
│  │  • Comparison View            │ │
│  │  • Metrics Display            │ │
│  └───────────────────────────────┘ │
│                                     │
│  ┌───────────────────────────────┐ │
│  │    Documentation Tab          │ │
│  │  • System Overview            │ │
│  │  • Technology Info            │ │
│  │  • Usage Guide                │ │
│  └───────────────────────────────┘ │
│                                     │
│  ┌───────────────────────────────┐ │
│  │    Session State Manager      │ │
│  │  • Current Result             │ │
│  │  • Processing History         │ │
│  │  • User Preferences           │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

### 2. Backend Layer (FastAPI)

```
┌─────────────────────────────────────────────┐
│           FastAPI Application               │
├─────────────────────────────────────────────┤
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │        Route Handlers                 │ │
│  │                                       │ │
│  │  • /                  → Root          │ │
│  │  • /health            → Health Check  │ │
│  │  • /process/mode-a    → Mode A        │ │
│  │  • /process/mode-b    → Mode B        │ │
│  │  • /image/{filename}  → Get Image     │ │
│  │  • /scenes            → Get Vocab     │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │        Middleware                     │ │
│  │                                       │ │
│  │  • CORS Handler                       │ │
│  │  • Request Logging                    │ │
│  │  • Error Handler                      │ │
│  │  • File Size Validator                │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │        Model Manager                  │ │
│  │                                       │ │
│  │  • Model Loading                      │ │
│  │  • GPU/CPU Detection                  │ │
│  │  • Memory Management                  │ │
│  │  • Model Caching                      │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │        Processing Pipeline            │ │
│  │                                       │ │
│  │  • Audio Validation                   │ │
│  │  • Feature Extraction                 │ │
│  │  • Model Inference                    │ │
│  │  • Image Generation                   │ │
│  │  • Evaluation                         │ │
│  └───────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

### 3. Mode A Processing Pipeline

```
Audio Input (.mp3, .wav, etc.)
        │
        ▼
┌───────────────────┐
│  Audio Loading    │
│  (librosa)        │
│  • Resample 48kHz │
│  • Normalize      │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ Feature Extract   │
│ (librosa)         │
│ • RMS Energy      │
│ • Spectral Cent.  │
│ • Zero-Cross Rate │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  CLAP Encoding    │
│  (Audio → Vector) │
│  • 512-dim embed  │
│  • L2 normalized  │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ Scene Matching    │
│ (Cosine Sim.)     │
│ • Compare w/ 66   │
│ • Top-5 retrieval │
│ • Best match      │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ Stable Diffusion  │
│ (Text → Image)    │
│ • 50 steps        │
│ • Guidance 7.5    │
│ • 512x512 output  │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ CLIP Evaluation   │
│ (Image + Text)    │
│ • Similarity score│
│ • Quality metric  │
└────────┬──────────┘
         │
         ▼
    Generated Image
    + Metadata JSON
```

### 4. Mode B Processing Pipeline

```
Audio Input (.mp3, .wav, etc.)
        │
        ▼
┌───────────────────┐
│  Audio Loading    │
│  (librosa)        │
│  • Resample 48kHz │
│  • Normalize      │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ Feature Extract   │
│ (librosa)         │
│ • RMS Energy      │
│ • Spectral Cent.  │
│ • Zero-Cross Rate │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Whisper ASR      │
│  (Audio → Text)   │
│  • Transcription  │
│  • Language detect│
│  • Confidence     │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ Text Processing   │
│ • Clean transcript│
│ • Format prompt   │
│ • Validate        │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ Stable Diffusion  │
│ (Text → Image)    │
│ • 50 steps        │
│ • Guidance 7.5    │
│ • 512x512 output  │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ CLIP Evaluation   │
│ (Image + Text)    │
│ • Similarity score│
│ • Quality metric  │
└────────┬──────────┘
         │
         ▼
    Generated Image
    + Transcript
    + Metadata JSON
```

## Data Flow Diagram

```
┌──────────┐
│   User   │
└────┬─────┘
     │ 1. Upload Audio
     ▼
┌─────────────┐
│  Frontend   │
│  (Streamlit)│
└────┬────────┘
     │ 2. HTTP POST /process/mode-{a|b}
     │    (multipart/form-data)
     ▼
┌─────────────┐
│   Backend   │
│  (FastAPI)  │
└────┬────────┘
     │ 3. Save to data/inputs/
     ▼
┌─────────────┐
│ File System │
└────┬────────┘
     │ 4. Load Audio
     ▼
┌─────────────┐
│   librosa   │
└────┬────────┘
     │ 5. Process Audio
     ▼
┌─────────────┐     ┌─────────────┐
│    CLAP     │ OR  │   Whisper   │
│  (Mode A)   │     │   (Mode B)  │
└────┬────────┘     └────┬────────┘
     │                   │
     │ 6. Scene/Text     │
     └────────┬──────────┘
              ▼
     ┌─────────────────┐
     │ Stable Diffusion│
     └────────┬────────┘
              │ 7. Generate Image
              ▼
     ┌─────────────────┐
     │   File System   │
     │ data/outputs/   │
     └────────┬────────┘
              │ 8. Evaluate
              ▼
     ┌─────────────────┐
     │      CLIP       │
     └────────┬────────┘
              │ 9. Return JSON
              ▼
     ┌─────────────────┐
     │    Backend      │
     │   (Response)    │
     └────────┬────────┘
              │ 10. HTTP Response
              ▼
     ┌─────────────────┐
     │    Frontend     │
     │  (Display)      │
     └────────┬────────┘
              │ 11. Show Results
              ▼
     ┌─────────────────┐
     │      User       │
     └─────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Local Machine                         │
│                                                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │              Virtual Environment                 │    │
│  │              (.venv)                             │    │
│  │                                                   │    │
│  │  ┌──────────────┐         ┌──────────────┐      │    │
│  │  │   Backend    │         │   Frontend   │      │    │
│  │  │   Process    │         │   Process    │      │    │
│  │  │              │         │              │      │    │
│  │  │ Port: 8000   │◄────────┤ Port: 8501   │      │    │
│  │  │              │  API    │              │      │    │
│  │  └──────┬───────┘  Calls  └──────────────┘      │    │
│  │         │                                        │    │
│  │         ▼                                        │    │
│  │  ┌──────────────┐                               │    │
│  │  │  GPU/CPU     │                               │    │
│  │  │  (CUDA/CPU)  │                               │    │
│  │  └──────────────┘                               │    │
│  └─────────────────────────────────────────────────┘    │
│                                                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │              File System                         │    │
│  │                                                   │    │
│  │  data/                                           │    │
│  │  ├── inputs/    (Audio uploads)                 │    │
│  │  └── outputs/   (Generated images)              │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit 1.24+ | Web UI framework |
| **Backend** | FastAPI 0.100+ | REST API server |
| **Server** | Uvicorn | ASGI server |
| **ASR** | Whisper (base) | Speech recognition |
| **Audio Embed** | CLAP (larger) | Audio-text matching |
| **Image Gen** | Stable Diffusion 1.5 | Text-to-image |
| **Evaluation** | CLIP (ViT-B/32) | Image-text similarity |
| **Audio Proc** | librosa 0.10+ | Feature extraction |
| **Deep Learning** | PyTorch 2.0+ | ML framework |
| **Transformers** | HuggingFace 4.30+ | Model loading |

---

**This architecture provides a scalable, modular foundation for the Voice-to-Image Generation System.**
