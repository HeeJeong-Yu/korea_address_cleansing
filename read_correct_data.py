import pandas as pd
from tqdm import tqdm
import os, json
from utils import *

class ReadCorrectData:
    _correct_data_path = get_config_data("paths", "correct_data")
    _col_mapping_path =  get_config_data("paths", "col_mapping")
    _col_mapping = None

    def __init__(self):
        self._folder_path = None
        self.original_col = None
        self.need_col = None
        self.del_word = None
        self.df = None

    # 컬럼명 찾기
    @classmethod
    def _load_column_mappings(cls, key: str):
        if cls._col_mapping == None:
            cls._col_mapping = load_json(cls._col_mapping_path)

        return cls._col_mapping[key]
    
    def split_col(self, col: dict):
        self.need_col = col['need_cols']

        oc = col['original_cols']
        self.original_col = {int(key):value for key, value in oc.items()}

    # 폴더 이름 찾기
    def _fild_folder_name(self, word: str)-> str:
        for name in os.listdir(self._correct_data_path):
            if word in name: 
                return name
    
    def _find_folder_path(self, word: str):
        self._folder_path = os.path.join(self._correct_data_path, self._fild_folder_name(word))

    # 타겟 파일리스트 찾기
    def find_filelist(self)-> list:
        filelist = os.listdir(self._folder_path)
        filelist = [filename for filename in filelist if self.del_word not in filename]
        
        return filelist
    
    def read_csv(self, file: str)-> pd.DataFrame:
        try:
            df = pd.read_csv(file, encoding="cp949", sep="|", header=None, low_memory=False, quoting=csv.QUOTE_NONE)
            return df
        except Exception as e:
            print(f"csv파일 읽기 오류({file}): {e}")
            sys.exit(1)
    
    # 데이터 파일 읽기
    def read_data(self, filelist: list, data: str)-> pd.DataFrame:
        df_list = []

        for filename in tqdm(filelist, desc=f"{data} 데이터 읽는 중"):
            file = os.path.join(self._folder_path, filename)
            new_df = self.read_csv(file)
            new_df.rename(columns=self.original_col, inplace=True)
            new_df = new_df[self.need_col]

            df_list.append(new_df)

        if df_list:
            df = pd.concat(df_list, ignore_index=True)
            return df
        
        return pd.DataFrame()   

    # 메인
    def run(self, foldername: str, del_word: str):
        self.split_col(self._load_column_mappings(foldername))

        self.del_word = del_word
        self._find_folder_path(foldername)

        filelist = self.find_filelist()
        self.df = self.read_data(filelist, foldername)

if __name__ == "__main__":
    roadname_foldername = get_config_data("foldernames", "roadname"); roadname_del_word = get_config_data("del_words", "roadname")
    detailed_foldername = get_config_data("foldernames", "detailed"); detailed_del_word = get_config_data("del_words", "detailed")

    roadname = ReadCorrectData(); roadname.run(roadname_foldername, roadname_del_word); roadname_df = roadname.df; del roadname
    detailed = ReadCorrectData(); detailed.run(detailed_foldername, detailed_del_word); detailed_df = detailed.df; del detailed