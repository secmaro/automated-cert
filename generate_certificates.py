import os
import re
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# ==============================================================================
# 🛠️ CONFIGURATION - DEFINE YOUR FILE NAMES AND SETTINGS HERE
# ==============================================================================

# File paths & Folder Names
EXCEL_FILE_NAME = "put_your_excel_file_here.xlsx"
TEMPLATE_FILE_NAME = "put_your_certificate_template.png"

OUTPUT_IMG_DIR_NAME = "Generated_Certificates_PNG"
OUTPUT_PDF_DIR_NAME = "Generated_Certificates_PDF"

# Text & Positioning Settings
FONT_SIZE = 62
TEXT_COLOR = "#00283a"

# Vertical position ratio relative to image height (e.g., 0.404 = 40.4% down from top)
Y_POSITION_RATIO = 0.404

# Target column index in Excel containing student names (0 = Column A, 1 = Column B)
NAME_COLUMN_INDEX = 1

# Custom fonts (checks local project folder first, then OS system fonts)
ARABIC_FONT_NAME = "Amiri-Bold.ttf"
ENGLISH_FONT_NAME = "cambriab.ttf"

# ==============================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EXCEL_FILE = os.path.join(BASE_DIR, EXCEL_FILE_NAME)
TEMPLATE_FILE = os.path.join(BASE_DIR, TEMPLATE_FILE_NAME)
OUTPUT_IMG_FOLDER = os.path.join(BASE_DIR, OUTPUT_IMG_DIR_NAME)
OUTPUT_PDF_FOLDER = os.path.join(BASE_DIR, OUTPUT_PDF_DIR_NAME)

os.makedirs(OUTPUT_IMG_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_PDF_FOLDER, exist_ok=True)

def is_arabic(text):
    return bool(re.search(r'[\u0600-\u06FF]', text))

def get_font(is_ar, size):
    fonts_dir = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')
    
    if is_ar:
        font_candidates = [ARABIC_FONT_NAME, 'timesbd.ttf', 'times.ttf', 'arialbd.ttf']
    else:
        font_candidates = [ENGLISH_FONT_NAME, 'cambria.ttf', 'timesbd.ttf', 'arial.ttf']

    for font_name in font_candidates:
        local_p = os.path.join(BASE_DIR, font_name)
        if os.path.exists(local_p):
            return ImageFont.truetype(local_p, size)
        win_p = os.path.join(fonts_dir, font_name)
        if os.path.exists(win_p):
            return ImageFont.truetype(win_p, size)
            
    return ImageFont.load_default()

def get_template_path():
    # 1. Check specified configuration template file
    if os.path.exists(TEMPLATE_FILE):
        return TEMPLATE_FILE
    
    # 2. Fallback: Search project folder for any image file (.png, .jpg, .jpeg)
    for f in os.listdir(BASE_DIR):
        if f.lower().endswith(('.png', '.jpg', '.jpeg')):
            return os.path.join(BASE_DIR, f)
            
    return None

def generate_certificates():
    template_path = get_template_path()
    if not template_path:
        print(f"[!] Template file not found. Please place '{TEMPLATE_FILE_NAME}' in: {BASE_DIR}")
        return

    if not os.path.exists(EXCEL_FILE):
        print(f"[!] Excel file not found: {EXCEL_FILE}")
        print(f"[!] Please set EXCEL_FILE_NAME to your actual file name.")
        return

    try:
        data = pd.read_excel(EXCEL_FILE)
    except Exception as e:
        print(f"[!] Error reading Excel file: {e}")
        return

    if NAME_COLUMN_INDEX >= len(data.columns):
        print(f"[!] Column index {NAME_COLUMN_INDEX} out of bounds. The Excel file has {len(data.columns)} column(s).")
        return

    template = Image.open(template_path)
    width, height = template.size

    x_pos = width / 2
    y_pos = int(height * Y_POSITION_RATIO)

    target_column = data.columns[NAME_COLUMN_INDEX]

    count = 0
    for _, row in data.iterrows():
        raw_name = str(row[target_column]).strip()
        
        if raw_name.lower() in ('nan', 'none', '') or not raw_name:
            continue

        has_arabic = is_arabic(raw_name)
        font = get_font(has_arabic, FONT_SIZE)

        if has_arabic:
            reshaped_text = reshape(raw_name)
            display_text = get_display(reshaped_text)
        else:
            display_text = raw_name.title()

        img = template.copy()
        draw = ImageDraw.Draw(img)

        draw.text((x_pos, y_pos), display_text, font=font, fill=TEXT_COLOR, anchor="mm")

        safe_name = "".join([c for c in raw_name if c.isalnum() or c in (' ', '-')]).strip()

        # Save PNG
        png_path = os.path.join(OUTPUT_IMG_FOLDER, f"{safe_name}.png")
        img.save(png_path)

        # Save PDF
        pdf_path = os.path.join(OUTPUT_PDF_FOLDER, f"{safe_name}.pdf")
        pdf_img = img.convert('RGB')
        pdf_img.save(pdf_path, "PDF", resolution=100.0)

        count += 1
        print(f"[+] Generated ({count}): {safe_name}")

    print(f"\n[✓] Finished generating {count} certificates successfully.")

if __name__ == "__main__":
    generate_certificates()
