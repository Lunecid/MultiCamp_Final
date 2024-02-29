import torch
import sys
from PIL import Image

sys.path.insert(0, '/home/lab04/yolov5')
model = torch.load('/Users/uiw_min/Downloads/yolov5s.pt')

results = model(Image.open('./case3.jpg'))
df = results.pandas().xyxy[0].to_dict(orient='records') 

print(df)