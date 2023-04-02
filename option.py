import argparse

'''
--CORPUS_INPUT_FOLDER_ROOT： rir文件的路径

--CORPUS_OUTPUT_FOLDER_ROOT: 生成数据的路径

--need_config：场景名称

--MIC_CONFIGs：场景名称

备注： need_config 和 MIC_CONFIGs  需要一致 

--noise_dir 噪音文件的路径

--timit_root 干净的人声的路径

--Speaker_txt  干净的人声文件的 txt

'''

parser = argparse.ArgumentParser(description='load these files')
parser.add_argument('--CORPUS_INPUT_FOLDER_ROOT', default='/data2/queenie_2023/GenWav/add_without_zky_0316/', type=str,help='load rir root')
parser.add_argument('--CORPUS_OUTPUT_FOLDER_ROOT', default='/data2/queenie_2023_gen_without_zky/', type=str)
<<<<<<< HEAD
parser.add_argument('--T60DRRresultsFile', default='./process_chart/extra_add_with_zky.csv', type=str)
=======
parser.add_argument('--T60DRRresultsFile', default='./process_chart/extra_add_without_zky.csv', type=str)
>>>>>>> fc5277abe523b1d0b08cbec7834b003445c3a074
#为了加速训练，必需按照config分开才行
parser.add_argument('--need_config', default='arthur-sykes-rymer-auditorium-university-york', type=str)
parser.add_argument('--MIC_CONFIGs', default="arthur-sykes-rymer-auditorium-university-york", type=str)
#parser.add_argument('--MIC_CONFIGs', default="Nature,Miscellaneous,Recreation,Stairwells,Underground,Underpasses,Venues", type=str)
parser.add_argument('--noise_dir', default="/data2/cql/code/augu_data/get_data/15NoiseScenes_txt", type=str)
parser.add_argument('--timit_root', default='/data2/cql/code/augu_data/concatPeople/chinese_concat', type=str)
parser.add_argument('--Speaker_txt', default='/data2/cql/code/augu_data/concatPeople/chinese_concat/catChinese.txt', type=str)
args = parser.parse_args()
