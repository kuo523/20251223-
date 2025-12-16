import shutil # 用於檔案的高級操作，例如複製整個資料夾或檔案
import os     # 用於與作業系統互動，例如處理檔案路徑、列出目錄內容

# --- 1. 定位病患資料夾根目錄 ---
def find_patient_root(root):
    """往下找，直到找到含有 patientXXXX 的資料夾"""
    # os.walk() 會遞迴遍歷目錄樹
    for dirpath, dirnames, filenames in os.walk(root):
        # 檢查當前目錄下是否存在任何以 "patient" 開頭的資料夾
        if any(d.startswith("patient") for d in dirnames):
            # 找到根目錄，返回當前路徑
            return dirpath
    # 如果找不到，則返回起始搜尋路徑 (作為備用/預設值)
    return root # fallback


# 呼叫函式，自動找到包含 patientXXXX 子資料夾的根目錄
IMG_ROOT = find_patient_root("./training_image")
LBL_ROOT = find_patient_root("./training_label")

# 輸出找到的路徑，方便使用者確認是否正確
print("IMG_ROOT =", IMG_ROOT)
print("LBL_ROOT =", LBL_ROOT)

# --- 2. 建立並清空輸出資料夾 ---
def ensure_clean_dir(path):
    """檢查路徑是否存在，如果存在則刪除，然後建立新的空資料夾"""
    if os.path.isdir(path):
        # 如果資料夾存在，遞迴刪除整個資料夾及其內容
        shutil.rmtree(path)
    # 建立新的資料夾 (exist_ok=True 避免重複建立時報錯，但因為上面已刪除，此處主要功能是建立)
    os.makedirs(path, exist_ok=True)

# 建立 YOLO 訓練所需的標準資料夾結構，並清空舊內容
ensure_clean_dir("./datasets/train/images") # 訓練集圖片
ensure_clean_dir("./datasets/train/labels") # 訓練集標籤 (YOLO .txt)
ensure_clean_dir("./datasets/val/images")   # 驗證集圖片
ensure_clean_dir("./datasets/val/labels")   # 驗證集標籤 (YOLO .txt)

# --- 3. 核心邏輯：依病患 ID 複製檔案 ---
def move_patients(start, end, split):
    """
    將指定範圍的病患資料複製到目標 split (train/val) 資料夾。
    採用病患級別劃分 (Patient-Level Splitting) 確保數據集分離。
    """
    # 遍歷指定的病患 ID 範圍
    for i in range(start, end + 1):
        # 格式化病患 ID (例如：1 -> patient0001)
        patient = f"patient{i:04d}"
        
        # 組合成完整的病患資料夾路徑
        img_dir = os.path.join(IMG_ROOT, patient)
        lbl_dir = os.path.join(LBL_ROOT, patient)
        
        # 檢查標籤資料夾是否存在，不存在則跳過此病患（重要檢查）
        if not os.path.isdir(lbl_dir):
            continue

        # 遍歷標籤資料夾內的檔案 (以標籤為主導，確保只複製有標註的圖片)
        for fname in os.listdir(lbl_dir):
            # 確保只處理 YOLO 格式的標籤檔案
            if not fname.endswith(".txt"):
                continue

            # 完整的標籤檔案路徑
            label_path = os.path.join(lbl_dir, fname)
            
            # 取出檔案名稱（不含 .txt 副檔名）
            base, _ = os.path.splitext(fname) 
            
            # 根據標籤檔名，組合出對應的圖片檔案路徑 (假設圖片為 .png)
            img_path = os.path.join(img_dir, base + ".png")
            
            # 檢查圖片是否存在，防止標籤檔案沒有對應圖片的情況
            if not os.path.exists(img_path):
                print(f"找不到對應圖片: {img_path}")
                continue

            # 圖片和標籤都存在，則複製到目標資料夾
            # shutil.copy2 複製檔案，並保留檔案的中繼資料（如時間戳）
            shutil.copy2(img_path, f"./datasets/{split}/images/")
            shutil.copy2(label_path, f"./datasets/{split}/labels/")

# --- 4. 執行資料集劃分 ---

# patient0001~0040 → train (訓練集)
move_patients(1, 40, "train")

# patient0041~0050 → val (驗證集)
move_patients(41, 50, "val")

print("完成移動！")