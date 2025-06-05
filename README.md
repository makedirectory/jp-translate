# 🇯🇵→🇺🇸 CSV Batch Translator (Japanese to English)

This script batch-translates Japanese CSV files into English using the **official Google Cloud Translation API**.

It recursively scans a source folder, translates both content and headers, and outputs fully translated CSVs while preserving the original folder structure.

---

## 🚀 Features

- ✅ Translates **cell content** and **column headers**
- ✅ Only translates **Japanese text** (skips English)
- ✅ Uses **batch requests** for efficiency (100 items/request)
- ✅ Handles `UTF-8` and `Shift-JIS` encoded files
- ✅ Preserves **original subdirectory structure**
- ✅ Logs untranslated (non-Japanese) values

---

## 🛠 Requirements

- Python 3.8+
- [Google Cloud Translation API](https://cloud.google.com/translate/docs/setup)
- `uv` (optional, for modern Python dependency management)

---

## 📦 Setup

### 1. Clone this repository or copy the script

```bash
git clone <repo-url>
cd translate-csv
```

### 2. Create virtual environment using uv (or venv)
```bash
uv venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
Run `uv pip install -r requirements.txt`

### 4. Set up Google Cloud credentials
 - Create a Google Cloud Project
 - Enable Cloud Translation API
 - Create a service account key (JSON)
 - Save the key as: google-credentials.json in this project folder

## 📂 Folder Structure
```
├── translate.py
├── google-credentials.json
├── japanese_csvs/
│   ├── file1.csv
│   └── nested/
│       └── file2.csv
├── translated_csvs/       # Generated automatically
├── untranslated_cells_log.txt
```

## 🧪 Usage
Run the script: `python translate.py` 

Translated CSVs will appear in translated_csvs/, matching the folder layout of the originals.

## 📝 Output
 - Translated CSV files will have:
    - All Japanese content translated to English
    - Column headers translated
 - untranslated_cells_log.txt will contain a list of non-Japanese values that were skipped

 ## ⚙️ Customization
You can modify the script to:
 - Translate other languages by adjusting the is_japanese() function
 - Add glossary terms (e.g., always translate "患者" as "Patient")
 - Support .xlsx files using openpyxl

## 📘 License
MIT License – use freely in personal or commercial projects.

## 🙋 Support
Feel free to open an issue or email the author for help or improvements.
Let me know if you'd like to:
- Add a `Makefile` or shell script for common tasks
- Package it as a CLI (`translate-csv --input foo --output bar`)
- Include GitHub Actions to lint or test it automatically

Happy translating!