from ultralytics import YOLO
import torch
# Load a model
if __name__ == '__main__':
    model = YOLO('yolov8n.pt')  # load a pretrained model (recommended for training)

# Train the model with 2 GPUs
    results = model.train(data='coco128.yaml', epochs=100, imgsz=640, device="0")