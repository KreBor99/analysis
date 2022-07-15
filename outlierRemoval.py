import os
import csv
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score

global truths
truths = []


# to smooth the data
def movAvg(X, window):
    newX = X
    for i in range(window, len(X) - window):
        temp = X[i]
        for j in range(1, window + 1):
            temp = temp + X[i - j] + X[i + j]
        temp = temp / (2 * window + 1)
        newX[i] = temp
    return newX


# set the directory of the file to our current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# read the outputs
def json_to_arr(json_filename):
    pixelx = []
    pixely = []
    timestp = []
    group = []
    id = 0  # index of gaze points
    group.append(id)  # this is to indicate which group each line belongs to
    os.chdir("/home/kre8or/PycharmProjects/analysis/experimentdata")
    with open(json_filename) as f:
        json_dict = json.load(f)
    # print(json_dict['perimeter_experiment']['points'][0])
    for point in json_dict['points']:  # loop through list
        pixelx.append(point[0])
        pixely.append(point[1])
        timestp.append(
            point[3])  # this is the timestamp of the ground truth points (will be used for matching the csv frames)
        if len(pixelx) > 1 and pixelx[-1] == pixelx[-2] and pixely[-1] == pixely[-2]:
            group.append(id)
        elif len(pixelx) > 1:
            id = id + 1
            group.append(id)

    return pixelx, pixely, timestp, group


def removeOutlier(file):
    if str(file).__contains__("subject_11") or str(file).__contains__("subject_10"):
        csv_filename = file
        json_filename = re.sub("_device_0.csv", '', file) + ".json"
    elif file == "":
        return
    else:
        csv_filename = file
        json_filename = file.rstrip("_device_0.csv") + ".json"
    #print(csv_filename)
    #print(json_filename)
    pixelx, pixely, timestp_gt, group = json_to_arr(json_filename)  # timestp_gt is the timestamp from the json file

    # print("number of frames read from json is ", len(pixelx))

    # 5 inputs, angle_x/y, head position x/y/z
    # 11, 12 | 294 - 295 (id in the csv file)
    anglex = []
    angley = []
    # headpox = []
    # headpoy = []
    # headpoz = []
    # headrox = []
    # headroy = []
    # headroz = []
    timestp_m = []  # timestamp from the csv file
    invalid_frames = 0
    flag = 0

    # read the csv into dictionary and then extract the required data into arrays
    with open(csv_filename, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if flag == 0:
                current_timestamp = float(row['timestamp'])
                delta = abs(current_timestamp - timestp_gt[0])
                # print("gotten to the point of measuring the delta")
                if delta < 0.02:
                    flag = 1
                    anglex.append(
                        float(row['gaze_angle_x']))  # if need other variables, simply use the name of the column
                    angley.append(float(row['gaze_angle_y']))
                    timestp_m.append(float(row['timestamp']))
                    if row['confidence'] == '0':
                        invalid_frames = invalid_frames + 1
            elif flag == 1 and len(anglex) < len(pixelx):
                anglex.append(float(row['gaze_angle_x']))
                angley.append(float(row['gaze_angle_y']))
                # headpox.append(float(row['pose_Tx']))
                # headpoy.append(float(row['pose_Ty']))
                # headpoz.append(float(row['pose_Tz']))
                # headrox.append(float(row['pose_Rx']))
                # headroy.append(float(row['pose_Ry']))
                # headroz.append(float(row['pose_Rz']))
                timestp_m.append(float(row['timestamp']))
                if row['confidence'] == '0':
                    invalid_frames = invalid_frames + 1

    #if invalid_frames > 0:
        #print("There are ", invalid_frames, " invalid frames in this dataset, please check !")
    if len(anglex) != len(group):
        #print("Skipping " + file)
        return
    for i in range(0, group[-1] + 1):
        group_anglex = []
        group_angley = []
        flag = 0
        group_start = 0
        for j in range(0, len(group)):
            if group[j] == i:
                if flag == 0:
                    flag = 1
                    group_start = j
                group_anglex.append(anglex[j])
                group_angley.append(angley[j])
        group_anglex = np.array(group_anglex)
        group_angley = np.array(group_angley)
        x_mean = np.mean(group_anglex, axis=0)
        x_sd = np.std(group_anglex, axis=0)
        y_mean = np.mean(group_angley, axis=0)
        y_sd = np.std(group_angley, axis=0)
        outliers = []
        for n in range(0, len(group_anglex)):
            if abs(group_anglex[n] - x_mean) > 2 * x_sd or abs(group_angley[n] - y_mean) > 2 * y_sd:
                outliers.append(n)
        for j in range(0, len(outliers)):
            anglex.pop(outliers[j] + group_start - j)
            angley.pop(outliers[j] + group_start - j)
            # headpox.pop(outliers[j] + group_start - j)
            timestp_m.pop(outliers[j] + group_start - j)  # added to get timestamp to the end.
            # headpoy.pop(outliers[j] + group_start - j)
            # headpoz.pop(outliers[j] + group_start - j)
            # headrox.pop(outliers[j] + group_start - j)
            # headroy.pop(outliers[j] + group_start - j)
            # headroz.pop(outliers[j] + group_start - j)
            group.pop(outliers[j] + group_start - j)
            pixelx.pop(outliers[j] + group_start - j)
            pixely.pop(outliers[j] + group_start - j)
    #print("After outlier removal, ", len(anglex), " timeframes of data are left.")
    # end of outlier removal

    # smooth the data before training
    window = 9
    anglex = movAvg(anglex, window)
    angley = movAvg(angley, window)
    # headpox = movAvg(headpox, window)
    # headpoy = movAvg(headpoy, window)
    # headpoz = movAvg(headpoz, window)
    # headrox = movAvg(headrox, window)
    # headroy = movAvg(headroy, window)
    # headroz = movAvg(headroz, window)
    timestp_m = movAvg(timestp_m, window)  # added to smooth time stamp data

    df = pd.DataFrame({'x_1': anglex,  # x1
                       'x_2': angley,  # x2
                       'tmsmp': timestp_m,
                       'group': group
                       })

    return df
