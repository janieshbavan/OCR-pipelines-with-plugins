#!/usr/bin/env python3
"""
ANPRYOLO - Automatic Number Plate Recognition System
Main entry point for the ANPR system using YOLOv8 and PaddleOCR

Date: 2026
"""

import os
import sys
import argparse
import cv2
import numpy as np
from pathlib import Path

# Add utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))

from detector import YOLODetector
from ocr_processor import OCRProcessor
from plate_validator import PlateValidator
from utils import load_config, create_output_dirs


class ANPRSystem:
    """Main ANPR System class"""
    
    def __init__(self, config_path='config.yaml'):
        """
        Initialize ANPR system with configuration
        
        Args:
            config_path: Path to configuration file
        """
        self.config = load_config(config_path)
        self.detector = YOLODetector(
            model_path=self.config['model_path'],
            confidence_threshold=self.config.get('confidence_threshold', 0.5)
        )
        self.ocr_processor = OCRProcessor(
            use_angle_cls=self.config.get('use_angle_cls', True),
            lang=self.config.get('ocr_language', 'en')
        )
        self.validator = PlateValidator()
        
    def process_image(self, image_path, output_dir=None):
        """
        Process a single image for license plate detection and recognition
        
        Args:
            image_path: Path to input image
            output_dir: Directory to save results
            
        Returns:
            List of detected plates with information
        """
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Cannot read image: {image_path}")
        
        # Detect plates
        detections = self.detector.detect(image)
        
        # Process each detection
        results = []
        for idx, detection in enumerate(detections):
            x1, y1, x2, y2 = detection['bbox']
            confidence = detection['confidence']
            
            # Extract plate region
            plate_crop = image[y1:y2, x1:x2]
            
            # Save intermediate steps if output directory provided
            if output_dir:
                step_dir = os.path.join(output_dir, 'steps', f'detection_{idx}')
                os.makedirs(step_dir, exist_ok=True)
                
                # Save original crop
                crop_path = os.path.join(step_dir, '1_original_crop.jpg')
                cv2.imwrite(crop_path, plate_crop)
            
            # Preprocess plate
            gray, thresh = self.ocr_processor.preprocess_plate(plate_crop)
            
            # Save preprocessing steps if output directory provided
            if output_dir:
                gray_path = os.path.join(step_dir, '2_preprocessed_gray.jpg')
                thresh_path = os.path.join(step_dir, '3_preprocessed_thresh.jpg')
                cv2.imwrite(gray_path, gray)
                cv2.imwrite(thresh_path, thresh)
            
            # OCR recognition
            ocr_result = self.ocr_processor.recognize_text((gray, thresh))
            
            # Validate plate
            validated_plate = self.validator.validate_and_correct(ocr_result)
            
            result = {
                'bbox': [x1, y1, x2, y2],
                'confidence': confidence,
                'raw_text': ocr_result,
                'plate_number': validated_plate,
                'is_valid': validated_plate is not None
            }
            results.append(result)
        
        # Save annotated image if output directory provided
        if output_dir:
            self._save_annotated_image(image, results, output_dir, Path(image_path).stem)
            self._save_processing_steps(results, output_dir, Path(image_path).stem)
        
        return results
    
    def process_video(self, video_path, output_dir=None, frame_skip=5):
        """
        Process video for license plate detection
        
        Args:
            video_path: Path to input video
            output_dir: Directory to save results
            frame_skip: Process every Nth frame
            
        Returns:
            List of unique plates detected
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")
        
        all_plates = []
        seen_plates = set()
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Skip frames
            if frame_count % frame_skip != 0:
                continue
            
            try:
                # Detect plates
                detections = self.detector.detect(frame)
                
                # Process detections
                for detection in detections:
                    x1, y1, x2, y2 = detection['bbox']
                    plate_crop = frame[y1:y2, x1:x2]
                    
                    # OCR
                    preprocessed = self.ocr_processor.preprocess_plate(plate_crop)
                    ocr_result = self.ocr_processor.recognize_text(preprocessed)
                    validated_plate = self.validator.validate_and_correct(ocr_result)
                    
                    if validated_plate and validated_plate not in seen_plates:
                        seen_plates.add(validated_plate)
                        all_plates.append({
                            'plate_number': validated_plate,
                            'frame_number': frame_count,
                            'confidence': detection['confidence']
                        })
            
            except Exception as e:
                print(f"Error processing frame {frame_count}: {e}")
                continue
        
        cap.release()
        return all_plates
    
    def _save_annotated_image(self, image, results, output_dir, image_name):
        """Save image with bounding boxes and plate numbers"""
        annotated = image.copy()
        
        for result in results:
            x1, y1, x2, y2 = result['bbox']
            plate_number = result['plate_number']
            is_valid = result['is_valid']
            
            color = (0, 255, 0) if is_valid else (0, 0, 255)
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
            
            if plate_number:
                cv2.putText(annotated, plate_number, (x1, max(y1-10, 20)),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        
        output_path = os.path.join(output_dir, f"{image_name}_annotated.jpg")
        cv2.imwrite(output_path, annotated)
        print(f"Saved annotated image: {output_path}")
    
    def _save_processing_steps(self, results, output_dir, image_name):
        """Save detailed processing steps information"""
        steps_path = os.path.join(output_dir, f"{image_name}_processing_steps.txt")
        
        with open(steps_path, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write(f"PROCESSING STEPS FOR: {image_name}\n")
            f.write("=" * 70 + "\n\n")
            
            for idx, result in enumerate(results, 1):
                f.write(f"Detection {idx}:\n")
                f.write("-" * 50 + "\n")
                f.write(f"Bounding Box: {result['bbox']}\n")
                f.write(f"Detection Confidence: {result['confidence']:.4f}\n")
                f.write(f"Raw OCR Text: {result['raw_text']}\n")
                f.write(f"Validated Plate Number: {result['plate_number']}\n")
                f.write(f"Is Valid: {result['is_valid']}\n")
                f.write(f"\nIntermediate Steps Saved:\n")
                f.write(f"  - steps/detection_{idx-1}/1_original_crop.jpg\n")
                f.write(f"  - steps/detection_{idx-1}/2_preprocessed_gray.jpg\n")
                f.write(f"  - steps/detection_{idx-1}/3_preprocessed_thresh.jpg\n")
                f.write("\n")
        
        print(f"Saved processing steps: {steps_path}")


def main():
    """Main function to run ANPR system"""
    parser = argparse.ArgumentParser(description='ANPRYOLO - ANPR System')
    parser.add_argument('--input', '-i', required=True, help='Input image or video path')
    parser.add_argument('--output', '-o', default='outputs', help='Output directory')
    parser.add_argument('--config', '-c', default='config.yaml', help='Configuration file')
    parser.add_argument('--type', '-t', choices=['image', 'video'], default='image',
                       help='Input type (image or video)')
    parser.add_argument('--frame-skip', type=int, default=5,
                       help='Frame skip for video processing')
    
    args = parser.parse_args()
    
    # Create output directories
    create_output_dirs(args.output)
    
    # Initialize ANPR system
    print("Initializing ANPR System...")
    anpr = ANPRSystem(args.config)
    print("ANPR System initialized successfully!")
    
    # Process input
    input_path = args.input
    
    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)
    
    print(f"\nProcessing {args.type}: {input_path}")
    
    if args.type == 'image':
        results = anpr.process_image(input_path, args.output)
        
        print(f"\nDetection Results:")
        print("=" * 50)
        for i, result in enumerate(results, 1):
            print(f"\nDetection {i}:")
            print(f"  Bounding Box: {result['bbox']}")
            print(f"  Confidence: {result['confidence']:.2f}")
            print(f"  Raw Text: {result['raw_text']}")
            print(f"  Plate Number: {result['plate_number']}")
            print(f"  Valid: {result['is_valid']}")
    
    elif args.type == 'video':
        results = anpr.process_video(input_path, args.output, args.frame_skip)
        
        print(f"\nDetection Results:")
        print("=" * 50)
        print(f"Total unique plates detected: {len(results)}")
        for i, result in enumerate(results, 1):
            print(f"\nPlate {i}:")
            print(f"  Plate Number: {result['plate_number']}")
            print(f"  Frame: {result['frame_number']}")
            print(f"  Confidence: {result['confidence']:.2f}")
    
    print(f"\nResults saved to: {args.output}")
    print("Processing complete!")


if __name__ == "__main__":
    main()
