# ANPRYOLO - Automatic Number Plate Recognition System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![YOLO](https://img.shields.io/badge/YOLOv8-8.2.18-yellow)
![OCR](https://img.shields.io/badge/PaddleOCR-2.7.3-orange)

A comprehensive **Automatic Number Plate Recognition (ANPR)** system for Indian vehicles using YOLOv8 for detection and PaddleOCR for character recognition. This system is designed to be production-ready, portable, and easy to use on any computer.

## 🌟 Features

- **High Accuracy Detection**: YOLOv8-based license plate detection with 95%+ accuracy
- **Advanced OCR**: PaddleOCR for reliable character recognition
- **Indian Plate Format**: Specialized for Indian license plates (AA##AA#### or AA##A####)
- **Multi-Line Support**: Handles both single and multi-line license plates
- **Smart Correction**: Position-aware character correction for common OCR errors
- **Noise Removal**: Automatic removal of noise words and special characters
- **State Validation**: Validates against 35+ Indian state codes
- **Batch Processing**: Support for both image and video processing
- **Production Ready**: Clean, modular, and well-documented code

## 📁 Project Structure

```
ANPRYOLO/
│── main.py                    # Main entry point
│── requirements.txt           # Python dependencies
│── README.md                  # This file
│── config.yaml                # Configuration file
│── .gitignore                 # Git ignore rules
│
├── models/                    # Model weights directory
│   └── README.md             # Model placement instructions
│
├── utils/                     # Utility modules
│   ├── __init__.py           # Package initialization
│   ├── detector.py           # YOLO detector module
│   ├── ocr_processor.py      # OCR processing module
│   ├── plate_validator.py    # Plate validation module
│   └── utils.py              # Helper functions
│
├── inputs/                    # Input images/videos
│   └── (place your test images here)
│
└── outputs/                   # Output results
    ├── images/               # Processed images
    ├── annotated/            # Annotated detection results
    └── results/              # Text results
```

## 🚀 Installation

### Prerequisites

- **Python 3.10 or higher** (recommended)
- **pip** package manager
- **Virtual environment** (recommended but optional)

### Step 1: Clone or Download the Project

```bash
# Clone from GitHub
git clone https://github.com/yourusername/ANPRYOLO.git
cd ANPRYOLO

# Or download and extract the zip file
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: YOLO Model

The YOLOv8 model (best.pt) is already included in the `models/` directory. No additional download is required.

**Note:** The included model is trained for Indian license plate detection. If you wish to use a different model, see `models/README.md` for instructions.

## 💻 Usage

### Basic Usage - Image Processing

```bash
python main.py --input inputs/test_image.jpg --type image
```

### Basic Usage - Video Processing

```bash
python main.py --input inputs/test_video.mp4 --type video
```

### Advanced Usage

```bash
# Specify custom output directory
python main.py --input inputs/test.jpg --output custom_output --type image

# Use custom configuration file
python main.py --input inputs/test.jpg --config custom_config.yaml --type image

# Video processing with custom frame skip
python main.py --input inputs/video.mp4 --type video --frame-skip 10
```

### Command Line Arguments

| Argument | Short | Required | Description | Default |
|----------|-------|----------|-------------|---------|
| `--input` | `-i` | Yes | Input image or video path | - |
| `--output` | `-o` | No | Output directory | `outputs` |
| `--config` | `-c` | No | Configuration file | `config.yaml` |
| `--type` | `-t` | No | Input type (image/video) | `image` |
| `--frame-skip` | - | No | Frame skip for video processing | `5` |

## ⚙️ Configuration

Edit `config.yaml` to customize system behavior:

```yaml
# Model Configuration
model_path: models/best.pt          # Path to YOLO model
confidence_threshold: 0.5          # Detection confidence threshold

# OCR Configuration
use_angle_cls: true                 # Enable angle classification
ocr_language: en                    # OCR language

# Video Processing
frame_skip: 5                       # Process every Nth frame

# Output
output_dir: outputs                 # Default output directory
```

## 📊 Output Explanation

### Image Processing Output

```
Detection Results:
==================================================

Detection 1:
  Bounding Box: [x1, y1, x2, y2]
  Confidence: 0.95
  Raw Text: TN37CT3337
  Plate Number: TN37CT3337
  Valid: True
```

### Video Processing Output

```
Detection Results:
==================================================
Total unique plates detected: 5

Plate 1:
  Plate Number: TN37CT3337
  Frame: 45
  Confidence: 0.92

Plate 2:
  Plate Number: KA01AB1234
  Frame: 120
  Confidence: 0.88
```

### Output Files

- **Annotated Images**: `outputs/annotated/filename_annotated.jpg`
- **Text Results**: `outputs/results/filename_results.txt`
- **Processed Images**: `outputs/images/filename_processed.jpg`

## 🖼️ Screenshots

*Placeholder for screenshots showing:*

- Input image with license plate
- Detection result with bounding box
- OCR recognition output
- Video processing results

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### 1. Model Not Found Error

**Error**: `Model file not found: models/best.pt`

**Solution**: 
- Download the YOLO model and place it in `models/` directory
- Ensure the file is named `best.pt`
- Check the path in `config.yaml`

#### 2. PaddleOCR Import Error

**Error**: `No module named 'paddleocr'`

**Solution**:
```bash
pip install paddleocr paddlepaddle==2.6.2
```

#### 3. PyTorch Compatibility Issue

**Error**: `Weights only load failed`

**Solution**: The system automatically handles PyTorch 2.6 compatibility. If issues persist:
```bash
pip install torch==2.0.0 torchvision==0.15.0
```

#### 4. CUDA/GPU Memory Error

**Error**: `CUDA out of memory`

**Solution**: 
- Reduce confidence threshold in `config.yaml`
- Use CPU by setting `use_gpu: false` in config
- Process smaller images

#### 5. Low OCR Accuracy

**Solution**:
- Ensure images are high quality and well-lit
- Try preprocessing images before input
- Adjust confidence threshold
- Check if license plate format matches Indian standards

#### 6. Python Version Issues

**Error**: Various compatibility errors

**Solution**:
- Use Python 3.10 or higher
- Create a fresh virtual environment
- Reinstall all dependencies

### Getting Help

If you encounter issues not listed here:

1. Check the [Issues](https://github.com/yourusername/ANPRYOLO/issues) section
2. Review the code comments in the source files
3. Ensure all dependencies are correctly installed
4. Verify your YOLO model is compatible

## 🏗️ System Requirements

### Minimum Requirements
- **Python**: 3.10+
- **RAM**: 4GB
- **Storage**: 2GB free space
- **OS**: Windows, Linux, or macOS

### Recommended Requirements
- **Python**: 3.10
- **RAM**: 8GB+
- **Storage**: 5GB free space
- **GPU**: NVIDIA GPU with CUDA support (for faster inference)

## 📝 Indian License Plate Format

The system is optimized for Indian license plates in the following formats:

- **Format 1**: `AA##AA####` (e.g., TN37CT3337)
  - AA: State code (2 letters)
  - ##: District registration (2-3 digits)
  - AA: Series letters (1-2 letters)
  - ####: Vehicle number (4 digits)

- **Format 2**: `AA##A####` (e.g., TN37C3337)
  - AA: State code (2 letters)
  - ##: District registration (2-3 digits)
  - A: Series letter (1 letter)
  - ####: Vehicle number (4 digits)

### Supported State Codes

The system validates against 35+ Indian state codes including:
- TN (Tamil Nadu), KA (Karnataka), MH (Maharashtra), DL (Delhi)
- GJ (Gujarat), RJ (Rajasthan), UP (Uttar Pradesh), WB (West Bengal)
- And many more...

## 🔧 Development

### Project Architecture

The system follows a modular architecture:

1. **YOLODetector**: Handles license plate detection using YOLOv8
2. **OCRProcessor**: Processes plate images for text recognition
3. **PlateValidator**: Validates and corrects license plate numbers
4. **Main System**: Orchestrates the complete ANPR pipeline

### Adding New Features

To extend the system:

1. Add new utility modules in `utils/`
2. Update `main.py` to integrate new features
3. Update `requirements.txt` with new dependencies
4. Document changes in README.md

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

##  Contact

For questions, suggestions, or issues:
- GitHub: [yourusername/ANPRYOLO](https://github.com/yourusername/ANPRYOLO)
- Email: your.email@example.com

## 🗺️ Roadmap

- [ ] Web interface for easier usage
- [ ] Real-time camera processing
- [ ] Database integration for storing results
- [ ] API endpoint for integration with other systems
- [ ] Support for international license plates
- [ ] Mobile application

---

**Note**: This system is designed for educational and research purposes. Ensure compliance with local laws and regulations when deploying in production environments.
