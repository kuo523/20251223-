from ultralytics import YOLO

model = YOLO('./runs/detect/train16/weights/best.pt') #將模型改成'best.pt'或其他訓練過的模型名稱
results = model.train(data="./aortic_valve_colab.yaml",
            resume = True
            )