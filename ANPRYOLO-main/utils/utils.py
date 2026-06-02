"""
Utility Functions Module
Helper functions for the ANPR system
"""

import os
import yaml
from pathlib import Path


def load_config(config_path='config.yaml'):
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    default_config = {
        'model_path': 'models/best.pt',
        'confidence_threshold': 0.5,
        'use_angle_cls': True,
        'ocr_language': 'en',
        'frame_skip': 5
    }
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                if config:
                    default_config.update(config)
        except Exception as e:
            print(f"Warning: Could not load config file: {e}")
            print("Using default configuration")
    else:
        print(f"Warning: Config file not found: {config_path}")
        print("Using default configuration")
    
    return default_config


def create_output_dirs(base_dir):
    """
    Create output directory structure
    
    Args:
        base_dir: Base output directory
    """
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'images'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'annotated'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'results'), exist_ok=True)


def validate_image_path(image_path):
    """
    Validate image file path
    
    Args:
        image_path: Path to image file
        
    Returns:
        True if valid, False otherwise
    """
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    return Path(image_path).suffix.lower() in valid_extensions


def validate_video_path(video_path):
    """
    Validate video file path
    
    Args:
        video_path: Path to video file
        
    Returns:
        True if valid, False otherwise
    """
    valid_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
    return Path(video_path).suffix.lower() in valid_extensions


def get_file_size(file_path):
    """
    Get file size in MB
    
    Args:
        file_path: Path to file
        
    Returns:
        File size in MB
    """
    return os.path.getsize(file_path) / (1024 * 1024)


def save_results(results, output_path):
    """
    Save detection results to text file
    
    Args:
        results: Detection results list
        output_path: Path to save results
    """
    with open(output_path, 'w') as f:
        for i, result in enumerate(results, 1):
            f.write(f"Detection {i}:\n")
            f.write(f"  Bounding Box: {result['bbox']}\n")
            f.write(f"  Confidence: {result['confidence']:.2f}\n")
            f.write(f"  Raw Text: {result['raw_text']}\n")
            f.write(f"  Plate Number: {result['plate_number']}\n")
            f.write(f"  Valid: {result['is_valid']}\n")
            f.write("\n")
