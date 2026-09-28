# training/ — 주차 판정 모델 학습·서빙 기록

> **English** — The model training, Triton serving and scoring pipeline in this folder are the KickKick Park team's work from 2024, uploaded for the record. They are not the repository owner's part of the project: the owner made the district-level Tableau visualisations and built the Django website. The YOLOv8 checkpoint and training code are built on Ultralytics, which is licensed under AGPL-3.0.

## 누구의 작업인가

이 폴더의 모델 학습, Triton 서빙, 점수 파이프라인은 킥킥파크 5인 팀의 작업이다. 저장소 주인이 맡은 부분(자치구별 Tableau 시각화, 웹사이트 구축)이 아니며, 프로젝트 기록으로 남기려고 올렸다. 팀원의 개인정보 보호를 위해 이름은 적지 않았다.

## 구성

| 경로 | 내용 |
|---|---|
| `notebooks/yolo.ipynb` | YOLOv8 학습(`yolo train`)과 테스트 이미지 예측 |
| `notebooks/server.ipynb` | YOLO·Mask R-CNN ONNX 추론, 바퀴와 주차구역의 IoU 계산, 점수 규칙, Triton gRPC 클라이언트와 실행 시간 비교 |
| `notebooks/inoutCal.ipynb` | 바퀴가 주차구역 안에 있는지 IoU로 계산 |
| `dataset.yaml` | YOLO 데이터셋 설정 (클래스: parking · scooter · wheel) |
| `weights/mask_yolo.pt` | Ultralytics YOLOv8n-seg 분할 체크포인트 (클래스: parking · scooter · wheel, Ultralytics 8.1.18, 2024-03-06 저장) |
| `triton/triton/models/*/config.pbtxt` | Triton 모델 설정. 앙상블은 preprocess → mrcnn · yolo → postprocess 순서다 |
| `triton/prometheus.yml`, `triton/triton 명령어.txt` | Triton 지표를 모으는 Prometheus 설정과 Triton(22.06)·Prometheus·Grafana 실행 명령 메모 |

Triton에 올린 ONNX 모델 파일과 Python 백엔드 코드(preprocess, postprocess)는 이 저장소에 없고 설정 파일만 있다. 가중치도 `mask_yolo.pt` 하나뿐이다.

## 알아 둘 점

- 2024년 작업 당시 상태 그대로 올린 탐색용 노트북이다. 경로는 작업 서버 기준 절대 경로(`/root/...`)이고, 그대로는 실행되지 않는 셀도 있다.
- 세 노트북의 출력을 보면 NVIDIA GeForce RTX 3060 Ti GPU 환경(Python 3.11, PyTorch 2.2)에서 실행했고, 학습에는 Ultralytics 8.1을 썼다.
- 점수 규칙(최대 20점, 저장소 README §5)은 `server.ipynb`의 로컬 프로토타입에서만 돌렸다. 공개 Django 데모(저장소 루트)는 이 파이프라인과 연결되어 있지 않고, 사진을 올릴 때마다 고정 점수(+10)를 쌓는다. 점수 계산 셀도 2024년 코드를 고치지 않고 그대로 두었다.
- Triton 서버 주소는 `TRITON_HOST` 자리표시자로 바꿨다. 노트북에서는 환경 변수 `TRITON_HOST`로, `prometheus.yml`에서는 `TRITON_HOST` 자리에 서버 주소를 넣어 쓴다.
- 공개 저장소에 올리면서 일부 셀의 출력을 지웠다. 테스트 이미지 예측 결과, 학습 로그, 서버 주소가 찍힌 연결 오류가 그 대상이다. 코드는 그대로다.

## 데이터

- 학습 이미지는 이 저장소에 없다. `dataset.yaml`에는 작업 서버의 경로와 클래스 이름만 있고, 데이터 출처나 라이선스는 적혀 있지 않다.
- 1차 모델은 Roboflow 공개 데이터로 학습했고, 2차부터는 팀이 직접 찍고 Labelme로 라벨링한 사진(증강 후 1,429장)을 썼다(저장소 README §4).
- `yolo.ipynb`에서 예측을 돌린 `test_img/real` 폴더는 학습 데이터 폴더와 별개이고, 출처가 제3자인 이미지가 섞여 있다. 그래서 그 예측 출력은 지웠고, 이미지도 올리지 않았다.

## 라이선스

`weights/mask_yolo.pt`와 학습 노트북은 Ultralytics YOLOv8로 만들었다. Ultralytics는 AGPL-3.0으로 배포되므로, 이 가중치와 코드를 다시 쓰거나 배포할 때는 AGPL-3.0 조건을 따라야 한다.
