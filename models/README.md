# Model Information - ANPRYOLO

This directory contains the YOLOv8 model weights for license plate detection.

## Included Model

- **Filename**: `best.pt`
- **Format**: PyTorch model weights
- **Architecture**: YOLOv8
- **Purpose**: Indian license plate detection

The model is already included and ready to use. No additional download is required.

## Model Specifications

- **Input Size**: 640x640
- **Classes**: 1 (license_plate)
- **Format**: PyOLOv8 PyTorch (.pt file)
- **Training**: Trained on Indian license plate dataset

## Using a Different Model

If you wish to use a different YOLO model:

1. Place your model file in this directory
2. Rename it to `best.pt` (or update the path in `config.yaml`)
3. Update `config.yaml` to point to your model:
   ```yaml
   model_path: models/your_model.pt
   ```

## Training Your Own Model

If you want to train your own model:

1. Collect a dataset of Indian license plate images
2. Annotate the images using tools like LabelImg or Roboflow
3. Train using YOLOv8:
   ```bash
   yolo detect train data=your_dataset.yaml model=yolov8n.pt epochs=100
   ```
4. Copy the best weights to this directory as `best.pt`

## Troubleshooting

### Model Not Found Error

If you get "Model file not found: models/best.pt":
1. Ensure the model file is in this directory
2. Check the filename is exactly `best.pt`
3. Verify the path in `config.yaml`

### Model Loading Issues

If the model fails to load:
1. Ensure you have compatible PyTorch version
2. Check if the model is corrupted
3. Try downloading the model again

### Poor Detection Accuracy

If detection accuracy is poor:
1. Ensure you're using a model trained on Indian license plates
2. Check input image quality
3. Adjust confidence threshold in `config.yaml`
4. Try a different model (larger models like YOLOv8m may work better)

## Model Performance

Expected performance with properly trained models:
- **YOLOv8n**: Fast (~5ms per image), good accuracy (~85%)
- **YOLOv8s**: Balanced (~8ms per image), better accuracy (~90%)
- **YOLOv8m**: Slower (~15ms per image), high accuracy (~95%)
- **YOLOv8l**: Slowest (~25ms per image), best accuracy (~97%)

Choose based on your speed vs accuracy requirements.
