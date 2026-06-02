# Input Files Directory

Place your test images and videos in this directory for processing.

## Supported Formats

### Images
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff)

### Videos
- MP4 (.mp4)
- AVI (.avi)
- MOV (.mov)
- MKV (.mkv)
- WMV (.wmv)

## Usage Examples

```bash
# Process an image
python main.py --input inputs/test_image.jpg --type image

# Process a video
python main.py --input inputs/test_video.mp4 --type video
```

## Tips

- Use high-resolution images for better OCR accuracy
- Ensure license plates are clearly visible
- Good lighting conditions improve detection accuracy
- Avoid blurry or motion-blurred images
