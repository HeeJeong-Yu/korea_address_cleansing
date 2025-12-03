import pandas as pd
import numpy as np

def replace_to_empty(df):
    df.replace(
        to_replace=[0, False, None, np.nan], 
        value='',
        inplace=True)
    

def split_eup_myeon_dong(df, col="법정읍면동명"):
    dong_end_word = ('동', '로', '가')
    eup_myeon_word = ('읍', '면')

    def make_new_col(end_word, new_col, df):
        mask = df[col].str.endswith(end_word, na=False)
        df[new_col] = np.where(
            mask, 
            df[col], 
            np.nan)
        
    make_new_col(dong_end_word, '법정동', df)
    make_new_col(eup_myeon_word, '법정읍면', df)

    return df

# 지하여부 처리 
# 0=지상(지금은 공백), 1=지하, 2=공중, 3=수상 
def change_underground(df):
    status_map = {
        0: '',  # 지상
        1: '지하',
        2: '공중',
        3: '수상'
    }

    return df['지하여부'].map(status_map)

def concat_address(df):
    def concat_str(col):
        return np.where(
            df[col].str.strip() != '', 
            ' ' + df[col], 
            ''
        )


    address_series = df['시도명'].copy()
    address_series += concat_str('시군구명')
    address_series += concat_str('법정읍면')
    address_series += ' ' + df['도로명'] 

    underground_status = concat_str('지하여부')
    address_series += np.where(
        underground_status != '',
        underground_status + df['건물본번'],
        ' ' + df['건물본번']
    )

    address_series += np.where(
        df['건물부번'].str.strip() != '', 
        '-' + df['건물부번'], 
        ''
    )

    return address_series

def select_buildingName(df):
    return np.where(
        df['건축물대장건물명'] != '',
        df['건축물대장건물명'], 
        
        np.where(
            df['시군구건물명'] != '',
            df['시군구건물명'],
            '' 
        )
    )

def process_roadname_data(df):
    roadname_df['지하여부'] = change_underground(roadname_df)
    replace_to_empty(roadname_df)
    roadname_df = roadname_df.astype(str)

    # 법정읍면동명-> 법정동, 법정읍면으로 분리
    roadname_df = split_eup_myeon_dong(roadname_df)

    # 필요한 컬럼 생성
        # 도로명주소: 풀도로명주소 
        # 건물명: 건축물대장건물명이 없을 경우, 시군구건물명으로 대체. 둘 다 없을 경우 공백
    roadname_df['도로명주소'] = concat_address(roadname_df)
    roadname_df['건물명'] = select_buildingName(roadname_df)

    # 필요없는 컬럼 삭제
    roadname_df = roadname_df.drop(columns=['법정읍면동명', '건축물대장건물명', '시군구건물명']) 