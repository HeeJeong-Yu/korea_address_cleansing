from read_correct_data import *
from utils import *

# 주소 정보 누리집 데이터 읽어 오기
roadname_foldername = get_config_data("foldernames", "roadname"); roadname_del_word = get_config_data("del_words", "roadname")
detailed_foldername = get_config_data("foldernames", "detailed"); detailed_del_word = get_config_data("del_words", "detailed")

log("도로명주소 한글 데이터 읽기 시작")
roadname = ReadCorrectData(); roadname.run(roadname_foldername, roadname_del_word); 
roadname_df = roadname.df; del roadname
log(f"도로명주소 한글 행 개수: {len(roadname_df)}")

log("상세주소 한글 데이터 읽기 시작")
detailed = ReadCorrectData(); detailed.run(detailed_foldername, detailed_del_word); 
detailed_df = detailed.df; del detailed
log(f"상세주소 표시 행 개수: {len(detailed_df)}")