from ultralytics import YOLO

# 載入模型 (以 YOLO12n 為例)
model = YOLO('yolo12n.pt') 

# -----------------------------------------------------------
# 2. 開始調優 (Tuning)
# -----------------------------------------------------------

# 您需要將訓練的參數傳遞給 tune 方法
# 注意：epochs 應該設得較低 (例如 5-15)，以節省總體優化時間。

model.tune(
    data="./data.yaml",
    epochs=10,        # 每次進化的訓練輪數（設定較短）
    iterations=50,    # 👈 這是 TUNE 模式下進行的進化次數 (即您想測試多少組參數)
    optimizer='AdamW',
    batch=32,
    imgsz=640,
    device=0,
    workers=8,
    
    # === 遺傳算法設定 ===
    # 這裡的 patience, close_mosaic, scale, box 等會作為調優的「起點」
    patience=10,
    close_mosaic=10,
    scale=0.8,
    box=10.0,
    max_det=1,       
    iou=0.0,        
    single_cls=True,
    mixup=0.5,
    degrees=0.3,
    # 其他您希望自動變異的超參數，如 lr0 (初始學習率), lrf (最終學習率)
    lr0=0.01,
    lrf=0.01,
)

print("優化完成！最佳超參數已儲存。")