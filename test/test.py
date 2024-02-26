import torch
import sys
from PIL import Image

# torch.hub를 사용하여 YOLOv5 'custom' 모델 로드
# 'path' 인자를 통해 사용자 정의 모델 가중치의 경로를 지정
#i)
# model = torch.hub.load('ultralytics/yolov5', 'custom', path='/home/lab07/yolov5/runs/train/scooter/weights/last.pt')
#ii)
sys.path.insert(0, '/home/lab07/yolov5')
model = torch.load('../MultiCamp_Final/model/scooter.pt')

results = model(Image.open('./case3.jpg'))
df = results.pandas().xyxy[0].to_dict(orient='records') 

print(df)