from ultralytics import YOLO

# 1. 載入剛訓練好的最佳權重
# 路徑通常在 runs/detect/您的專案名稱/weights/best.pt
# 根據您的程式碼，名稱是 'train_final_hyp1'
#model = YOLO('runs/detect/train_final_hyp1/weights/best.pt')
model = YOLO('./best.pt')
# 2. 執行驗證 (Validation)
# split='val' 代表使用 data.yaml 裡面的 val 資料集進行測試
metrics = model.val(data='./data.yaml', split='val')

# 3. 輸出 mAP50 結果
print(f"mAP50: {metrics.box.map50}")
print(f"mAP50-95: {metrics.box.map}") # 這是 mAP50-95，更嚴格的標準