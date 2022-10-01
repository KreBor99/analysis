import pandas as pd
import math
import os
from tabulate import tabulate
from scipy.constants import degree

import outlierRemoval
import statistics

global truths
truths = []
global experiment
experiment = ""
global currentfile
currentfile = ""
global experimentnumber
experimentnumber = 0
global absx_experimenterror
absx_experimenterror = []
global absy_experimenterror
absy_experimenterror = []
global relx_experimenterror
relx_experimenterror = []
global rely_experimenterror
rely_experimenterror = []
global releventtruths
releventtruths = []
global x_experimenterror
x_experimenterror = []
global y_experimenterror
y_experimenterror = []
global allstats
allstats = []
global expcount
expcount = 0


def generategroundtruths():  # generates truths, which is an array of ground truth pairs to be evaluated against
    iterate = [0, 1, 2, 3, 4, 5]  # used to iterate in for loops
    distances = [30, 60, 90, 120, 150]
    original = [[5.6, 24.3], [47.7, 24.3], [47.7, 5.5], [5.6, 5.5],
                [26.65, 13]]  # locations of A-E in cm from bottom left of monitor
    monitor = [53, 30]
    for d in distances:
        original.append([monitor[0] / 2, monitor[1] / 2, d])  # appends the location of the user
        temptruths = []
        for i in iterate:  # calculates the xgaze and ygaze of the user for each of the points A-E
            xgaze = math.atan((original[4][0] - original[i][0]) / original[5][2])
            ygaze = math.atan((original[4][1] - original[i][1]) / original[5][2])
            temptruths.append([xgaze, ygaze])
        truths.append(temptruths)
        original.pop(5)
    return truths


def generatemovinggroundtruths():  # appends the groundtruths for the moving dot experiments.
    speeds = [12, 8, 6]
    original = [[6, 15.5], [47.2, 15.5], [26.5, 15.5, 60]]
    for i in speeds:
        temptruths = []
        max = i * 30
        counter = 0
        step = ((original[1][0] - original[0][0]) / i)
        while counter != max:
            xgaze = math.atan((original[2][0] - (original[0][0] + step * counter)) / original[2][2])
            ygaze = math.atan((original[2][1] - original[0][1]) / original[2][2])
            temptruths.append([xgaze, ygaze])
            counter = counter + 1
        truths.append(temptruths)


def printcsvcounter(experimentcounter):
    # print("Operated on " + str(experimentcounter) + " csvs")
    return


def findfiles2(experimentnumber):
    if experimentnumber == 1.3:
        experimentcounter = 0
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("30cm") and str(filename).__contains__(".csv"):
                experimentcounter += 1  # should something else be happening in here to use the files identified?
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    if experimentnumber == 1.6:
        experimentcounter = 0
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("60cm") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    if experimentnumber == 1.9:
        experimentnumber = 1.9
        experimentcounter = 0
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("90cm") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    if experimentnumber == 1.12:
        experimentnumber = 1.12
        experimentcounter = 0
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("120cm") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    if experimentnumber == 1.15:
        experimentnumber = 1.15
        experimentcounter = 0
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("150cm") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    if experimentnumber == -2.4:
        experimentnumber = -2.4
        experimentcounter = 0
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("steep-left-turn") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    if experimentnumber == -2.2:
        experimentnumber = -2.2
        experimentcounter = 0
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("shallow-left-turn") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    if experimentnumber == 2.2:
        experimentnumber = 2.2
        experimentcounter = 0
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("shallow-right-turn") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    if experimentnumber == 2.4:
        experimentnumber = 2.4
        experimentcounter = 0
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("steep-right-turn") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    if experimentnumber == 3:
        experimentcounter = 0
        experimentnumber = 3
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("glasses") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    if experimentnumber == 4.1:
        experimentnumber = 4.1
        experimentcounter = 0
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("camera-left") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    if experimentnumber == 4.2:
        experimentnumber = 4.2
        experimentcounter = 0
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("camera-right") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    if experimentnumber == 4.3:
        experimentnumber = 4.3
        experimentcounter = 0
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("camera-top") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    if experimentnumber == 5.6:
        experimentcounter = 0
        experimentnumber = 5.6
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("fast-movement") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    if experimentnumber == 5.8:
        experimentcounter = 0
        experimentnumber = 5.8
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("medium-movement") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    if experimentnumber == 5.12:
        experimentcounter = 0
        experimentnumber = 5.12
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("slow-movement") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    if experimentnumber == 6.1:
        experimentnumber = 6.1
        experimentcounter = 0
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("steep-left-lighting") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    if experimentnumber == 6.2:
        experimentnumber = 6.2
        experimentcounter = 0
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("shallow-left-lighting") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    if experimentnumber == 6.3:
        experimentnumber = 6.3
        experimentcounter = 0
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("shallow-right-lighting") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    if experimentnumber == 6.4:
        experimentnumber = 6.4
        experimentcounter = 0
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("steep-right-lighting") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    if experimentnumber == 7.1:
        experimentnumber = 7.1
        experimentcounter = 0
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("red-lighting") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    if experimentnumber == 7.2:
        experimentnumber = 7.2
        experimentcounter = 0
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("green-lighting") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    if experimentnumber == 7.3:
        experimentnumber = 7.3
        experimentcounter = 0
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("blue-lighting") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    if experimentnumber == 8:
        experimentnumber = 8
        experimentcounter = 0
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("IR-projector") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)


def findfiles(experimentnumber):
    grouperror = []
    abscsverror = []
    relcsverror = []
    if experimentnumber == 1:
        specify = int(input("Please enter which distance you'd like analyzed(30, 60, 90,120,150):\n"))
        if specify == 30:
            experimentnumber = 1.3
            experimentcounter = 0
            for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
                if str(filename).__contains__("30cm") and str(filename).__contains__(".csv"):
                    experimentcounter += 1  # should something else be happening in here to use the files identified?
                    if calculateerror(filename.name) == -1:
                        experimentcounter -= 1
            printcsvcounter(experimentcounter)
        if specify == 60:
            experimentnumber = 1.6
            experimentcounter = 0
            for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
                if str(filename).__contains__("60cm") and str(filename).__contains__(".csv"):
                    experimentcounter += 1
                    if calculateerror(filename.name) == -1:
                        experimentcounter -= 1
            printcsvcounter(experimentcounter)
        if specify == 90:
            experimentnumber = 1.9
            experimentcounter = 0
            for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
                if str(filename).__contains__("90cm") and str(filename).__contains__(".csv"):
                    experimentcounter += 1
                    if calculateerror(filename.name) == -1:
                        experimentcounter -= 1
            printcsvcounter(experimentcounter)
        if specify == 120:
            experimentnumber = 1.12
            experimentcounter = 0
            for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
                if str(filename).__contains__("120cm") and str(filename).__contains__(".csv"):
                    experimentcounter += 1
                    if calculateerror(filename.name) == -1:
                        experimentcounter -= 1
            printcsvcounter(experimentcounter)
        if specify == 150:
            experimentnumber = 1.15
            experimentcounter = 0
            for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
                if str(filename).__contains__("150cm") and str(filename).__contains__(".csv"):
                    experimentcounter += 1
                    if calculateerror(filename.name) == -1:
                        experimentcounter -= 1
            printcsvcounter(experimentcounter)
    if experimentnumber == 2:
        specify = int(input("Please select the rotation you'd like to analyze(-40, -20, 20, 40):\n"))
        if specify == -40:
            experimentnumber = -2.4
            experimentcounter = 0
            for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
                if str(filename).__contains__("steep-left-turn") and str(filename).__contains__(".csv"):
                    experimentcounter += 1
                    if calculateerror(filename.name) == -1:
                        experimentcounter -= 1
            printcsvcounter(experimentcounter)
        if specify == -20:
            experimentnumber = -2.2
            experimentcounter = 0
            for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
                if str(filename).__contains__("shallow-left-turn") and str(filename).__contains__(".csv"):
                    experimentcounter += 1
                    if calculateerror(filename.name) == -1:
                        experimentcounter -= 1
            printcsvcounter(experimentcounter)
        if specify == 20:
            experimentnumber = 2.2
            experimentcounter = 0
            for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
                if str(filename).__contains__("shallow-right-turn") and str(filename).__contains__(".csv"):
                    experimentcounter += 1
                    if calculateerror(filename.name) == -1:
                        experimentcounter -= 1
            printcsvcounter(experimentcounter)
        if specify == 40:
            experimentnumber = 2.4
            experimentcounter = 0
            for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
                if str(filename).__contains__("steep-right-turn") and str(filename).__contains__(".csv"):
                    experimentcounter += 1
                    if calculateerror(filename.name) == -1:
                        experimentcounter -= 1
            printcsvcounter(experimentcounter)
    if experimentnumber == 3:
        experimentcounter = 0
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("glasses") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    if experimentnumber == 4:
        specify = int(input("Please enter which camera position you'd like analyzed(1,2,3):\n1.Left\n2.Right\n3.Top"))
        if specify == 1:
            experimentnumber = 4.1
            experimentcounter = 0
            for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
                if str(filename).__contains__("camera-left") and str(filename).__contains__(".csv"):
                    experimentcounter += 1
                    if calculateerror(filename.name) == -1:
                        experimentcounter -= 1
            printcsvcounter(experimentcounter)
        if specify == 2:
            experimentnumber = 4.2
            experimentcounter = 0
            for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
                if str(filename).__contains__("camera-right") and str(filename).__contains__(".csv"):
                    experimentcounter += 1
                    if calculateerror(filename.name) == -1:
                        experimentcounter -= 1
            printcsvcounter(experimentcounter)
        if specify == 3:
            experimentnumber = 4.3
            experimentcounter = 0
            for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
                if str(filename).__contains__("camera-high") and str(filename).__contains__(".csv"):
                    experimentcounter += 1
                    if calculateerror(filename.name) == -1:
                        experimentcounter -= 1
            printcsvcounter(experimentcounter)
    if experimentnumber == 5:  ##This section doesn't work, jsons not trimmable
        specify = int(input("Please enter which movement speed you'd like analyzed(6,8,12):\n"))
        if specify == 6:
            experimentcounter = 0
            experimentnumber = 5.6
            for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
                if str(filename).__contains__("fast-movement") and str(filename).__contains__(".csv"):
                    experimentcounter += 1
                    if calculateerror(filename.name) == -1:
                        experimentcounter -= 1
            printcsvcounter(experimentcounter)
        if specify == 8:
            experimentcounter = 0
            experimentnumber = 5.8
            for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
                if str(filename).__contains__("medium-movement") and str(filename).__contains__(".csv"):
                    experimentcounter += 1
                    if calculateerror(filename.name) == -1:
                        experimentcounter -= 1
            printcsvcounter(experimentcounter)
        if specify == 12:
            experimentcounter = 0
            experimentnumber = 5.12
            for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
                if str(filename).__contains__("slow-movement") and str(filename).__contains__(".csv"):
                    experimentcounter += 1
                    if calculateerror(filename.name) == -1:
                        experimentcounter -= 1
            printcsvcounter(experimentcounter)

    # pick up adding continuous run here

    if experimentnumber == 6:
        specify = int(input("Please enter which direction you's like the light from:\n1. Steep Left\n2. Shallow "
                            "Left\n3. Shallow Right\n4. Steep Right"))
        if specify == 1:
            experimentnumber = 6.1
            experimentcounter = 0
            for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
                if str(filename).__contains__("steep-left-lighting") and str(filename).__contains__(".csv"):
                    experimentcounter += 1
                    if calculateerror(filename.name) == -1:
                        experimentcounter -= 1
            printcsvcounter(experimentcounter)
        if specify == 2:
            experimentnumber = 6.2
            experimentcounter = 0
            for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
                if str(filename).__contains__("shallow-left-lighting") and str(filename).__contains__(".csv"):
                    experimentcounter += 1
                    if calculateerror(filename.name) == -1:
                        experimentcounter -= 1
            printcsvcounter(experimentcounter)
        if specify == 3:
            experimentnumber = 6.3
            experimentcounter = 0
            for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
                if str(filename).__contains__("shallow-right-lighting") and str(filename).__contains__(".csv"):
                    experimentcounter += 1
                    if calculateerror(filename.name) == -1:
                        experimentcounter -= 1
            printcsvcounter(experimentcounter)
        if specify == 4:
            experimentnumber = 6.4
            experimentcounter = 0
            for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
                if str(filename).__contains__("steep-right-lighting") and str(filename).__contains__(".csv"):
                    experimentcounter += 1
                    if calculateerror(filename.name) == -1:
                        experimentcounter -= 1
            printcsvcounter(experimentcounter)
    if experimentnumber == 7:
        specify = int(input("Please enter which color you'd like to analyze:\n1. Red\n2. Green\n3. Blue\n"))
        if specify == 1:
            experimentnumber = 7.1
            experimentcounter = 0
            for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
                if str(filename).__contains__("red-lighting") and str(filename).__contains__(".csv"):
                    experimentcounter += 1
                    if calculateerror(filename.name) == -1:
                        experimentcounter -= 1
            printcsvcounter(experimentcounter)
        if specify == 2:
            experimentnumber = 7.2
            experimentcounter = 0
            for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
                if str(filename).__contains__("green-lighting") and str(filename).__contains__(".csv"):
                    experimentcounter += 1
                    if calculateerror(filename.name) == -1:
                        experimentcounter -= 1
            printcsvcounter(experimentcounter)
        if specify == 3:
            experimentnumber = 7.3
            experimentcounter = 0
            for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
                if str(filename).__contains__("blue-lighting") and str(filename).__contains__(".csv"):
                    experimentcounter += 1
                    if calculateerror(filename.name) == -1:
                        experimentcounter -= 1
            printcsvcounter(experimentcounter)
    if experimentnumber == 8:
        experimentcounter = 0
        for filename in os.scandir("/home/kre8or/PycharmProjects/analysis/experimentdata"):
            if str(filename).__contains__("IR-projector") and str(filename).__contains__(".csv"):
                experimentcounter += 1
                if calculateerror(filename.name) == -1:
                    experimentcounter -= 1
        printcsvcounter(experimentcounter)
    # trimmedfile = outlierRemoval.removeOutlier(currentfile)
    # print(trimmedfile)
    return


def calculateerror(currentfile):
    grouperror = []
    abscsverror = []
    relcsverror = []
    currenterror = []
    print(currentfile)
    currentdata = outlierRemoval.removeOutlier(currentfile)
    if type(currentdata) == None.__class__:
        return -1
    ####These if/elif/else statements decide which groundtruth to use####
    if experimentnumber == 1.3:
        releventtruths = truths[0]
    elif experimentnumber == 1.6:
        releventtruths = truths[1]
    elif experimentnumber == 1.9:
        releventtruths = truths[2]
    elif experimentnumber == 1.12:
        releventtruths = truths[3]
    elif experimentnumber == 1.12:
        releventtruths = truths[4]
    elif experimentnumber == 4:
        releventtruths = truths[2]
    elif experimentnumber == 5.12:
        releventtruths = truths[5]
    elif experimentnumber == 5.8:
        releventtruths = truths[6]
    elif experimentnumber == 5.6:
        releventtruths = truths[7]
    else:
        releventtruths = truths[1]
    # print("The relevant truth is below:")
    # print(releventtruths)
    currentdata = currentdata.reset_index()
    ####This forloop and if statements calculate the error for each group####
    for index, row in currentdata.iterrows():
        if row['group'] == 0:
            if releventtruths[0][0] == 0 or releventtruths[0][1] == 0:
                continue
            relxerror = (abs(releventtruths[0][0] - row['x_1'])) / releventtruths[0][0]
            relyerror = (abs(releventtruths[0][1] - row['x_2'])) / releventtruths[0][1]
            absxerror = (abs(releventtruths[0][0] - row['x_1']))
            absyerror = (abs(releventtruths[0][1] - row['x_2']))
            abscsverror.append([absxerror, absyerror])
            relcsverror.append([relxerror, relyerror])
        if row['group'] == 1:
            if releventtruths[1][0] == 0 or releventtruths[1][1] == 0:
                continue
            relxerror = (abs(releventtruths[1][0] - row['x_1'])) / releventtruths[1][0]
            relyerror = (abs(releventtruths[1][1] - row['x_2'])) / releventtruths[1][1]
            absxerror = (abs(releventtruths[1][0] - row['x_1']))
            absyerror = (abs(releventtruths[1][1] - row['x_2']))
            abscsverror.append([absxerror, absyerror])
            relcsverror.append([relxerror, relyerror])
        if row['group'] == 2:
            if releventtruths[2][0] == 0 or releventtruths[2][1] == 0:
                continue
            relxerror = (abs(releventtruths[2][0] - row['x_1'])) / releventtruths[2][0]
            relyerror = (abs(releventtruths[2][1] - row['x_2'])) / releventtruths[2][1]
            absxerror = (abs(releventtruths[2][0] - row['x_1']))
            absyerror = (abs(releventtruths[2][1] - row['x_2']))
            abscsverror.append([absxerror, absyerror])
            relcsverror.append([relxerror, relyerror])
        if row['group'] == 3:
            if releventtruths[3][0] == 0 or releventtruths[3][1] == 0:
                continue
            relxerror = (abs(releventtruths[3][0] - row['x_1'])) / releventtruths[3][0]
            relyerror = (abs(releventtruths[3][1] - row['x_2'])) / releventtruths[3][1]
            absxerror = (abs(releventtruths[3][0] - row['x_1']))
            absyerror = (abs(releventtruths[3][1] - row['x_2']))
            abscsverror.append([absxerror, absyerror])
            relcsverror.append([relxerror, relyerror])
        if row['group'] == 4:
            if releventtruths[4][0] == 0 or releventtruths[4][1] == 0:  ##this solution might not work, check again
                continue
            relxerror = (abs(releventtruths[4][0] - row['x_1'])) / releventtruths[4][0]
            relyerror = (abs(releventtruths[4][1] - row['x_2'])) / releventtruths[4][1]
            absxerror = (abs(releventtruths[4][0] - row['x_1']))
            absyerror = (abs(releventtruths[4][1] - row['x_2']))
            abscsverror.append([absxerror, absyerror])
            relcsverror.append([relxerror, relyerror])
        # print(abscsverror)
        # print(relcsverror)
    runningxavg = 0
    runningyavg = 0
    for item in abscsverror:
        runningxavg = runningxavg + item[0]
        runningyavg = runningyavg + item[1]
    absxavg = runningxavg / abscsverror.__len__()
    absyavg = runningyavg / abscsverror.__len__()
    absx_experimenterror.append(absxavg)
    absy_experimenterror.append(absyavg)
    runningxavg = 0
    runningyavg = 0
    for item in relcsverror:
        runningxavg = runningxavg + item[0]
        runningyavg = runningyavg + item[1]
    relxavg = runningxavg / relcsverror.__len__()
    relyavg = runningyavg / relcsverror.__len__()
    relx_experimenterror.append(relxavg)
    rely_experimenterror.append(relyavg)
    runningxavg = 0
    runningyavg = 0
    for item in abscsverror:
        runningxavg = runningxavg + item[0]
        runningyavg = runningyavg + item[1]
    absxavg = runningxavg / abscsverror.__len__()
    absyavg = runningyavg / abscsverror.__len__()
    absx_experimenterror.append(absxavg)
    absy_experimenterror.append(absyavg)
    return


def generategraphics():
    head = ["Experiment", "Relative x error", "Relative y error", "Absolute x error", "Absolute y error",
            "Standard deviation of data", "Standard Deviation of absolute Error"]
    print(tabulate(allstats, headers=head, tablefmt="grid"))
    return


# experimentnumber = int(
#    input("Please select which experiment you want to perform analysis on with its number\n1.Distance "
#          "\n2.Head Rotation\n3.Sunglasses/glasses\n4.Camera Position\n5.MovingDot\n6.Focus "
#          "Lighting\n7.RGB Lighting\n8.IR Projector\n9.Lighting Levels\n"))
experimentnumberlist = [1.3, 1.6, 1.9, 1.12, 1.15, -2.4, -2.2, 2.2, 2.4, 3, 4.1, 4.2, 4.3, 5.6, 5.8, 5.12, 6.1, 6.2, 6.3, 6.4, 7.1, 7.2, 7.3, 8]
generategroundtruths()
# while experimentnumber != 0:
for item in experimentnumberlist:
    temparray = []
    # findfiles(experimentnumber)
    findfiles2(item)
    temparray.append(item)
    #    print("The average relative x gaze error for this experiment is " + str(
    #        '{:.3g}'.format(math.fabs(statistics.mean(relx_experimenterror) * 100))) + "%")
    temparray.append(str('{:.3g}'.format(math.fabs(statistics.mean(relx_experimenterror) * 100))) + "%")
    #    print("The average relative y gaze error for this experiment is " + str(
    #        '{:.3g}'.format(math.fabs(statistics.mean(rely_experimenterror) * 100))) + "%")
    temparray.append(str('{:.3g}'.format(math.fabs(statistics.mean(rely_experimenterror) * 100))) + "%")
    #    print("The average absolute x gaze error for this experiment is " + str(
    #        '{:.3g}'.format(math.degrees(statistics.mean(absx_experimenterror)))) + " degrees")
    temparray.append(str('{:.3g}'.format(math.degrees(statistics.mean(absx_experimenterror)))) + " degrees")
    #    print("The average absolute y gaze error for this experiment is " + str(
    #        '{:.3g}'.format(math.degrees(statistics.mean(absy_experimenterror)))) + " degrees")
    temparray.append(str('{:.3g}'.format(math.degrees(statistics.mean(absy_experimenterror)))) + " degrees")
    allstats.append(temparray)
    # experimentcounter = 0
    x_experimenterror = []
    y_experimenterror = []
    expcount = expcount + 1
    # experimentnumber = int(
    #    input("Please select which experiment you want to perform analysis on with its number\n1.Distance "
    #          "\n2.Head Rotation\n3.Sunglasses/glasses\n4.Camera Position\n5.MovingDot\n6.Focus "
    #          "Lighting\n7.RGB Lighting\n8.IR Projector\n9.Lighting Levels\n"))
    # experimentnumber = int(input("Please make another selection, or 0 to exit\n"))
generategraphics()
print("Program has ended")
