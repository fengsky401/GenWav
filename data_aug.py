# -*- coding: utf-8 -*-
"""
@file      :  SSIMLoss.py
@Time      :  2023/3/13
@Software  :  PyCharm
@summary   :
@Author    :
"""
import os
import argparse
import glob
import librosa
import random
import numpy as np


parser = argparse.ArgumentParser(description='load these files')
parser.add_argument('--input_rir_path', default='/data2/new_wzd/36_room_new_val/', type=str, help='load ')
parser.add_argument('--output_train_data_root', default='/data2/new_wzd/20230313_rubbish/', type=str)
parser.add_argument('--clean_speaker', default='/data2/cql/code/augu_data/concatPeople/chinese_concat', type=str)
parser.add_argument('--noise_dir', default="/data2/TEAM/Noise_TUT/TUT-acoustic-scenes-2017-development/audio", type=str)
parser.add_argument('--fs', default=16000, type=int)
parser.add_argument('--channel', default=1, type=int)
args = parser.parse_args()


input_rir_path = args.input_rir_path
output_train_data_root = args.output_train_data_root
clean_speaker = args.clean_speaker
noise_file_path = args.noise_dir
channel = args.channel


fs = args.fs


# TODO find files of rir
rir_scene_path = [os.path.join(args.input_rir_path, i) for i in os.listdir(input_rir_path)]
rir_file_path = sum([glob.glob(i+"/*.wav") for i in rir_scene_path], [])


# TODO find files of cleaner_speaker
clean_speaker_file = sum([glob.glob(clean_speaker+"/*.wav")], [])


# TODO find files of noise
noise_files = sum([glob.glob(noise_file_path+"/*.wav")], [])
rand_noise_file = random.sample(noise_files, 15)


# TODO modify  fs  channel
h_rir, rir_sr = librosa.load(rir_file_path[0], sr=fs, mono=False)
clean, clean_sr = librosa.load(clean_speaker_file[0], sr=fs, mono=False)
noise_file, noise_fs = librosa.load(noise_files[1], sr=fs, mono=False)


# 通道统一，以？为基准对齐，对通道做逻辑判断
# 卷积后的对应, 场景_房间_说话人.wav


if h_rir.ndim == 1:
    channel = 1


A = np.convolve(h_rir, clean)

# 卷积和干净的语料卷积的函数








# 通过读取做的csv读取找到对应的rir， xls文件 做拼接然后[场景  房间]


# 开始卷积，这块的内容是
# 想起来了， 咋们t60加噪音吗？ dB 噪音的命名  信噪比的噪声
# 生成wav文件：  ’输出文件的命名‘  男女声说话  +  rir的场景  +  rir的房间


# 逻辑判断












































