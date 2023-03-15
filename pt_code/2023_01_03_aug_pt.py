# -*- coding: utf-8 -*-
"""
@file      :  0922_STI_slice_pt_for_FPN.py
@Time      :  2022/9/22 09:34
@Software  :  PyCharm
@summary   :  生成整张语谱图的图片，然后带上clean的语谱图，同时参考rir的起始点进行切分
@Author    :  Bajian Xiang
"""

import numpy as np
from scipy.signal import lfilter
import gtg
import splweighting
import wave
import glob
import os
import re
import torch
import pandas as pd
import argparse
from gen_specgram import All_Frequency_Spec


##configuration area
chunk_length = 4
chunk_overlap = 0.5

parser = argparse.ArgumentParser(description='manual to this script')
# 切分用倍频程
parser.add_argument('--csv_file', type=str,
                    default="/data2/new_wzd/36_room_val_code/pt_code/cat_csv.csv")
parser.add_argument('--dir_str', type=str,
                    default="/data2/new_wzd/36_val_output_dir/Dev/Speech/trollers-gill")
parser.add_argument('--save_dir', type=str,
                    default="/data1/wzd/02_07_new_val_data/trollers-gill/")

clean_speech_path = "/data2/cql/code/augu_data/concatPeople/chinese_concat/"


# rir_dict = {'BatteryQuarles_left': 1, 'yikehuichashi01_right': 9, 'BatteryQuarles_right': 1,
#             'yikehuilaobanshi01_right': 0,
#             'yikehuilaobanshi02_left': 8, 'xiaohedaban-01_right': 14, 'yikehuilaobanshi01_left': 26,
#             'BatteryBenson_left': 0,
#             'yikehuihuiyishi02_left': 2, 'junzheng5ktv01_right': 0, 'PortageCreekTunnel_left': 0,
#             'yiteng701dabangong01_left': 1,
#             'yikehuilaobanshi02_right': 34, 'junzheng5ktv01_left': 14, 'yiteng701dabangong01_right': 2,
#             'junzheng5ktv02_left': 17,
#             'xiaohedaban-01_left': 0, 'junzheng5ktv02_right': 5, 'CCRMAStairwell_right': 8,
#             'SewardWaterfrontPark_right': 0,
#             'SewardWaterfrontPark_left': 1, 'BatteryBrannan_left': 2, 'CCRMAStairwell_left': 2,
#             'RacquetballCourt_left': 1,
#             '3000CStreetGarageStairwell_left': 8, 'BatteryBrannan_right': 0, 'NancyLakeTunnel_right': 0,
#             'CedarCreekWinery_left': 0,
#             'TonyKnowlesCoastalTrailTunnel_right': 1, 'SquareVictoriaDome_left': 26, 'RacquetballCourt_right': 3,
#             '3000CStreetGarageStairwell_right': 0, 'NancyLakeTunnel_left': 2, 'GraffitiHallway_right': 4,
#             'GraffitiHallway_left': 3,
#             'TonyKnowlesCoastalTrailTunnel_left': 1, 'BatteryRandol_right': 1, 'StrathconaStairwellMcGill_right': 2,
#             'BatteryBenson_right': 1, 'PortageCreekTunnel_right': 0, 'HaleHolisticYogaStudio_right': 1,
#             'PabellonCulturalDeLaRepublica_left': 1, 'TransitCenter_left': 0, 'OutbackClimbingCenter_left': 1,
#             'HaleHolisticYogaStudio_left': 1, 'WaterplacePark_left': 1, 'BatteryRandol_left': 1, 'Natatorium_left': 0,
#             'LittlefieldLobby_left': 0, 'StrathconaStairwellMcGill_left': 0, 'OutbackClimbingCenter_right': 0,
#             'PabellonCulturalDeLaRepublica_right': 1, 'WaterplacePark_right': 0, 'TransitCenter_right': 0,
#             'ByronGlacier_left': 0,
#             'FatMansMisery_right': 0, 'CliffOfTheDawn_left': 1, 'QuadracciPavilion_right': 0, 'Amaranth_left': 0,
#             'FatMansMisery_left': 13,
#             'Amaranth_right': 0, 'ByronGlacier_right': 1, 'BatteryTolles_left': 1, 'FishCreekTrestleBridge_right': 0,
#             'FatMansSqueeze_right': 2, 'PabstBrewery_left': 1, 'ConvocationMall_left': 0, 'CliffOfTheDawn_right': 1,
#             'FishCreekTrestleBridge_left': 13, 'PabstBrewery_right': 1, 'ConvocationMall_right': 0,
#             'QuadracciPavilion_left': 1,
#             'junzheng3dahui02_left': 0, 'junzheng3dahui03_right': 0, 'junzheng304hui02_right': 6,
#             'xiaohedaban-03_left': 1,
#             'xiaohedaban-03_right': 11, 'junzheng5chashi01_left': 0, 'junzheng310hui02_right': 4,
#             'junzheng3dahui02_right': 0,
#             'yiteng701dabangong02_right': 35, 'junzheng304hui01_right': 3, 'xiaohedaban-02_left': 2,
#             'junzheng5chashi01_right': 10,
#             'junzheng310hui02_left': 5, 'junzheng310hui01_right': 1, 'junzheng3dahui03_left': 9,
#             'xiaohedaban-02_right': 3,
#             'junzheng3dahui01_left': 26, 'junzheng304hui01_left': 6, 'BatteryPowell_right': 0,
#             'PurgatoryChasm_right': 1,
#             'StorageTankNo7_right': 1, 'Avenue52UnderpassLARiver_left': 0, 'BoulevardRosemontUnderpass_right': 1,
#             'TheSlot_left': 0,
#             'WangenheimRareBooksRoom_left': 0, 'TheSlot_right': 0, 'LawrenceWelkCave_left': 28,
#             'WangenheimRareBooksRoom_right': 0,
#             'StorageTankNo7_left': 0, 'MillsGreekTheater_right': 0, 'LakeMerrittBART_right': 0,
#             'MillsGreekTheater_left': 2,
#             'LakeMerrittBART_left': 0, 'LawrenceWelkCave_right': 7, 'BoulevardRosemontUnderpass_left': 1,
#             'BatteryPowell_left': 0}

args = parser.parse_args()
save_dir = args.save_dir
if not os.path.exists(args.save_dir):
    os.makedirs(save_dir)
save_dir = args.save_dir
dir_str = args.dir_str
csv_file = args.csv_file


##functions
def SPLCal(x):
    Leng = len(x)
    pa = np.sqrt(np.sum(np.power(x, 2)) / Leng)
    p0 = 2e-5
    spl = 20 * np.log10(pa / p0)
    return spl

def get_rir_name(wav_file_name):
    # Four_Config_3000CStreetGarageStairwell_leftFour_Config__DR4_FCAG0_SX63_TIMIT_S_1000dB.wav
    room_name = wav_file_name.split('/')[-1].split('.')[0]
    config_name = wav_file_name.split('/')[-2]
    rir_name = room_name.split(config_name)[1].strip('_')
    speech_name = wav_file_name.split(config_name)[-1].split('TIMIT')[0].strip('_') + '.wav'
    return rir_name, speech_name


def cut_begin(wave, cut_time):
    res = wave[cut_time:]
    return res




##main loop, process eahc file in dir
# g = wave.open("clean_speech_example","rb")


class Totensor(object):
    """Convert ndarrays in sample to Tensors."""

    def __call__(self, sample):
        image, clean, ddr, t60, meanT60 = sample['image'], sample['clean'], sample['ddr'], sample['t60'], sample['MeanT60']

        # image, ddr, t60 = sample['image'], sample['ddr'], sample['t60']
        image = torch.from_numpy(image)
        clean = torch.from_numpy(clean)
        ddr = ddr.astype(float)
        t60 = t60.astype(float)
        meanT60 = meanT60.astype(float)
        # image = image.transpose((2, 0, 1))
        return {'image': image,
                'clean': clean,
                'ddr': torch.from_numpy(ddr),
                't60': torch.from_numpy(t60),
                "MeanT60": torch.from_numpy(meanT60)
                }
        #




if __name__ == '__main__':
    csv_data = pd.read_csv(csv_file)
    # print('csv data:', csv_data)

    # csv_data = pd.read_csv()
    for file_name in glob.glob(dir_str + r"/*.wav"):
        f = wave.open(file_name, "rb")
        params = f.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]
        print('file_name:', file_name)
        # TODO 从file_name中提取出需要的rir_room名，拿到cut_time
        rir_name, speech_name = get_rir_name(file_name)
        print('info:', nchannels, sampwidth, framerate, nframes / framerate)

        # if rir_name in rir_dict.keys():
        #     cut_index = rir_dict[rir_name]
        # else:
        #     print('DO NOT FIND:', rir_name, '-- for -- ', file_name)
        #     break

        str_data = f.readframes(nframes)
        f.close()
        wave_data = np.frombuffer(str_data, dtype=np.int16)

        # TODO 切掉RIR前面的部分
        # wave_data = cut_begin(wave_data, cut_index)

        wave_data.shape = -1, nchannels
        wave_data = wave_data.T
        audio_time = nframes / framerate
        chan_num = 0
        count = 0

        # TODO 读取干净语音，并进行相同的操作
        temp_clean_path = clean_speech_path + speech_name  # /data/xbj/TIMIT/DR4_FDKN0_SI1081.wav
        if not os.path.exists(temp_clean_path):
            print('not find clean:', temp_clean_path)
            break
        # 读取clean_wav的data
        else:
            f = wave.open(temp_clean_path, "rb")
            params = f.getparams()
            cnchannels, csampwidth, cframerate, cnframes = params[:4]

            clean_str_data = f.readframes(cnframes)
            f.close()
            clean_wave_data = np.frombuffer(clean_str_data, dtype=np.int16)

            clean_wave_data.shape = -1, cnchannels
            clean_wave_data = clean_wave_data.T
            clean_audio_time = cnframes / cframerate
            clean_chan_num = 0
            clean_count = 0
        # Four_Config_3000CStreetGarageStairwell_leftFour_Config__DR4_FCAG0_SX63_TIMIT_S_1000dB.wav
        new_file_name = (file_name.split("\\")[-1]).split(".")[0]
        new_file_name = new_file_name.split("/")[-1]
        ## process each channel of audio

        for audio_samples_np, clean_audio_samples_np in zip(wave_data, clean_wave_data):

            whole_audio_SPL = SPLCal(audio_samples_np)  # 应该是算这个片段中语音出现的长度

            available_part_num = (audio_time - chunk_overlap) // (
                    chunk_length - chunk_overlap)  # 4*x - (x-1)*0.5 <= audio_time    x为available_part_num

            if available_part_num == 1:
                cut_parameters = [chunk_length]
            else:
                cut_parameters = np.arange(chunk_length,
                                           (chunk_length - chunk_overlap) * available_part_num + chunk_overlap,
                                           chunk_length)  # np.arange()函数第一个参数为起点，第二个参数为终点，第三个参数为步长（10秒）

            start_time = int(0)  # 开始时间设为0
            count = 0
            # 开始存储pt文件
            dict = {}
            save_data = []
            for t in cut_parameters:
                stop_time = int(t)  # pydub以毫秒为单位工作
                start = int(start_time * framerate)
                end = int((start_time + chunk_length) * framerate)

                audio_chunk = audio_samples_np[start:end]  # 音频切割按开始时间到结束时间切割
                clean_audio_chunk = clean_audio_samples_np[start:end]

                ##ingore chunks with no audio
                chunk_spl = SPLCal(audio_chunk)
                if whole_audio_SPL - chunk_spl >= 20:
                    continue

                ##file naming

                count += 1

                ##A weighting
                chunk_a_weighting = splweighting.weight_signal(audio_chunk, framerate)
                clean_chunk_a_weighting = splweighting.weight_signal(clean_audio_chunk, cframerate)

                ##gammatone
                chunk_result, _, _ = All_Frequency_Spec(chunk_a_weighting, framerate)
                clean_chunk_result, _, _ = All_Frequency_Spec(clean_chunk_a_weighting, cframerate)

                chan = chan_num + 1

                # Four_Config_3000CStreetGarageStairwell_leftFour_Config__DR4_FCAG0_SX63_TIMIT_S_1000dB.wav

                config = new_file_name.split("_")[0]
                # config = new_file_name.split("_")[0] + "_" + new_file_name.split("_")[1]
                if config == "dirac":
                    config = new_file_name.split("_")[0]  # +"_" + new_file_name.split("_")[1]
                    # room = new_file_name.split(config)[1][1:-1]
                    room = new_file_name.split(config)[1].strip('_')
                else:
                    config = new_file_name.split("_")[0]
                    # config = new_file_name.split("_")[0] + "_" + new_file_name.split("_")[1]
                    room = new_file_name.split(config)[1].strip('_')
                print('new_file_name:', new_file_name)

                a = (csv_data['Room:'] == room).values
                b = (csv_data['Room Config:'] == config).values

                data = csv_data[a]
                T60_data = data.loc[:, ['T60:']]
                print('T60_data:', T60_data)
                FB_T60_data = data.loc[:, ['FB T60:']]
                FB_T60_M_data = data.loc[:, ['FB T60 Mean (Ch):']]
                DDR_each_band = np.array([0 for i in range(30)])
                T60_each_band = (T60_data.values).reshape(-1)
                MeanT60_each_band = np.array([FB_T60_data, FB_T60_M_data])
                image = chunk_result
                clean_image = clean_chunk_result
                print('-- Reverb Image: ', image.shape, ' -- Clean Image:', clean_image.shape)
                sample = {'image': image, 'clean': clean_image, 'ddr': DDR_each_band, 't60': T60_each_band,
                          "MeanT60": MeanT60_each_band}
                transform = Totensor()
                sample = transform(sample)

                save_data.append(sample)

                start_time = start_time + chunk_length - chunk_overlap  # 开始时间变为结束时间前1s---------也就是叠加上一段音频末尾的4s

            if len(save_data) != 0:
                pt_file_name = os.path.join(save_dir, new_file_name + '-' + str(chan_num) + '.pt')
                dict[new_file_name + '-' + str(chan_num)] = save_data
                torch.save(dict, pt_file_name)
            chan_num = chan_num + 1
        print('----------------finish----------------')

