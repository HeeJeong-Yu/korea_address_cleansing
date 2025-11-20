import json, sys, time, csv
import pandas as pd

_config_cache = None

# json 파일 불러오기 
def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Json 파일 load 오류: {e}")
        sys.exit(1)

# 설정 파일 
def _load_config_data(file_path="config.json"):
    global _config_cache
    
    if _config_cache is not None:
        return _config_cache
        
    config = load_json(file_path)
    _config_cache = config 
    
    return _config_cache

# 설정 파일 값 읽어오기
def get_config_data(category, word):
    config = _load_config_data()

    try:
        data = config[category][word]
        return data
    except Exception as e:
        print(f"config 파일 읽기 오류: {e}")
        sys.exit(1)

# csv 파일 읽기
def read_csv(file):
    try:
        df = pd.read_csv(file, encoding="cp949", sep="|", header=None, low_memory=False, quoting=csv.QUOTE_NONE)
        return df
    except Exception as e:
        print(f"csv파일 읽기 오류({file}): {e}")
        sys.exit(1)
    

# 로그 출력
def log(text):
    now = time.strftime(r"%Y/%m/%d %H:%M:%S")
    res = f"[{now}] {text}"
    print(res, flush=True)