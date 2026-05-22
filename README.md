# 🎙️ Voice-to-Image Generation System

**SLT Mobitel Research Project**  
*Intelligent Voice Understanding Platform for Telecom Customer Service*

![Version](https://img.shields.io/badge/version-3.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-Research-red)

## 📋 Overview

This system translates spoken audio from telecom customer service interactions into contextually relevant images using state-of-the-art multimodal AI. It bridges the gap between audio-based customer interactions and visual content, offering a novel tool for intelligent service automation.

### ✨ Key Features

- 🔊 **Dual Processing Modes**: Audio-direct retrieval (CLAP) and speech-guided generation (Whisper + Stable Diffusion)
- 🎨 **High-Quality Image Generation**: Powered by Stable Diffusion v1.5
- 📊 **Intelligent Evaluation**: CLIP-based similarity scoring
- 🌐 **Domain-Specific**: Tailored for telecom customer service scenarios
- 💻 **Modern Web Interface**: Beautiful Streamlit frontend with real-time processing
- 🚀 **RESTful API**: FastAPI backend for easy integration

## 🏗️ Architecture

```
┌─────────────────┐
│  Audio Input    │
│  (.mp3, .wav)   │
└────────┬────────┘
         │
    ┌────▼────┐
    │  Mode?  │
    └─┬────┬──┘
      │    │
┌─────▼──┐ │  ┌──────▼─────┐
│ Mode A │ │  │  Mode B    │
│ CLAP   │ │  │  Whisper   │
└────┬───┘ │  └─────┬──────┘
     │     │        │
     │  ┌──▼────────▼──┐
     └─►│ Stable        │
        │ Diffusion     │
        └───────┬───────┘
                │
        ┌───────▼────────┐
        │ Generated Image│
        │   + Metrics    │
        └────────────────┘
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Backend (Terminal 1)
```bash
start_backend.bat
```

### 3. Start Frontend (Terminal 2)
```bash
start_frontend.bat
```

### 4. Open Browser
Navigate to: **http://localhost:8501**

📖 For detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)

## 🎯 Processing Modes

### Mode A: Audio-Direct Retrieval 🔊
- **Technology**: CLAP (Contrastive Language-Audio Pretraining)
- **Process**: Audio → Acoustic Embedding → Scene Matching → Image Generation
- **Best For**: Noisy or unclear audio, background noise
- **Speed**: Fast (~30-45 seconds)
- **Vocabulary**: 66 pre-defined telecom service scenes

### Mode B: Speech Recognition 🗣️
- **Technology**: Whisper ASR + Stable Diffusion
- **Process**: Audio → Speech-to-Text → Text-to-Image
- **Best For**: Clear, articulate speech
- **Speed**: Moderate (~45-60 seconds)
- **Flexibility**: Open-ended generation from transcript

## 🏢 Domain Coverage

### ConnectPlus ISP Service Areas

#### 🌐 Internet Connectivity
- Router problems and configuration
- Network outages and disruptions
- Slow speeds and bandwidth issues
- Home network setup

#### 📺 Television Services
- No signal issues
- Set-top box faults
- Cable TV problems
- Broadcast service complaints

#### 🔧 Field Operations
- Tower damage and maintenance
- Cable faults and repairs
- Technician home visits
- Infrastructure incidents

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **ASR** | OpenAI Whisper | Speech-to-text transcription |
| **Audio Embedding** | LAION CLAP | Audio-language matching |
| **Image Generation** | Stable Diffusion v1.5 | Text-to-image synthesis |
| **Evaluation** | OpenAI CLIP | Image-text similarity |
| **Backend** | FastAPI | RESTful API server |
| **Frontend** | Streamlit | Web interface |
| **Audio Processing** | librosa | Feature extraction |

## 📊 Evaluation Metrics

- **CLIP Similarity Score**: Measures semantic alignment between generated image and audio content (0-1 scale)
- **Acoustic Features**: Energy, spectral brightness, zero-crossing rate
- **Processing Time**: End-to-end generation latency
- **Scene Match Confidence**: Similarity score for Mode A retrieval

## 🖼️ Frontend Features

### 🎨 Modern UI Design
- SLT Mobitel branded color scheme
- Responsive layout with real-time updates
- Intuitive mode selection
- Progress tracking with visual feedback

### 📈 Results Dashboard
- Generated image display with zoom
- Detailed metrics and scores
- Processing history tracking
- Acoustic feature visualization

### 📚 Documentation Tab
- System overview and architecture
- Technology stack information
- Usage guidelines
- Domain coverage details

## 🔌 API Endpoints

### Health Check
```http
GET /health
```

### Process Audio - Mode A
```http
POST /process/mode-a
Content-Type: multipart/form-data

file: <audio_file>
```

### Process Audio - Mode B
```http
POST /process/mode-b
Content-Type: multipart/form-data

file: <audio_file>
```

### Retrieve Image
```http
GET /image/{filename}
```

### Get Scene Vocabulary
```http
GET /scenes
```

## 📁 Project Structure

```
Telecom-Speech-to-Image-Conversion/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── config.py            # Configuration
│   ├── vocab.py             # Scene vocabulary
│   └── utils/
│       ├── audio_utils.py   # Audio processing
│       └── eval_utils.py    # Evaluation metrics
├── frontend/
│   └── app.py               # Streamlit interface
├── data/
│   ├── inputs/              # Audio uploads
│   └── outputs/             # Generated images
├── requirements.txt         # Dependencies
├── SETUP_GUIDE.md          # Detailed setup
└── README.md               # This file
```

## 🎓 Research Background

This prototype was developed as part of an internship at **SLT Mobitel**, Sri Lanka's national telecommunications provider. The project explores how emerging multimodal AI technologies can be applied to real-world telecom customer service settings.

### Key Contributions
- Novel application of CLAP for telecom audio understanding
- Domain-specific scene vocabulary for ISP customer service
- Comparative analysis of audio-direct vs. speech-guided approaches
- Production-ready API architecture for deployment

## 🔮 Future Enhancements

### Short-Term
- [ ] Fine-tune Whisper on Sri Lankan English corpus
- [ ] Dynamic vocabulary expansion using LLMs
- [ ] Confidence-based mode fallback
- [ ] Multilingual support (Sinhala, Tamil)

### Medium-Term
- [ ] Real-time API for live call processing
- [ ] Upgrade to Stable Diffusion XL
- [ ] Web-based admin dashboard
- [ ] User study with call center agents

### Long-Term
- [ ] Production deployment at SLT Mobitel
- [ ] Multi-turn conversation support
- [ ] Retrieval-augmented generation with photo database
- [ ] Integration with CRM systems

## ⚠️ Limitations

- **Language**: Optimized for English audio (Mode B)
- **Compute**: Requires GPU for optimal performance
- **Domain**: Scoped to telecom customer service scenarios
- **Status**: Research prototype, not production-ready

## 🔐 Security & Privacy

- Research prototype for internal use
- No authentication/authorization implemented
- Audio files stored temporarily during processing
- Use in trusted environments only

## 📞 Support & Contact

For questions or issues:
1. Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for installation help
2. Review API documentation at `/docs` endpoint
3. Contact SLT Mobitel Research team

## 📄 License

**SLT Mobitel Research Project - Confidential**  
For internal research and evaluation purposes only.

## 🙏 Acknowledgments

- **Organization**: SLT Mobitel
- **Domain**: Artificial Intelligence / Natural Language Processing
- **Models**: OpenAI, LAION, RunwayML, Stability AI
- **Version**: 3.0 (2026)

---

<div align="center">

**Built with ❤️ for SLT Mobitel Research**

*Intelligent Voice Understanding Platform for Telecom Customer Service*

</div>
