import shutil
import os
#移動檔案
def find_patient_root(root):
    """往下找，直到找到含有 patientXXXX 的資料夾"""
    for dirpath, dirnames, filenames in os.walk(root):
        if any(d.startswith("patient") for d in dirnames):
            return dirpath
    return root  # fallback


IMG_ROOT = find_patient_root("./training_image")
LBL_ROOT = find_patient_root("./training_label")

print("IMG_ROOT =", IMG_ROOT)
print("LBL_ROOT =", LBL_ROOT)

# 建立並清空輸出資料夾（若存在）
def ensure_clean_dir(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)

ensure_clean_dir("./datasets/train/images")
ensure_clean_dir("./datasets/train/labels")
ensure_clean_dir("./datasets/val/images")
ensure_clean_dir("./datasets/val/labels")
"""
def move_patients(start, end, split):
    for i in range(start, end + 1):
        patient = f"patient{i:04d}"
        img_dir = os.path.join(IMG_ROOT, patient)
        lbl_dir = os.path.join(LBL_ROOT, patient)
        
        # 檢查圖片資料夾是否存在
        if not os.path.isdir(img_dir):
            continue

        # ⚠️ 修改邏輯：遍歷「圖片資料夾」而不是標記資料夾
        for fname in os.listdir(img_dir):
            if not fname.endswith(".png"): # 假設圖片是 png
                continue

            base, _ = os.path.splitext(fname)
            img_src = os.path.join(img_dir, fname)
            lbl_src = os.path.join(lbl_dir, base + ".txt")

            # 複製圖片
            shutil.copy2(img_src, f"./datasets/{split}/images/")

            # 檢查是否有標記檔
            if os.path.exists(lbl_src):
                # 有標記，複製過去
                shutil.copy2(lbl_src, f"./datasets/{split}/labels/")
            else:
                # ❌ 沒有標記檔 = 這是背景圖片
                # 為了讓 YOLO 知道這是背景，我們不需要做任何事 (不用複製 txt)
                # 或者如果您想要保險一點，可以建立一個空的 txt
                # with open(f"./datasets/{split}/labels/{base}.txt", 'w') as f:
                #     pass
                print(f"加入背景圖片 (無標記): {fname}")
"""

def move_patients(start, end, split):
    for i in range(start, end + 1):
        patient = f"patient{i:04d}"
        img_dir = os.path.join(IMG_ROOT, patient)
        lbl_dir = os.path.join(LBL_ROOT, patient)
        if not os.path.isdir(lbl_dir):
            continue

        for fname in os.listdir(lbl_dir):
            if not fname.endswith(".txt"):
                continue

            label_path = os.path.join(lbl_dir, fname)
            base, _ = os.path.splitext(fname)  # 取出檔名不含副檔名
            img_path = os.path.join(img_dir, base + ".png")
            if not os.path.exists(img_path):
                print(f"找不到對應圖片: {img_path}")
                continue

            shutil.copy2(img_path, f"./datasets/{split}/images/")
            shutil.copy2(label_path, f"./datasets/{split}/labels/")

# patient0001~0030 → train
move_patients(1, 40, "train")

# patient0031~0050 → val
move_patients(41, 50, "val")

print("完成移動！")
