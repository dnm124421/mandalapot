import os
import re
import urllib.request
import ssl
import time

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

html_dir = r"c:\dsa in c++\pro__ jettt\spiece and soul\spice_soul_website"
assets_dir = os.path.join(html_dir, "assets", "images")
os.makedirs(assets_dir, exist_ok=True)

# Find all https://images.unsplash.com/...
url_pattern = re.compile(r'(https://images\.unsplash\.com/photo-[a-zA-Z0-9\-]+(?:[^"\'\s]*))')

success_count = 0
fail_count = 0

for filename in os.listdir(html_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(html_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        urls = url_pattern.findall(content)
        # Deduplicate to avoid multiple downloads
        urls = list(set(urls))
        
        for url in urls:
            photo_match = re.search(r'photo-([a-zA-Z0-9\-]+)', url)
            if not photo_match:
                continue
            photo_id = photo_match.group(1)
            img_filename = f"{photo_id}.jpg"
            img_path = os.path.join(assets_dir, img_filename)
            
            if not os.path.exists(img_path):
                print(f"Downloading {url} to {img_filename}")
                try:
                    req_url = url
                    if '?' not in req_url:
                         req_url += '?w=800&auto=format&fit=crop'
                    
                    req = urllib.request.Request(req_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                    with urllib.request.urlopen(req, context=ctx) as response, open(img_path, 'wb') as out_file:
                        data = response.read()
                        out_file.write(data)
                    time.sleep(0.5)
                    success_count += 1
                except Exception as e:
                    print(f"Failed to download {url}: {e}")
                    fail_count += 1
                    
            # Replace in content.
            content = content.replace(url, f"assets/images/{img_filename}")
            
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

print(f"Done! Downloaded {success_count} images. Failed {fail_count} images.")
