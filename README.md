# 📜 Bi-Directional Arabic & English Bulk Certificate Generator

An automated Python tool designed to bulk-generate high-resolution personalized certificates (PNG & PDF) from Excel spreadsheets. Built to solve right-to-left (RTL) Arabic text rendering and ligature issues alongside standard English text.

---

## 🛠️ Features

- **Auto Language Detection:** Identifies Arabic vs. English names dynamically via UTF-8 Regex (`\u0600-\u06FF`).
- **RTL & BiDi Text Support:** Applies `arabic_reshaper` and `python-bidi` algorithms to render Arabic ligatures correctly without reversed text.
- **Middle-Center Alignment:** Dynamically centers strings using Pillow canvas anchors (`anchor="mm"`).
- **Multi-Format Export:** Generates lossless `.png` images and print-ready `.pdf` files simultaneously.

---

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/arabic-cert-generator.git](https://github.com/your-username/arabic-cert-generator.git)
   cd arabic-cert-generator

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Your Settings:**
   Open `generate_certificates.py` and update the top configuration section with your Excel spreadsheet and template image file names:
   ```python
   EXCEL_FILE_NAME = "students.xlsx"
   TEMPLATE_FILE_NAME = "batu_template.png"
   ```

4. **Run the Generator:**
   ```bash
   python generate_certificates.py
   ```

---

## ⚙️ Configuration Reference

All settings can be customized directly at the top of `generate_certificates.py`:

| Setting | Default | Description |
| :--- | :--- | :--- |
| `EXCEL_FILE_NAME` | `"put_your_excel_file_here.xlsx"` | Excel file placed in project directory |
| `TEMPLATE_FILE_NAME` | `"put_your_certificate_template.png"` | Template image placed in project directory |
| `NAME_COLUMN_INDEX` | `1` | Zero-indexed column position for student names (1 = Column B) |
| `FONT_SIZE` | `62` | Font point size for name rendering |
| `Y_POSITION_RATIO` | `0.404` | Vertical position ratio from image top (0.404 = 40.4%) |
| `TEXT_COLOR` | `"#00283a"` | Hex color code for printed text |
