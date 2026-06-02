# Quick Start Guide - ANPRYOLO

## 5-Minute Setup

### 1. Extract/Clone the Project
```bash
cd ANPRYOLO
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. YOLO Model
The YOLOv8 model (best.pt) is already included in the `models/` directory. No additional download required.

### 5. Run the System
```bash
# For image processing
python main.py --input inputs/test_image.jpg --type image

# For video processing
python main.py --input inputs/test_video.mp4 --type video
```

## That's It! 🎉

The system is ready to detect Indian license plates with high accuracy.

For detailed information, see README.md
