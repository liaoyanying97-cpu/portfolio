import os
import re
import time
from PIL import Image

# 1. Compress Images
def compress_webp(directory, quality=80):
    total_saved_bytes = 0
    count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".webp"):
                filepath = os.path.join(root, file)
                original_size = os.path.getsize(filepath)
                
                try:
                    with Image.open(filepath) as img:
                        temp_path = filepath + ".tmp"
                        img.save(temp_path, "WEBP", quality=quality)
                    
                    new_size = os.path.getsize(temp_path)
                    # Replace if it's smaller
                    if new_size < original_size:
                        os.replace(temp_path, filepath)
                        total_saved_bytes += (original_size - new_size)
                        count += 1
                    else:
                        os.remove(temp_path)
                        
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
    return count, total_saved_bytes

print("开始压缩图片...")
count, saved_bytes = compress_webp("/Users/yanying/CodeBuddy/work/assets/images", 80)
print(f"成功压缩了 {count} 张图片，总共减小了 {saved_bytes / (1024*1024):.2f} MB 的体积。")

# 2. Update HTML cache versions
html_path = '/Users/yanying/CodeBuddy/work/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_v = str(int(time.time()))[-5:]
content = re.sub(r'\.webp\?v=\d+', f'.webp?v={new_v}', content)
content = re.sub(r'\.webp"', f'.webp?v={new_v}"', content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("HTML 缓存版本号更新完成。")
