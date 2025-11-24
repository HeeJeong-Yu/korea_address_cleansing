from utils import *
from read_correct_data import *
import os

def calculate_data(df):
    results = {}
    df_len = len(df)

    for col in df.columns:
        null_count = df[col].isnull().sum()
        null_percent = round((null_count/df_len)*100)
        unique_count = df[col].nunique()
        
        results[col] = {
            'null값 인스턴스 건수': null_count,
            'null값 퍼센트': null_percent,
            '중복제거한 인스턴스 건수': unique_count
        }

    return pd.DataFrame(results)

def save_dataframe(df, file_path):
    try:
        if not file_path:
            df.to_csv(file_path, index=False, encoding='cp949')
        else:
            df.to_csv(file_path, mode="a", index=False, encoding='cp949')
    except Exception as e:
        print(f"DF 저장 오류{file_path}: {e}")

def check_path():
    file_path = get_config_data("paths", "output")
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    
    return os.path.join(file_path, get_config_data("filename", "correct_data_summary"))

def get_correct_data_summary(roadname_df, detailed_df):
    file_path = check_path()

    data_summary = []
    df_len = pd.DataFrame({"도로명주소 한글 인스턴스 건수" : [len(roadname_df)], 
                            "상세주소 표시 인스턴스 건수" : [len(detailed_df)]})
    roadname_summary = calculate_data(roadname_df)
    detailed_summary = calculate_data(detailed_df)
    data_summary.append(df_len); data_summary.append(roadname_summary); data_summary.append(detailed_summary)

    for d in data_summary: save_dataframe(d, file_path)