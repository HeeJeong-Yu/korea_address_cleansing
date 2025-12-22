import pandas as pd
import sys, os, re
from utils import *

def read_csv(file_path: str)-> pd.DataFrame:
    try:
        return pd.read_csv(file_path, encoding='euc-kr')
    except Exception as e:
        print(f"csv파일 읽기 오류({file_path}): {e}")
        sys.exit(1)

# 컬럼명이 여러 개인 경우 컬럼 중복 위험. 
def rename_col(df: pd.DataFrame, target_col:str):
    taraget_cols = get_config_data("target_col", "roadnames")
    col_map  = {}
    for col in df.columns:
        if col in taraget_cols: 
            col_map[col] = target_col
    # col_map = {col:target_col for col in taraget_cols}

    try:
        df.rename(columns=col_map,
                inplace=True)
    except Exception as e:
        print("{e}, 데이터프레임 컬럼명 변경 오류")
        sys.exit(1)

def split_address(data: str)-> tuple:
    pattern = r"(?:[^\s]+(?:개|길|리|로|동|가)\s*"+\
            "(?:\d*[가-힣]*(?:개|길|리|로|동|가))?)"+\
            "(?:\s+)?((지하)*|(산)*)(?:\s+)?(\d+(?:-\d*)?)" 
    match = re.search(pattern, data)

    if match is not None:
        idx = match.span()[-1]
        address = data[:idx].strip()          # 도로명주소
        detailed_address = data[idx:].strip() # 상세주소

        return address, detailed_address

    else: return data, ''

def read_target_data():
    target_path = get_config_data("paths", "target_data")
    target_file_list = os.listdir(target_path)
    target_col = get_config_data("target_col", "roadname")

    for filename in target_file_list: 
        file_df = read_csv(os.path.join(target_path, filename))
        rename_col(file_df, target_col)

        file_df[target_col] = file_df[target_col].fillna('')
        file_df[['도로명주소', '상세주소']] = pd.DataFrame(
                file_df[target_col].map(split_address).tolist(),
                index=file_df.index
            )



        break