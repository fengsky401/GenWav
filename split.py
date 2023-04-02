import os
import csv
import argparse
import shutil
import xlrd

import numpy as np
parser = argparse.ArgumentParser()
#创建解析器
#ArgumentParser 对象包含将命令行解析成 Python 数据类型所需的全部信息。
#path = r"C:\Users\17579\Desktop\新建文件夹\TAE_Train\Data_Aug\Step_1\test_1.csv"


def excel_to_csv(file):

    resultsFileName = file.replace(".xlsx",'.csv')#"02_06_val_data.csv"
    resultsHandle = open(resultsFileName, "a", newline="")
    csv_writer = csv.writer(resultsHandle)
    headLine = ["Test ID:", "Ver:", "fs:", "Room:", "Room Config:", "Session ID:", "Mic Pos:",
                "Source Pos:", "Config:", "Rec Type:", "RIR:", "Freq band:", "Centre freq:",
                "Channel:", "DRR:", "DRR Mean (Ch):", "T60 AHM:", "T30 ISO:", "T20 ISO:",
                "T60 AHM Mean (Ch):", "T30 ISO Mean (Ch):", "T20 ISO Mean (Ch):", "ISO AHM Ints:", "FB DRR :",
                "FB DRR Mean (Ch):",
                "FB T60 AHM:", "FB T30 ISO:", "FB T20 ISO:", "FB T60 AHM Mean (Ch):", "FB T30 ISO Mean (Ch):",
                "FB T20 ISO Mean (Ch):",
                "DRR direct +:", "DRR direct -:"]
    # headLine = ["Test ID:", "Ver:", "fs:", "Room:",  "Session ID:", "Mic Pos:",
    #             "Source Pos:", "Config:", "Rec Type:", "RIR:", "Freq band:", "Centre freq:",
    #             "Channel:", "DRR:", "DRR Mean (Ch):", "T60 AHM:", "T30 ISO:", "T20 ISO:",
    #             "T60 AHM Mean (Ch):", "T30 ISO Mean (Ch):", "T20 ISO Mean (Ch):", "ISO AHM Ints:", "FB DRR :",
    #             "FB DRR Mean (Ch):",
    #             "FB T60 AHM:", "FB T30 ISO:", "FB T20 ISO:", "FB T60 AHM Mean (Ch):", "FB T30 ISO Mean (Ch):",
    #             "FB T20 ISO Mean (Ch):",
    #             "DRR direct +:", "DRR direct -:"]

    csv_writer.writerow(headLine)

    book = xlrd.open_workbook(file)

    sheet1 = book.sheets()[0]
    # 数据总行数
    nrows = sheet1.nrows
    # 数据总列数
    ncols = sheet1.ncols

    # 获取表中第三行的数据
    x = sheet1.row_values(2)
    # 获取表中第二列的数据
    y = sheet1.col_values(1)
    # 获取第五列中的第二个数据
    z = sheet1.col_values(4)[1]

    test_id = 0
    for i in range(1, nrows):
        values = sheet1.row_values(i)
        room = values[1]
        config = values[0]
        channel = values[4]
        fre_band = 0

        for j in range(len(values)):

            if j < 10:
                continue
            else:
                if j % 5 == 0:
                    info = []
                    # resultsHandle = open(resultsFileName, "a", newline="")
                    # csv_writer = csv.writer(resultsHandle)
                    fre_band += 1
                    test_id += 1
                    t60 = values[j]
                    info.append(test_id)  # 序号
                    info.append(1)
                    info.append(48000)
                    info.append(room)
                    info.append("NAN")
                    info.append(1)
                    info.append(2)
                    info.append(config)
                    info.append("IR")
                    info.append(room)
                    info.append("NAN")
                    info.append(fre_band)  # 表示第几个频段，它没有30个频段，所有应该设置为0
                    info.append(0)  # 中心频段设置为0
                    info.append(channel)
                    info.append(0)
                    info.append(0)
                    info.append(t60)
                    # 下面内容都为0
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    info.append(0)
                    copy_info = info
                    if fre_band == 30:
                        info[15] = 0
                    csv_writer.writerow(info)
            # if j==len(values)-1:
            #      copy_info[10] = copy_info[10] + 1 #中心频率设置为30
            #      copy_info[15] = 0
            #      csv_writer.writerow(copy_info)

    resultsHandle.close()
    return  resultsFileName





parser.add_argument("--xls_file",default="./process_chart/extra_add_with_zky.xlsx",type=str)
#parser.add_argument("--csv_file",default="/data2/new_wzd/36_room_val_code/02_06_val_data.csv",type=str)
parser.add_argument("--split_key",default="T60 AHM:",type=str)
parser.add_argument("--freq_num",default="14",type=str)  #11对应250Hz,14对应500hz,

parser.add_argument("--split_internal",default=0.1,type=float)
<<<<<<< HEAD
parser.add_argument('--rir_dir',default="./ZKY",type=str)
parser.add_argument("--output_dir",default="./add_with_zky_0316",type=str)
parser.add_argument("--gen_convwav_shell",default='./conv_zky_0316.sh',type = str)
=======
parser.add_argument('--rir_dir',default="/data2/TEAM/AIR_dataset/Openair",type=str)
parser.add_argument("--output_dir",default="./add_without_zky_0316",type=str)
parser.add_argument("--gen_convwav_shell",default='./conv_wav.sh',type = str)
>>>>>>> fc5277abe523b1d0b08cbec7834b003445c3a074
# parser.add_argument("--nohup_convwav_shell",default='/data2/new_wzd/36_room_val_code/nohup_conv_wav.sh',type = str)


# def convert_xls2csv(xls_file):
#     return csv
#

if __name__ == "__main__":
    args = parser.parse_args()
    # xls_file = args.xls_file
    #file = "./new_val_data.xls"
    csv_file = excel_to_csv(args.xls_file)
    remove_lst = []
    nohup_lst = []

    shell_file = open(args.gen_convwav_shell, 'w')

    # shell_file = open(csv_file, 'a')

    with open(csv_file, 'r') as f:
    # with open(args.csv_file,'r') as f:
        f_csv = csv.reader(f)
        key_index = None
        headers = next(f_csv)
        for head_str_i in range(len(headers)):
            if headers[head_str_i] == args.split_key:
                key_index = head_str_i
                break

        data_dict = {}
        for row in f_csv:
            if str(row[11])  == args.freq_num:
                key = round(float(row[key_index]),1)
                value = row
                if not key in data_dict.keys():
                    data_dict[key] = [value]
                else:
                    data_dict[key].append(value)
            else:
                continue

        min_key = min(data_dict.keys())
        max_key = max(data_dict.keys())
        c = 0
        for key in np.arange(min_key,max_key,round(args.split_internal,1)):
            if not key in data_dict.keys():
                continue
            key = round(key,1)
            save_dir = os.path.join(args.output_dir,"split_%s" %(str(key).replace(".","_")))
            conv_wav_dir = os.path.join(args.output_dir,"split_%d_conv_wav" %(c))

            c+=1
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            values = data_dict[key]
            for value in values:
                scene_name = value[7]
                room_name = value[3]
                # config_name = value[8]
                src_path = os.path.join(args.rir_dir,scene_name,room_name + ".wav")
                scene_dir = os.path.join(save_dir,scene_name)
                if not os.path.exists(scene_dir):
                    os.makedirs(scene_dir)

                dst_path = os.path.join(save_dir,scene_name,room_name + ".wav")
                shutil.copy(src_path,dst_path)
                shell_str = "python main.py --CORPUS_INPUT_FOLDER_ROOT %s --CORPUS_OUTPUT_FOLDER_ROOT %s  --need_config %s --MIC_CONFIGs %s\n" % (
                save_dir, args.output_dir,scene_name,scene_name)
                remove_lst.append(shell_str)

    temp_lists = list(set(remove_lst))
    for i in range(len(temp_lists)):
        log_name = temp_lists[i].split('--MIC_CONFIGs')[-1].split("\n")[0].strip() + '.log'
        nohup_shell = "nohup" + " " + temp_lists[i].split('\n')[0] + " " + ">%s 2>&1 &" % (log_name) + "\n"
        nohup_lst.append(nohup_shell)
    print(len(nohup_lst))

    for i in nohup_lst:
        shell_file.write(i)
    shell_file.close()
    print('finished!!!')

















