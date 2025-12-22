from read_correct_data import *
from utils import *
from get_correct_data_summary import *
from process_roadname_data import *

# 주소 정보 누리집 데이터 읽어 오기
roadname_foldername = get_config_data("foldernames", "roadname"); roadname_del_word = get_config_data("del_words", "roadname")
detailed_foldername = get_config_data("foldernames", "detailed"); detailed_del_word = get_config_data("del_words", "detailed")

log("도로명주소 한글 데이터 읽기 중")
roadname = ReadCorrectData(); roadname.run(roadname_foldername, roadname_del_word); 
roadname_df = roadname.df; del roadname

log("상세주소 한글 데이터 읽기 중")
detailed = ReadCorrectData(); detailed.run(detailed_foldername, detailed_del_word); 
detailed_df = detailed.df; del detailed

log("주소정보누리집 데이터 요약 중")
get_correct_data_summary(roadname_df, detailed_df)

log("도로명주소 한글 데이터 처리 중")
roadname_df = process_roadname_data(roadname_df)