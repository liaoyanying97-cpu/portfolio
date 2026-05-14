import os
from PIL import Image
import glob

def compress_images_high_res():
    img_dir = 'assets/images'
    files = glob.glob(os.path.join(img_dir, '*.png'))
    
    for file in files:
        try:
            img = Image.open(file)
            # 这次我们【不缩小尺寸】，保留原图的高分辨率（如 2400px）
            # 仅仅改变格式为 WebP，并使用较高的质量 85，这样可以兼顾高清和加载速度
            webp_path = os.path.splitext(file)[0] + '.webp'
            img.save(webp_path, 'WEBP', quality=85)
            print(f'Converted to High-Res WebP: {webp_path}')
            os.remove(file)
        except Exception as e:
            print(f'Error processing {file}: {e}')

if __name__ == '__main__':
    compress_images_high_res()