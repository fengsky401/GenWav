import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--wave_dir',default="/data2/new_wzd/36_val_output_dir/Dev/Speech/", type=str)
parser.add_argument("--output_pt_dir",default="/data2/new_wzd/36_val_output_dir/Dev/pt_val_data/", type=str)
parser.add_argument("--gen_shell",default='/data2/new_wzd/36_room_val_code/pt_code/wav_to_pt.sh', type=str)
args = parser.parse_args()




# wave_parent_folder
# dir_str_head = "/data2/new_wzd/1000Hz/modif_output_wav/Dev/Speech/"
dir_str_head = args.wave_dir


sence_lst = os.listdir(dir_str_head)

# merge all csv in current folder
csv_file_list = []
# find all csv file needed
for k in range(len(sence_lst)):
    sence = os.path.join(dir_str_head, sence_lst[k])
    file = os.listdir(sence)
    # glob.glob(file + '/*.csv')
    for v in range(len(file)):
        if file[v].split(".")[-1] == 'csv':
            save_csv = os.path.join(sence, file[v])
            csv_file_list.append(save_csv)
# print(csv_file_list)



csv_file_str = " ".join(csv_file_list)
cat_csv_file = "cat_csv.csv"
os.system("cat %s > %s" % (csv_file_str, cat_csv_file))
csv_file = os.path.join(os.getcwd(), cat_csv_file)

# create pt_save folder
pt_save_path = args.output_pt_dir
for i in range(len(sence_lst)):
    pt_folder = os.path.join(pt_save_path, sence_lst[i])
    if not os.path.exists(pt_folder):  # 判断所在目录下是否有该文件名的文件夹
        os.mkdir(pt_folder)

threads = []
for i in range(len(sence_lst)):
    csv_file = csv_file
    wave_dir = os.path.join(dir_str_head, sence_lst[i])
    pt_save = os.path.join(pt_save_path, sence_lst[i])

    shell_name = "nohup python 2023_01_03_aug_pt.py --csv_file " + csv_file + " --dir_str " + wave_dir + "/" + " --save_dir " + pt_save + "/" + " >> ./%s.log 2>&1 &" % (sence_lst[i]) +"\n"
    threads.append(shell_name)

print(threads)

shell_file = open(args.gen_shell, 'a')

for i in threads:
    shell_file.write(i)
shell_file.close()

print('finished!!!')
