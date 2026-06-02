"""
YOLOv8 License Plate Detector Module
Handles YOLO-based license plate detection
"""

import cv2
import numpy as np
import torch
from pathlib import Path
from ultralytics import YOLO


class YOLODetector:
    """YOLOv8-based license plate detector"""
    
    def __init__(self, model_path, confidence_threshold=0.5):
        """
        Initialize YOLO detector
        
        Args:
            model_path: Path to YOLO model weights (.pt file)
            confidence_threshold: Minimum confidence for detection
        """
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.model = None
        
        self._load_model()
    
    def _load_model(self):
        """Load YOLO model with PyTorch 2.6 compatibility handling"""
        if not Path(self.model_path).exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        
        try:
            # Try normal loading
            self.model = YOLO(self.model_path)
        except Exception as e:
            if "weights_only" in str(e):
                # Handle PyTorch 2.6 security restrictions
                try:
                    from ultralytics.nn.tasks import DetectionModel
                    import torch.nn as nn
                    torch.serialization.add_safe_globals([
                        DetectionModel,
                        nn.Sequential,
                        nn.Module,
                        nn.Conv2d,
                        nn.BatchNorm2d,
                        nn.ReLU,
                        nn.SiLU,
                        nn.Upsample,
                        nn.Identity,
                    ])
                    self.model = YOLO(self.model_path)
                except Exception:
                    # Last resort: temporarily disable weights_only
                    import warnings
                    warnings.warn("Loading YOLO model with weights_only=False for compatibility")
                    original_load = torch.load
                    def patched_load(*args, **kwargs):
                        kwargs['weights_only'] = False
                        return original_load(*args, **kwargs)
                    torch.load = patched_load
                    try:
                        self.model = YOLO(self.model_path)
                    finally:
                        torch.load = original_load
            else:
                raise e
        
        print(f"YOLO model loaded successfully from: {self.model_path}")
    
    def detect(self, image):
        """
        Detect license plates in image
        
        Args:
            image: Input image (numpy array)
            
        Returns:
            List of detections with bbox and confidence
        """
        results = self.model.predict(image, conf=self.confidence_threshold, verbose=False)
        detections = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                if box.cls == 0:  # License plate class
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    confidence = float(box.conf[0].cpu().numpy())
                    
                    detections.append({
                        'bbox': [x1, y1, x2, y2],
                        'confidence': confidence
                    })
        
        return detections
    
    def detect_with_padding(self, image, padding_ratio=0.15):
        """
        Detect plates with padding around bounding box
        
        Args:
            image: Input image
            padding_ratio: Padding ratio (15% by default)
            
        Returns:
            List of detections with padded bounding boxes
        """
        detections = self.detect(image)
        h, w = image.shape[:2]
        
        padded_detections = []
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            
            # Add padding
            pad_x = int((x2 - x1) * padding_ratio)
            pad_y = int((y2 - y1) * padding_ratio)
            
            x1p = max(0, x1 - pad_x)
            y1p = max(0, y1 - pad_y)
            x2p = min(w, x2 + pad_x)
            y2p = min(h, y2 + pad_y)
            
            padded_detections.append({
                'bbox': [x1p, y1p, x2p, y2p],
                'confidence': det['confidence']
            })
        
        return padded_detections
