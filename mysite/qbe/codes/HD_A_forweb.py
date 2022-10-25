import csv
import re
import matplotlib.pyplot as plt # plt 用於顯示圖片
import matplotlib.image as mpimg # mpimg 用於讀取圖片
import numpy as np
import cv2
import os
import score
import readOutFile
from operator import itemgetter

filename = "HD1_forweb"

def combine(data, MainDataHis, num) :
    # 比較
    HisDifList = []
    dif = data.copy()
    for i in range(len(data)-num) :
        HisDif = 0
        for pos in range(10) :
            dif[i][pos] = data[i][pos] - MainDataHis[pos]
            if (dif[i][pos] < 0) :
                dif[i][pos] = dif[i][pos] *(-1)
            HisDif += dif[i][pos]
        HisDifList.append(HisDif)
    return HisDifList

def HD(data, MainData, num) :
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
    return combine(HisData, MainDataHis, num)

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
    # print("newdata")
    # print(newdata)
    data = []
    for i in range(len(newdata)) :
        if (i < 100) :
            data.append(newdata[i][1])
    print("data", data)



def main() :
    # 主要比對圖片
    MainData = ['27', '27', '29', '32', '30', '30', '30', '30', '36', '42', '26', '25', '28', '34', '32', '31', '30', '36', '42', '41', '24', '24', '24', '33', '34', '38', '42', '42', '40', '41', '24', '24', '24', '30', '42', '38', '42', '38', '40', '44', '24', '24', '24', '24', '34', '37', '30', '38', '44', '34', '32', '28', '24', '24', '34', '39', '37', '44', '44', '21', '35', '35', '30', '32', '39', '38', '37', '40', '44', '21', '35', '35', '34', '35', '35', '36', '37', '37', '33', '21', '31', '31', '33', '35', '35', '35', '36', '37', '29', '21', '27', '27', '31', '35', '35', '35', '35', '34', '29', '23']
    # list 裝要比對的時間
    dataSelect = ['2018/12/31 22:00', '2018/12/31 17:00', '2018/12/30 22:00', '2018/12/20 22:00', '2018/12/30 10:00', '2018/12/5 09:00', '2018/11/9 06:00', '2018/11/2 22:00', '2018/11/2 20:00', '2018/10/17 10:00']
    # 裝每小時的100筆空汙資料
    data = []
    # 讀入csv檔
    with open('2018mirco.csv', newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            data.append(row)
    data = data[:len(data)-1]
    # list 裝要比對的時間的PM2.5值
    dataSelectPM25 = chooseData(dataSelect, data)

    # 轉換資料型態
    changeType(dataSelectPM25)
    changeTypeTwo(MainData)
    # 分成10等分
    part(dataSelectPM25)
    partTwo(MainData)

    # 轉換成Histogram
    ans = []
    ans = HD(dataSelectPM25,MainData, 1)
    
    # 排名
    ranking(ans, dataSelect)
    
if __name__ == '__main__' :
    main()