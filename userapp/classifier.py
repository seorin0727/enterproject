import torch
from PIL import Image

def classify_image(image_path):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:/weights/last.pt')  # 가중치 경로 지정
    img = Image.open(image_path)
    results = model(img, size=640)  # 이미지 크기는 모델에 맞게 조정
    results.print()  # 결과 출력
    return results.xyxy[0]  # 반환
