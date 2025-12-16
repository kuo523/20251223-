from ultralytics import YOLO

# 1. 載入模型
model = YOLO('yolo12n.pt') 

# 2. 開始訓練
results = model.train(
    # --- 核心訓練設定 ---
    data="./data.yaml",   
    epochs=150,            
    patience=20,
    batch=32,
    imgsz=640,
    device=0,
)