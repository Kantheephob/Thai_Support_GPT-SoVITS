import os
import shutil
import re
from pathlib import Path

# ====== CONFIG ======
source_dir = "./Toki-Voice-Data"      # โฟลเดอร์ต้นทาง (ที่มี 01, 02...)
output_dir = "./GPT_SoVITS_Dataset"   # โฟลเดอร์ปลายทาง
speaker_name = "toki"                 # ชื่อตัวละคร
language = "ja"                       # ภาษา (ja = Japanese, zh = Chinese, en = English)

# สร้างโฟลเดอร์ปลายทาง
output_path = Path(output_dir)
output_path.mkdir(parents=True, exist_ok=True)

# Regex สำหรับดึงข้อความภาษาญี่ปุ่น (01嬉しいわ.wav -> 嬉しいわ)
pattern = re.compile(r"^\d+[\s_.-]*(.+)\.wav$")

def prepare_gpt_sovits_dataset():
    source_path = Path(source_dir)
    audio_files = sorted(source_path.rglob("*.wav"))
    
    list_entries = []
    count = 0

    print(f"🚀 เริ่มแปลงไฟล์สำหรับ GPT-SoVITS ({len(audio_files)} ไฟล์)...")

    for path in audio_files:
        file_name = path.name
        match = pattern.match(file_name)
        
        if match:
            # 1. ดึงข้อความ
            text = match.group(1).strip()
            
            # 2. คัดลอกไฟล์เสียง (แนะนำให้รวมไว้ที่เดียวหรือสร้าง sub-folder)
            # ใน GPT-SoVITS มักจะใช้ path เต็มหรือ path ที่สัมพันธ์กับตัวรัน
            dest_path = output_path / file_name
            shutil.copy2(path, dest_path)
            
            # 3. Format ของ GPT-SoVITS list file:
            # path_to_wav|speaker_name|language|text
            # ตัวอย่าง: D:/data/toki/01.wav|toki|JA|こんにちは
            line = f"{dest_path.absolute()}|{speaker_name}|{language}|{text}"
            list_entries.append(line)
            
            count += 1
            if count % 20 == 0:
                print(f"✅ ทำเสร็จแล้ว {count} ไฟล์...")

    # เขียนไฟล์ .list (GPT-SoVITS นิยมใช้ .list หรือ .txt)
    output_file = output_path / f"{speaker_name}.list"
    with open(output_file, "w", encoding="utf-8") as f:
        for entry in list_entries:
            f.write(entry + "\n")

    print(f"\n✨ เตรียมข้อมูลเสร็จสิ้น!")
    print(f"📂 ไฟล์เสียงทั้งหมดอยู่ที่: {output_path}")
    print(f"📝 ไฟล์สำหรับ Train (List file): {output_file}")
    print(f"⚠️ อย่าลืมเช็คว่า Path ในไฟล์ .list ถูกต้องตามที่เครื่องเทรนมองเห็น")

if __name__ == "__main__":
    prepare_gpt_sovits_dataset()