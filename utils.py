import json
import sys

# json 파일 불러오기 
def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception:
        print(f"{file_path} json 파일 읽는 중 오류: {Exception}")
        sys.exit(1)