import csv
import pandas as pd
import debug_flag
import numpy as np


def readInT60DRRSubband(csv_file):

    if debug_flag.QUEENIE_DEBUG == 1:
        csv_file = r"E:\yousonic_code\ACE Chanllege\Data\20150225T195903_test_t60_DRR_measurement_results.csv"
    data = pd.read_csv(csv_file)
    print(data)
    resultsScan = data.values
    results = {}
    results["testID"] = resultsScan[:,0]
    results["version"] = resultsScan[:,1]
    results["fs"]= resultsScan[:,2]
    results["room"] = resultsScan[:,3]

    results["sessionID"]= resultsScan[:,4]

    results["micPos"] = resultsScan[:,5]

    results["srcPos"] = resultsScan[:,6]

    # 为啥要用去除空格
    results["config"]= np.array([resultsScan[:,7][i].replace(" ","") for i in range(len(resultsScan[:,7]))])

    results["recType"] = resultsScan[:,8]

    results["rirName"] = resultsScan[:,9]

    results["freqBand"]= resultsScan[:,10]

    results["centreFreq"] = resultsScan[:,11]

    results["channel"] = resultsScan[:,12]

    results["DRR"] = resultsScan[:,13]

    results["DRRMean"]= resultsScan[:,14]

    results["T60AHM"] = resultsScan[:,15]

    results["T60AHMMean"] = resultsScan[:,18]

    results["DRRFullband"] = resultsScan[:,22]

    results["DRRFullbandMean"] = resultsScan[:,23]

    results["T60AHMFullband"]= resultsScan[:,24]

    results["T60AHMFullbandMean"] = resultsScan[:,27]

   
    return results

