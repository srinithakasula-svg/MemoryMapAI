import os
import pandas as pd


def extract_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def extract_csv(file_path):
    data = pd.read_csv(file_path)
    return data.to_string(index=False)


def extract_text(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".txt":
        return extract_txt(file_path)

    elif extension == ".csv":
        return extract_csv(file_path)

    return ""


def split_text(text, chunk_size=1000, overlap=150):
    text = text.strip()

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks