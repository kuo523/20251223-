from ultralytics import YOLO

model = YOLO('best.pt')
results = model.predict(source="./datasets/test/images2/",
              save=True,
              imgsz=512,
              device=0,
              conf = 0.5,
              max_det=1,
              augment=True,
              single_cls=True
              )

output_file = open('./predict_txt/images2.txt', 'w')
for i in range(len(results)):

    filename = results[i].path.split('/')[-1].split('.png')[0]

    boxes = results[i].boxes
    box_num = len(boxes.cls.tolist())

    if box_num > 0:
        for j in range(box_num):
            label = int(boxes.cls[j].item())
            conf = boxes.conf[j].item()      
            x1, y1, x2, y2 = boxes.xyxy[j].tolist() 

            line = f"{filename} {label} {conf:.4f} {int(x1)} {int(y1)} {int(x2)} {int(y2)}\n"
            output_file.write(line)

output_file.close()