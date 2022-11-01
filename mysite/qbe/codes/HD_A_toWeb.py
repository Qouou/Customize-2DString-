import csv
import re
import matplotlib.pyplot as plt # plt 用於顯示圖片
import matplotlib.image as mpimg # mpimg 用於讀取圖片
import numpy as np
# import cv2
import os
from operator import itemgetter
import sys

filename = "HD1_forweb"

def combine(data, MainDataHis) :
    # 比較
    HisDifList = []
    dif = data.copy()
    for i in range(len(data)) :
        HisDif = 0
        for pos in range(10) :
            dif[i][pos] = data[i][pos] - MainDataHis[pos]
            if (dif[i][pos] < 0) :
                dif[i][pos] = dif[i][pos] *(-1)
            HisDif += dif[i][pos]
        HisDifList.append(HisDif)
    return HisDifList

def HD(data, MainData) :
    # HisData = 計算後的直方圖
    HisData = []
    for r in range(1, len(data)) :
        His = plt.hist(data[r][1:], bins=10, range=[0, 10])
        # 直方圖的y軸值
        y = His[0]
        HisData.append(y)
    MainDataHis = []
    His = plt.hist(MainData, bins=10, range=[0, 10])
    MainDataHis = His[0] # 直方圖的y軸值

    # 裝cut的list
    return combine(HisData, MainDataHis)

def part(data) :
    # 各等級的下界
    levelList = [-1, 7.5, 15.5, 25.5, 35.5, 45.5, 54.5, 102.5, 150.5, 250.5, 500]
    for r in range(1, len(data)) :
        for c in range(1, len(data[0])) :
            for i in range(11) :
                if (levelList[i] > data[r][c]) :
                    data[r][c] = i
                    break
def partTwo(data) :
    # 各等級的下界
    levelList = [-1, 7.5, 15.5, 25.5, 35.5, 45.5, 54.5, 102.5, 150.5, 250.5, 500]
    for r in range(1, len(data)) :
        for i in range(11) :
            if (levelList[i] > data[r]) :
                data[r] = i
                break

def changeType(data) :
    for i in range(1, len(data)) :
        for v in range(1, len(data[0])) :
            data[i][v] = int(data[i][v])

def changeTypeTwo(data) :
    for i in range(1, len(data)) :
        data[i] = int(data[i])

# 選出要比較時間的 PM2.5 資料
def chooseData(dataSelect, data) :
    newdata = []
    for i in range(len(dataSelect)):
        for j in range(len(data)) :
            if (dataSelect[i] == data[j][0]) :
                newdata.append(data[j])

    return newdata

def ranking(ans, dataSelect) :
    newdata = []
    # 先合併成一個 list
    for i in range(len(ans)) :
        newdata.append([ans[i], dataSelect[i]])

    # 拿 list 中的第 0 項排列
    newdata = sorted(newdata, key=itemgetter(0))
    finaldata = []
    for i in range(len(newdata)) :
        if (i < 100) :
            finaldata.append(newdata[i][1])
    # print("data", finaldata)
    return finaldata

def takeDataTime(data) :
    newdata = []
    for i in range(1,len(data)) :
        newdata.append(data[i][0])
    return newdata

def takepm25(data, MainData) :
    need = 0
    for i in range(len(data)) :
        if (data[i][0] == MainData) :
            need = data[i][1:]
            break
    # print("need" , data[i][1:])
    return need


def main(argv) :
    # 主要比對圖片
    # MainData = '2018/12/31 17:00'
    MainData = argv[0]    # the frame want to be compared
    # list 裝要比對的時間
    # dataSelect = ['2018/12/31 22:00', '2018/12/31 17:00', '2018/12/30 22:00', '2018/12/20 22:00', '2018/12/30 10:00', '2018/12/5 09:00', '2018/11/9 06:00', '2018/11/2 22:00', '2018/11/2 20:00', '2018/10/17 10:00']
    # 裝每小時的100筆空汙資料
    data = []
    # 讀入csv檔
    with open('2018mirco.csv', newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            data.append(row)
    data = data[:len(data)-1]
    
    PicData = takepm25(data, MainData)

    changeType(data)
    part(data)

    # 轉換成Histogram
    ans = []
    ans = HD(data, PicData)
    DataTime = takeDataTime(data)
    # print(DataTime)

    # 排名
    result = ranking(ans, DataTime)
    for time in result:
        print(time)
    
if __name__ == '__main__' :
    main(sys.argv[1:])