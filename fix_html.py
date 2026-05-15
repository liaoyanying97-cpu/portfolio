import re
import os
from PIL import Image

mobile_dir = 'assets/images/mobile/'
sizes = {}
for f in os.listdir(mobile_dir):
    if f.endswith('.webp'):
        try:
            with Image.open(os.path.join(mobile_dir, f)) as img:
                sizes[f] = img.size
        except:
            pass

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pictures = re.findall(r'<picture.*?>.*?</picture>', html, flags=re.DOTALL)
css_rules = []
counter = 1

for pic in pictures:
    new_pic = pic
    if 'decoding=' not in new_pic:
        new_pic = re.sub(r'(<img )', r'\1decoding="async" ', new_pic)

    is_base = False
    img_tag_match = re.search(r'<img[^>]+>', new_pic)
    if img_tag_match:
        img_tag = img_tag_match.group(0)
        if 'full-img' in img_tag and 'position: absolute' not in img_tag:
            is_base = True
            
    sm = re.search(r'<source.*?(?:srcset="([^"]+)")', new_pic)
    im = re.search(r'<img.*?width="(\d+)".*?height="(\d+)"', new_pic)
    
    if is_base and sm and im:
        dw, dh = int(im.group(1)), int(im.group(2))
        
        srcset = sm.group(1)
        fname = srcset.split('?')[0].split('/')[-1]
        if fname in sizes:
            mw, mh = sizes[fname]
        else:
            mw, mh = dw, dh
            
        desktop_pt = (dh / float(dw)) * 100
        mobile_pt = (mh / float(mw)) * 100
        
        cls = f"ar-container-{counter}"
        rule = f".{cls} {{ position: relative; width: 100%; padding-top: {desktop_pt:.4f}%; }}\n"
        rule += f"@media (max-width: 767px) {{ .{cls} {{ padding-top: {mobile_pt:.4f}%; }} }}"
        css_rules.append(rule)
        
        new_pic = re.sub(r'<picture[^>]*>', r'<picture style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;">', new_pic)
        
        # safely inject width:100%; height:100% into img style
        img_tag = re.search(r'<img[^>]+>', new_pic).group(0)
        if 'style="' in img_tag:
            new_img_tag = re.sub(r'style="([^"]*)"', r'style="\1; width: 100%; height: 100%; object-fit: fill;"', img_tag)
        else:
            new_img_tag = img_tag.replace('<img ', '<img style="width: 100%; height: 100%; object-fit: fill;" ')
        
        new_pic = new_pic.replace(img_tag, new_img_tag)
        new_pic = f'<div class="ar-container {cls}">\n{new_pic}\n</div>'
        
        counter += 1

    html = html.replace(pic, new_pic)

def fix_source(match):
    src = match.group(0)
    if 'width=' in src: return src
    m = re.search(r'srcset="([^"]+)"', src)
    if m:
        fname = m.group(1).split('?')[0].split('/')[-1]
        if fname in sizes:
            w, h = sizes[fname]
            return src.replace('srcset=', f'width="{w}" height="{h}" srcset=')
    return src
html = re.sub(r'<source [^>]+>', fix_source, html)

style_block = "<style>\n" + "\n".join(css_rules) + "\n</style>\n</head>"
if '<style>' in html:
    html = re.sub(r'<style>.*?</style>\s*</head>', '</head>', html, flags=re.DOTALL)
html = html.replace('</head>', style_block)

if 'rel="preload"' not in html:
    preloads = '<link rel="preload" href="assets/images/mobile/01.webp" as="image" media="(max-width: 767px)">\n    <link rel="preload" href="assets/images/mobile/02.webp?v=1" as="image" media="(max-width: 767px)">\n    <link rel="stylesheet"'
    html = html.replace('<link rel="stylesheet"', preloads)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Done")
