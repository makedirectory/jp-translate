import os
import pandas as pd
from google.cloud import translate_v2 as translate
from collections import defaultdict
import six

# Setup credentials and API client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google-credentials.json'
translate_client = translate.Client()

input_folder = './japanese_csvs'
output_folder = './translated_csvs'
log_file_path = 'untranslated_cells_log.txt'
batch_size = 100

# --- Utility Functions ---

def read_csv_safely(path):
    """Attempt to read with UTF-8, fall back to Shift-JIS if needed."""
    try:
        df = pd.read_csv(path, encoding='utf-8')
        print(f"  Read with UTF-8: {path}")
        return df
    except UnicodeDecodeError:
        print(f"  Falling back to Shift-JIS: {path}")
        return pd.read_csv(path, encoding='shift_jis')

def is_japanese(text):
    """Detect if text contains Japanese characters."""
    if not isinstance(text, str):
        return False
    return any('\u3040' <= ch <= '\u30ff' or '\u4e00' <= ch <= '\u9faf' for ch in text)

def translate_batch(texts, target='en'):
    """Translate a batch of strings."""
    try:
        results = translate_client.translate(texts, target_language=target)
        return [res['translatedText'] for res in results]
    except Exception as e:
        print(f"⚠️ Batch translation error: {e}")
        return texts  # fallback to original

# --- Main Translation Workflow ---

def main():
    all_untranslated = defaultdict(int)

    for root, _, files in os.walk(input_folder):
        for filename in files:
            if not filename.endswith('.csv'):
                continue

            input_path = os.path.join(root, filename)
            rel_path = os.path.relpath(input_path, input_folder)
            output_path = os.path.join(output_folder, rel_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            print(f"\n🔄 Processing {rel_path}")
            df = read_csv_safely(input_path)

            flat_cells = []
            cell_positions = []  # (row, col) index map
            untranslated = defaultdict(int)

            data = df.values.tolist()
            for row_idx, row in enumerate(data):
                for col_idx, cell in enumerate(row):
                    if pd.isna(cell) or not isinstance(cell, str):
                        continue
                    if is_japanese(cell):
                        flat_cells.append(cell)
                        cell_positions.append((row_idx, col_idx))
                    else:
                        untranslated[cell] += 1

            # Translate in batches
            translated = []
            for i in range(0, len(flat_cells), batch_size):
                batch = flat_cells[i:i + batch_size]
                translated.extend(translate_batch(batch))

            # Apply translations back into data matrix
            for (row_idx, col_idx), text in zip(cell_positions, translated):
                data[row_idx][col_idx] = text

            translated_df = pd.DataFrame(data, columns=df.columns)

            # --- Translate column headers ---
            original_headers = list(df.columns)
            headers_to_translate = [col for col in original_headers if is_japanese(col)]

            if headers_to_translate:
                print(f"  Translating {len(headers_to_translate)} header(s)...")
                translated_headers = translate_batch(headers_to_translate)
            else:
                translated_headers = headers_to_translate

            header_map = dict(zip(headers_to_translate, translated_headers))
            translated_df.columns = [header_map.get(col, col) for col in original_headers]

            # --- Save file ---
            translated_df.to_csv(output_path, index=False)
            print(f"✅ Saved: {output_path}")

            # Update untranslated log
            for k, v in untranslated.items():
                all_untranslated[k] += v

    # Save untranslated cell log
    if all_untranslated:
        with open(log_file_path, 'w', encoding='utf-8') as f:
            f.write("=== Untranslated Non-Japanese Content ===\n")
            for k, v in sorted(all_untranslated.items(), key=lambda x: -x[1]):
                f.write(f"{k} (x{v})\n")
        print(f"📝 Log saved: {log_file_path}")

if __name__ == "__main__":
    main()
