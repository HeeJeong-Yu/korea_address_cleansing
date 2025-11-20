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
        self.col = None
        self.del_word = None
        self.df = None

    # 컬럼명 찾기
    @classmethod
    def _load_column_mappings(cls, key):
        if cls._col_mapping == None:
            data = load_json(cls._col_mapping_path)
            data = load_json(get_config_data("paths", "col_mapping"))

            def str_to_int(col):
                col = {int(k):v for k, v in col.items()}
                return col

            cls._col_mapping = {key: str_to_int(value) for key, value in data.items()}
        
        return cls._col_mapping[key]

    # 폴더 이름 찾기
    def _fild_folder_name(self, word):
        for name in os.listdir(self._correct_data_path):
            if word in name: 
                return name
    
    def _find_folder_path(self, word):
        self._folder_path = os.path.join(self._correct_data_path, self._fild_folder_name(word))

    # 타겟 파일리스트 찾기
    def find_filelist(self):
        filelist = os.listdir(self._folder_path)
        filelist = [filename for filename in filelist if self.del_word not in filename]
        
        return filelist
    
    # 데이터 파일 읽기
    def read_data(self, filelist, data):
        df_list = []

        for filename in tqdm(filelist, desc=f"{data} 데이터 읽는 중"):
            file = os.path.join(self._folder_path, filename)
            new_df = pd.read_csv(file, encoding="cp949", sep="|", header=None, low_memory=False)
            new_df.rename(columns=self.col, inplace=True)
            df_list.append(new_df)

        if df_list:
            df = pd.concat(df_list, ignore_index=True)
            return df
        
        return pd.DataFrame()   

    # 메인
    def run(self, foldername, del_word):
        self.col = self._load_column_mappings(foldername)
        self.del_word = del_word
        self._find_folder_path(foldername)

        filelist = self.find_filelist()
        self.df = self.read_data(filelist, foldername)

        print(len(self.df))

if __name__ == "__main__":
    roadname_foldername = get_config_data("foldernames", "roadname"); roadname_del_word = get_config_data("del_words", "roadname")
    detailed_foldername = get_config_data("foldernames", "detailed"); detailed_del_word = get_config_data("del_words", "detailed")

    roadname = ReadCorrectData(); roadname.run(roadname_foldername, roadname_del_word); roadname_df = roadname.df; del roadname
    detailed = ReadCorrectData(); detailed.run(detailed_foldername, detailed_del_word); detailed_df = detailed.df; del detailed