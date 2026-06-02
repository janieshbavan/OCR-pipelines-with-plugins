# """
# OCR Processing Module
# Handles text recognition from license plate images using PaddleOCR
# """

# import cv2
# import numpy as np
# from paddleocr import PaddleOCR
# import re


# class OCRProcessor:
#     """OCR processor for license plate text recognition"""
    
#     def __init__(self, use_angle_cls=True, lang='en'):
#         """
#         Initialize OCR processor
        
#         Args:
#             use_angle_cls: Use angle classification for rotated text
#             lang: Language for OCR (default: English)
#         """
#         self.use_angle_cls = use_angle_cls
#         self.lang = lang
#         self.ocr_engine = None
        
#         self._load_model()
    
#     def _load_model(self):
#         """Load PaddleOCR model"""
#         try:
#             self.ocr_engine = PaddleOCR(use_angle_cls=self.use_angle_cls, lang=self.lang)
#             print("PaddleOCR model loaded successfully")
#         except Exception as e:
#             raise RuntimeError(f"Failed to load PaddleOCR model: {e}")
    
#     def preprocess_plate(self, plate_image):
#         """
#         Preprocess license plate image for better OCR
        
#         Args:
#             plate_image: Cropped license plate image
            
#         Returns:
#             Preprocessed image variants for OCR
#         """
#         # Resize 2x with cubic interpolation
#         resized = cv2.resize(plate_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        
#         # Convert to grayscale
#         gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        
#         # Bilateral filter for noise reduction
#         gray = cv2.bilateralFilter(gray, 11, 17, 17)
        
#         # Histogram equalization for contrast enhancement
#         gray = cv2.equalizeHist(gray)
        
#         # Adaptive thresholding
#         thresh = cv2.adaptiveThreshold(
#             gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
#             cv2.THRESH_BINARY, 11, 3
#         )
        
#         # Morphological operations
#         kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
#         thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        
#         return gray, thresh
    
#     def recognize_text(self, image_variants):
#         """
#         Recognize text from preprocessed image variants
        
#         Args:
#             image_variants: Tuple of (gray_image, threshold_image)
            
#         Returns:
#             Recognized text string
#         """
#         if not self.ocr_engine:
#             raise RuntimeError("OCR model not loaded")
        
#         all_texts = []
        
#         # Process both image variants
#         for variant in image_variants:
#             try:
#                 result = self.ocr_engine.ocr(variant, cls=True)
#                 if result and result[0]:
#                     for line in result[0]:
#                         text = line[1][0]
#                         all_texts.append(text)
#             except Exception as e:
#                 print(f"OCR error: {e}")
#                 continue
        
#         # Clean and combine results
#         if all_texts:
#             combined = "".join(all_texts)
#             cleaned = self._clean_text(combined)
#             return cleaned
        
#         return ""
    
#     def _clean_text(self, text):
#         """
#         Clean OCR text by removing noise and special characters
        
#         Args:
#             text: Raw OCR text
            
#         Returns:
#             Cleaned text
#         """
#         # Remove special characters
#         text = re.sub(r'[^A-Z0-9]', '', text.upper())
        
#         # Remove common noise words
#         noise_words = ['IND', 'ND', 'IN', 'INDIA', 'BHARAT']
#         for word in noise_words:
#             text = text.replace(word, '')
        
#         # Remove any remaining special characters
#         text = re.sub(r'[^A-Z0-9]', '', text)
        
#         return text
    
#     def recognize_multi_line(self, image_variants):
#         """
#         Recognize text from multi-line plates
        
#         Args:
#             image_variants: Tuple of (gray_image, threshold_image)
            
#         Returns:
#             Recognized text with multi-line handling
#         """
#         if not self.ocr_engine:
#             raise RuntimeError("OCR model not loaded")
        
#         all_results = []
        
#         for variant in image_variants:
#             try:
#                 result = self.ocr_engine.ocr(variant, cls=True)
#                 if result and result[0]:
#                     # Sort by Y-coordinate for line detection
#                     lines = sorted(result[0], key=lambda x: x[0][0][1])
                    
#                     # Check for multi-line (significant Y-gap)
#                     if len(lines) > 1:
#                         y_coords = [line[0][0][1] for line in lines]
#                         gaps = [y_coords[i+1] - y_coords[i] for i in range(len(y_coords)-1)]
#                         avg_gap = sum(gaps) / len(gaps) if gaps else 0
                        
#                         if avg_gap > 15:  # Multi-line detected
#                             # Group by lines
#                             line_groups = []
#                             current_line = [lines[0]]
#                             current_y = lines[0][0][0][1]
                            
#                             for line in lines[1:]:
#                                 if abs(line[0][0][1] - current_y) < avg_gap * 0.5:
#                                     current_line.append(line)
#                                 else:
#                                     current_line.sort(key=lambda x: x[0][0][0])  # Sort by X
#                                     line_groups.append(current_line)
#                                     current_line = [line]
#                                     current_y = line[0][0][1]
                            
#                             current_line.sort(key=lambda x: x[0][0][0])
#                             line_groups.append(current_line)
                            
#                             # Combine lines
#                             combined_text = ""
#                             for group in line_groups:
#                                 line_text = "".join([l[1][0] for l in group])
#                                 combined_text += line_text
                            
#                             all_results.append(combined_text)
#                         else:
#                             # Single line
#                             text = "".join([line[1][0] for line in lines])
#                             all_results.append(text)
#                     else:
#                         text = lines[0][1][0] if lines else ""
#                         all_results.append(text)
            
#             except Exception as e:
#                 print(f"OCR error: {e}")
#                 continue
        
#         # Return best result
#         if all_results:
#             cleaned_results = [self._clean_text(text) for text in all_results]
#             return max(cleaned_results, key=len) if cleaned_results else ""
        
#         return ""
"""
OCR Processing Module
Handles text recognition from license plate images using PaddleOCR
"""

import cv2
import numpy as np
from paddleocr import PaddleOCR
import re


class OCRProcessor:
    """OCR processor for license plate text recognition"""
    
    def __init__(self, use_angle_cls=True, lang='en', drop_score=0.3):  # ADD drop_score parameter
        """
        Initialize OCR processor
        
        Args:
            use_angle_cls: Use angle classification for rotated text
            lang: Language for OCR (default: English)
            drop_score: Confidence threshold for OCR (0-1, lower = more text accepted)
        """
        self.use_angle_cls = use_angle_cls
        self.lang = lang
        self.drop_score = drop_score  # Store threshold
        self.ocr_engine = None
        
        self._load_model()
    
    def _load_model(self):
        """Load PaddleOCR model with drop_score parameter"""
        try:
            self.ocr_engine = PaddleOCR(
                use_angle_cls=self.use_angle_cls, 
                lang=self.lang,
                drop_score=self.drop_score  # PASS THRESHOLD TO PaddleOCR
            )
            print(f"PaddleOCR model loaded successfully (confidence threshold: {self.drop_score})")
        except Exception as e:
            raise RuntimeError(f"Failed to load PaddleOCR model: {e}")
    
    def preprocess_plate(self, plate_image):
        """
        Preprocess license plate image for better OCR
        
        Args:
            plate_image: Cropped license plate image
            
        Returns:
            Preprocessed image variants for OCR
        """
        # Resize 2x with cubic interpolation
        resized = cv2.resize(plate_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        
        # Convert to grayscale
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        
        # Bilateral filter for noise reduction
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        
        # Histogram equalization for contrast enhancement
        gray = cv2.equalizeHist(gray)
        
        # Adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY, 11, 3
        )
        
        # Morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        
        return gray, thresh
    
    def recognize_text(self, image_variants):
        """
        Recognize text from preprocessed image variants
        
        Args:
            image_variants: Tuple of (gray_image, threshold_image)
            
        Returns:
            Recognized text string
        """
        if not self.ocr_engine:
            raise RuntimeError("OCR model not loaded")
        
        all_texts = []
        all_confidences = []
        
        # Process both image variants
        for variant in image_variants:
            try:
                result = self.ocr_engine.ocr(variant, cls=True)
                if result and result[0]:
                    for line in result[0]:
                        # PaddleOCR returns: [[[x1,y1], [x2,y2], [x3,y3], [x4,y4]], (text, confidence)]
                        text = line[1][0]
                        confidence = line[1][1]
                        
                        # Optional: Print confidence for debugging
                        # print(f"OCR detected: '{text}' with confidence {confidence:.3f}")
                        
                        # Only add if confidence meets threshold
                        if confidence >= self.drop_score:
                            all_texts.append(text)
                            all_confidences.append(confidence)
            except Exception as e:
                print(f"OCR error: {e}")
                continue
        
        # Clean and combine results
        if all_texts:
            # Get the text with highest confidence
            if all_confidences:
                best_idx = all_confidences.index(max(all_confidences))
                best_text = all_texts[best_idx]
            else:
                best_text = "".join(all_texts)
            
            cleaned = self._clean_text(best_text)
            return cleaned
        
        return ""
    
    def recognize_with_confidence(self, image_variants):
        """
        Recognize text and return confidence scores
        
        Args:
            image_variants: Tuple of (gray_image, threshold_image)
            
        Returns:
            Tuple of (text, confidence, all_results)
        """
        if not self.ocr_engine:
            raise RuntimeError("OCR model not loaded")
        
        all_results = []
        
        for variant in image_variants:
            try:
                result = self.ocr_engine.ocr(variant, cls=True)
                if result and result[0]:
                    for line in result[0]:
                        text = line[1][0]
                        confidence = line[1][1]
                        all_results.append({
                            'text': text,
                            'confidence': confidence,
                            'variant': 'gray' if variant is image_variants[0] else 'thresh'
                        })
            except Exception as e:
                print(f"OCR error: {e}")
                continue
        
        if all_results:
            # Sort by confidence
            all_results.sort(key=lambda x: x['confidence'], reverse=True)
            best = all_results[0]
            cleaned = self._clean_text(best['text'])
            return cleaned, best['confidence'], all_results
        
        return "", 0.0, []
    
    def _clean_text(self, text):
        """
        Clean OCR text by removing noise and special characters
        
        Args:
            text: Raw OCR text
            
        Returns:
            Cleaned text
        """
        # Remove special characters
        text = re.sub(r'[^A-Z0-9]', '', text.upper())
        
        # Remove common noise words
        noise_words = ['IND', 'ND', 'IN', 'INDIA', 'BHARAT']
        for word in noise_words:
            text = text.replace(word, '')
        
        # Remove any remaining special characters
        text = re.sub(r'[^A-Z0-9]', '', text)
        
        return text
    
    def recognize_multi_line(self, image_variants):
        """
        Recognize text from multi-line plates
        
        Args:
            image_variants: Tuple of (gray_image, threshold_image)
            
        Returns:
            Recognized text with multi-line handling
        """
        if not self.ocr_engine:
            raise RuntimeError("OCR model not loaded")
        
        all_results = []
        
        for variant in image_variants:
            try:
                result = self.ocr_engine.ocr(variant, cls=True)
                if result and result[0]:
                    # Sort by Y-coordinate for line detection
                    lines = sorted(result[0], key=lambda x: x[0][0][1])
                    
                    # Check for multi-line (significant Y-gap)
                    if len(lines) > 1:
                        y_coords = [line[0][0][1] for line in lines]
                        gaps = [y_coords[i+1] - y_coords[i] for i in range(len(y_coords)-1)]
                        avg_gap = sum(gaps) / len(gaps) if gaps else 0
                        
                        if avg_gap > 15:  # Multi-line detected
                            # Group by lines
                            line_groups = []
                            current_line = [lines[0]]
                            current_y = lines[0][0][0][1]
                            
                            for line in lines[1:]:
                                if abs(line[0][0][1] - current_y) < avg_gap * 0.5:
                                    current_line.append(line)
                                else:
                                    current_line.sort(key=lambda x: x[0][0][0])  # Sort by X
                                    line_groups.append(current_line)
                                    current_line = [line]
                                    current_y = line[0][0][1]
                            
                            current_line.sort(key=lambda x: x[0][0][0])
                            line_groups.append(current_line)
                            
                            # Combine lines with confidence filtering
                            combined_text = ""
                            for group in line_groups:
                                # Filter by confidence within the group
                                valid_texts = []
                                for line in group:
                                    if line[1][1] >= self.drop_score:
                                        valid_texts.append(line[1][0])
                                line_text = "".join(valid_texts)
                                combined_text += line_text
                            
                            all_results.append(combined_text)
                        else:
                            # Single line - filter by confidence
                            text = ""
                            for line in lines:
                                if line[1][1] >= self.drop_score:
                                    text += line[1][0]
                            all_results.append(text)
                    else:
                        text = lines[0][1][0] if lines and lines[0][1][1] >= self.drop_score else ""
                        all_results.append(text)
            
            except Exception as e:
                print(f"OCR error: {e}")
                continue
        
        # Return best result
        if all_results:
            cleaned_results = [self._clean_text(text) for text in all_results if text]
            return max(cleaned_results, key=len) if cleaned_results else ""
        
        return ""