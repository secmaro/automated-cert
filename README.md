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
