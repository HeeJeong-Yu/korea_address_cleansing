import json, sys, time, csv
import pandas as pd
import numpy as np
from typing import Any

_config_cache = None

# json 파일 불러오기 
def load_json(file_path: str) -> Any:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Json 파일 load 오류: {e}\n파일: {file_path}")
        sys.exit(1)

# 설정 파일 
def _load_config_data(file_path: str="config.json"):
    global _config_cache
    
    if _config_cache is not None:
        return _config_cache
        
    config = load_json(file_path)
    _config_cache = config 
    
    return _config_cache

# 설정 파일 값 읽어오기
def get_config_data(category: str, word: str)-> str:
    config = _load_config_data()

    try:
        data = config[category][word]
        return data
    except Exception as e:
        print(f"config 파일 읽기 오류: {e}")
        sys.exit(1)

# # csv 파일 읽기
# def read_csv(file):
#     try:
#         df = 
#         return df
#     except Exception as e:
#         print(f"csv파일 읽기 오류({file}): {e}")
#         sys.exit(1)
    
# 로그 출력
def log(text: str):
    now = time.strftime(r"%Y/%m/%d %H:%M:%S")
    res = f"[{now}] {text}"
    print(res, flush=True)

# 데이터프레임 결측치 값 처리
def replace_to_empty(df: pd.DataFrame):
    df.replace(
        to_replace=[0, False, None, np.nan], 
        value='',
        inplace=True)