import csv
import matplotlib.pyplot as plt # plt 用於顯示圖片
import matplotlib.image as mpimg # mpimg 用於讀取圖片
import numpy as np
# import cv2
# import os
# import score
# import readOutFile
import sys

filename = "rasterScan_D_toWeb"


def Combine(Data, PicData) :
    newdata = []
    for r in range(len(Data)-1) :
        allcount = 0
        for i in range(1,len(Data[r])) :
            count = Data[r][i] - PicData[i-1]
            if count < 0 :
                count = count * -1
            allcount = allcount + count
        newdata.append(allcount)
    return newdata

def takeDataTime(data) :
    # print("data length check", len(data))
    newdata = []
    for i in range(1,len(data)) :
        newdata.append(data[i][0])
    return newdata

def turnScore(data) :
    minScore = min(data)
    maxScore = max(data)
    standard = maxScore - minScore
    for i in range(len(data)) :
        data[i] = 1 - ((data[i] - minScore) / standard)
    # print(data)
    return data

def ranking(ans, dataSelect) :
    newdata = []
    # 先合併成一個 list
    # print("ans big big", len(ans))
    # print("dataSelect", len(dataSelect))
    for i in range(len(ans)) :
        newdata.append([ans[i], dataSelect[i]])

    # 拿 list 中的第 0 項排列
    newdata = sorted(newdata)#, key=itemgetter(0)
    # , reverse=True
    finaldata = []
    for i in range(len(newdata)-1, len(newdata)-101, -1) :
        finaldata.append(newdata[i])
    # print(len(finaldata))
    rank = 0
    backdataScore = -1
    manySame = 0
    for i in range(100) :
        if (finaldata[i][0] == backdataScore) :
            finaldata[i].append(rank)
            manySame = manySame + 1
        else :
            backdataScore = finaldata[i][0]
            rank = rank + manySame + 1
            finaldata[i].append(rank)
            manySame = 0

    # print("data", finaldata)
    return finaldata

def takepm25(data, MainData) :
    need = []
    for i in range(len(data)) :
        # print(data[i][0])
        if (data[i][0] == MainData) :
            need = data[i][1:]
            # break
            # print("MainData", data[i][1:])
            return data[i][1:]

        # print("MainData", data[i][1:])
    return need

def RasterScan(data, PicData) :
    Data = []
    DataNum = 0
    for r in range(1, len(data)) :
        y = []
        y.append(data[r][0])
        for i in range(1, len(data[r])) :
            DataNum = data[r][i]
            y.append(DataNum)
        Data.append(y)
    # Data = backto(data, Data)
    
    cutData = Combine(Data, PicData)
    return cutData

def backtoData(data) :
    month = 1
    date = 1
    hour = 0
    dateList = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    hourList = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]
    # 紀錄沒有資料的
    noData = []
    pos = 1
    for i in range(365*24) :
        name = "2018/" + str(month) + "/" + str(date) + " " + str(hourList[hour]) + ":00"
        if (data[pos][0] != name) :
            noData.append(name)
            pos = pos - 1
        else :
            noData.append(data[pos][0])
        pos = pos + 1
        hour = hour + 1
        if (hour > 23) :
            hour = 0
            date = date + 1
        if (date > dateList[month-1]) :
            date = 1
            month = month + 1
    return noData

def changeType(data) :
    for i in range(1, len(data)) :
        for v in range(1, len(data[0])) :
            data[i][v] = int(data[i][v])
def changeTypeOne(data) :
    for i in range(len(data)) :
        data[i] = int(data[i])

def backto(data, cut) :
    # noData = 沒資料的日期
    noData = []
    noData = checkDate(data)
    # 把資料位置恢復
    newcut = []
    cutpos = 0
    Dpos = 0
    for i in range(365*24) :
        if (i == noData[Dpos]) :
            newcut.append(np.array([ 0.,  0., 0., 0.,  0.,  0.,  0.,  0.,  0.,  0.]))
            Dpos = Dpos + 1
        else :
            newcut.append(cut[cutpos])
            cutpos = cutpos + 1
    return newcut

def checkDate(data) :
    month = 1
    date = 1
    hour = 0
    dateList = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    hourList = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]
    # 紀錄沒有資料的
    noData = []
    pos = 1
    for i in range(365*24) :
        name = "2018/" + str(month) + "/" + str(date) + " " + str(hourList[hour]) + ":00"
        if (data[pos][0] != name) :
            noData.append(i)
            pos = pos - 1
        pos = pos + 1
        hour = hour + 1
        if (hour > 23) :
            hour = 0
            date = date + 1
        if (date > dateList[month-1]) :
            date = 1
            month = month + 1
    return noData

def main(argv) :
    # 主要比對圖片
    # print(argv)
    # MainData = argv[0]
    MainData = argv[0] + " " + argv[1]
    data = []
    # 讀入csv檔
    with open('2018mirco.csv', newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            data.append(row)
    PicData = takepm25(data, MainData)
    changeType(data)
    changeTypeOne(PicData)

    ans = []

    ans = RasterScan(data, PicData)
    # print("ans", ans)
    # print("orignal", len(data))

    DataTime = takeDataTime(data)
    # print("get in change ans")
    ans = turnScore(ans)

    # 排名
    result = ranking(ans, DataTime)
    # print(result)
    for time in result:
        print(*time)

if __name__ == '__main__' :
    main(sys.argv[1:])