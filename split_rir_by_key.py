import os
import csv
import argparse

parser = argparse.ArgumentParser()
#创建解析器
#ArgumentParser 对象包含将命令行解析成 Python 数据类型所需的全部信息。

parser.add_argument("--csv_file",default='C:\Users\17579\Desktop\新建文件夹\TAE_Train\Data_Aug\Step_1\test_1.csv',type=str)
parser.add_argument("--split_key",default="test_1.csv",type=str)
parser.add_argument("--split_internal",default=0.1,type=float)
parser.add_argument("--output_dir",default=None,type=str)

if __name__ == "__main__":
    args = parser.parse_args()
    with open(args.csv_file,'r') as f:
        f_csv = csv.reader(f)


