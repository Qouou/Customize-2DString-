import os
import csv
from collections import defaultdict
import sys
import time
# os.system("")
#該版本是返回最長公共子串和其長度，若只返回長度，則可以簡化
def lcs(s1, s2):
    l1 = len(s1)
    l2 = len(s2)
    # res[i][j]儲存子串s1[0:i] 和 子串s2[0:j] 的lcs串
    # num[i][j]儲存子串s1[0:i] 和 子串s2[0:j] 的lcs長度
    # 由於考慮到空串也作為比較元素，則將兩個字串的長度各加一
    res = [['' for i in range(l2+1)] for j in range(l1+1)]
    num = [[0 for i in range(l2+1)] for j in range(l1+1)]
    count = 0
    maxIndex = -1
    for i in range(1,l1+1):
        for j in range(1, l2+1):
            if s1[i-1] == s2[j-1]:
                count += 1
                if count == 1:
                    minIndex = i-1
                elif count > 0:
                    if i-1 > maxIndex:
                        maxIndex = i-1
                num[i][j] = num[i-1][j-1]+1
                res[i][j] = res[i-1][j-1] + s1[i-1]
            else:
                if num[i-1][j] > num[i][j-1]:
                    num[i][j] = max(num[i-1][j],num[i][j-1])
                    res[i][j] = res[i-1][j]
                else:
                    num[i][j] = num[i][j-1]
                    res[i][j] = res[i][j-1]
    #print(len(s1[minIndex:maxIndex]))
    #print(s1[minIndex:maxIndex])
    return num[-1][-1],res[-1][-1],minIndex,maxIndex

def segment(data):
    data = float(data)
    if data < 7.5:
        return 'A'
    elif data > 7.4 and data < 15.5:
        return 'B'
    elif data > 15.4 and data < 25.5:
        return 'C'
    elif data > 25.4 and data < 35.5:
        return 'D'
    elif data > 35.4 and data < 45.5:
        return 'E'
    elif data > 45.4 and data < 54.5:
        return 'F'
    elif data > 54.4 and data < 102.5:
        return 'G'
    elif data > 102.4 and data < 150.5:
        return 'H'
    elif data > 150.4 and data < 250.5:
        return 'I'
    else:
        return 'J'
    

def Similarity(Q, D, L, N, M):
    if M > 0:
        s = 1 - ((Q + D - 2 * L) / (4 * N + 1))
    else:
        s = 0 
    return s

def changePattern(string):
    i = 0
    newStr = ''
    while i < len(string)-1:
        if string[i] == '#':
            newStr += '#'
        elif string[i+1] == 'b':
            newStr += string[i]
        elif string[i+1] == 'e':
            newStr += string[i].lower()
        i += 1
    return newStr
def addLine(string):
    stringAfterChange = changePattern(string)
    i = 0 
    newStr = ''
    tmpBegin = ''
    tmpEnd = ''
    while i < len(stringAfterChange)-1:
        if stringAfterChange[i].islower():
            tmpEnd += stringAfterChange[i]
        elif stringAfterChange[i] == '#':
            i += 1
            continue
        else:
            tmpBegin += stringAfterChange[i]
        newStr += '#' + tmpBegin + '#' + tmpEnd
        tmpBegin = ''
        tmpEnd = ''
        i += 1
    return newStr

def Distance(M, original):
    i = 0
    start = -1
    end = -2
    while i < len(original):
        if original[i] == M[0] and start < 0:
            start = i
            i += 1
        elif start > 0 and original[i] == M[-1]:
            end = i
            break
        else:
            i += 1
    return original[start:end+1]

def Score(str1, str2): 
    # Str1 and Str2 are list of string including x and y
    # Str1 is string in library
    # Str2 is user's query

    parameter = {}
    N = len(str2[0].replace('#',''))/4
    newStr1 = []
    newStr2 = []
    # str1 and str2 LCS
    for i in str1:
        newStr1.append(addLine(i))
    for i in str2:
        newStr2.append(addLine(i))
    length_Qx = len(newStr2[0])
    length_Qy = len(newStr2[1])
    length_x, lcs_x, minIndex_x, maxIndex_x=lcs(newStr1[0], newStr2[0])
    length_y, lcs_y, minIndex_y, maxIndex_y=lcs(newStr1[1], newStr2[1])
    Mx = lcs_x.replace('#','')
    My = lcs_y.replace('#','')
    Dx = newStr1[0][minIndex_x:maxIndex_x+1]
    Dy = newStr1[1][minIndex_y:maxIndex_y+1]
    Sx = Similarity(length_Qx, len(Dx), length_x, N, len(Mx))
    Sy = Similarity(length_Qy, len(Dy), length_y, N, len(My))
    Score = (Sx + Sy)/2
    """
    To Dictionary: 
    """
    parameter['Qx'] = length_Qx
    parameter['Qy'] = length_Qy
    parameter['Lx'] = length_x
    parameter['Ly'] = length_y
    parameter['Mx'] = len(Mx)
    parameter['My'] = len(My)
    parameter['Dx'] = len(Dx)
    parameter['Dy'] = len(Dy)
    parameter['Sx'] = Sx
    parameter['Sy'] = Sy
    parameter['Score'] = Score
    
    return Score, parameter

def GetDays(time_query):
    #"2018-01-01", "9"
    start = [int(i) for i in time_query[0].split('-')]
    start.append(int(time_query[1]))
    end = [int(i) for i in time_query[2].split('-')]
    end.append(int(time_query[3]))
    

    startDay = date(start[0], start[1], start[2])
    endDay = date(end[0], end[1], end[2])

    allDaysList = endDay - startDay    # 起始終止日期之間的所有日期
    allHours = []    # 儲存起始終止日期之間的所有小時

    for i in range(allDaysList.days + 1):
        day = str(startDay + timedelta(days=i)).replace('-', '/')    # 當日日期
        
        # 轉格式: 拿掉第一個 0 ('2018/1/2 17:00' -> '2018/01/02 17:00')
        aday = day.split('/')
        day = aday[0]
        for element in aday[1:]:
            if (element[0] == "0"):
                element = element[1:]
            day += "/" + element
        hr = ""     # 小時

        # 如果是起始日, 小時: 起始時間~24
        if(i == 0):
            for i in range(start[3], 24):
                hr = '%02d' % i + ':00'
                allHours.append(str(day) + " " + hr)
        # 如果是結束日, 小時: 0~結束時間
        elif(i == allDaysList.days):
            for i in range(0, end[3]+1):
                hr = '%02d' % i + ':00'
                allHours.append(str(day) + " " + hr)
        # 其他,  小時: 0~24
        else:
            for i in range(24):
                hr = '%02d' % i + ':00'
                allHours.append(str(day) + " " + hr)
                
    return allHours


def FilterTime(library, time_query):
    days = GetDays(time_query)
    toDelete = []    # 把要刪除的項目日期加到 list

    for date in library.keys():
        if date not in days:
            toDelete.append(date)

    # 移除不需要的 item
    for date in toDelete:
        library.pop(date)
    
    return library


def Filter(library, weather_query):
    query = [-100, 10000, -100, 10000, -100, 10000, -100, 10000]
    for i in range(1, len(weather_query)):
        if(weather_query[i] != 'X'):
            query[i-1] = float(weather_query[i])
    query.insert(0, weather_query[0])
    # print(query)
    # print(query)

    toDelete = []    # 把要刪除的項目日期加到 list

    for date in library.keys():

    # date = "2018/8/7 16:00"
        # 過濾風向
        if(weather_query[0] != 'X'):
            if(library[date]['WD'] != query[0]):
                # print(library[date]['WD'])
                toDelete.append(date)
        # 過濾風速
        if(weather_query[1] != 'X' or weather_query[2] != 'X'):
            if(library[date]['WS'] < query[1] or library[date]['WS'] > query[2]):
                toDelete.append(date)
        # 過濾壓力
        if(weather_query[3] != 'X' or weather_query[4] != 'X'):
            if(library[date]['PS'] < query[3] or library[date]['PS'] > query[4]):
                toDelete.append(date)
        # 過濾氣溫
        if(weather_query[5] != 'X' or weather_query[6] != 'X'):
            if(library[date]['TP'] < query[5] or library[date]['TP'] > query[6]):
                toDelete.append(date)
        # 過濾濕度
        if(weather_query[7] != 'X' or weather_query[8] != 'X'):
            if(library[date]['RH'] < query[7] or library[date]['RH'] > query[8]):
                toDelete.append(date)
        
    # 移除重複項
    toDelete = list(dict.fromkeys(toDelete))
    # print("library: ", len(library))
    # print(library)
    # print("toDelete: ", len(toDelete))
    # print(toDelete)
    
    # 移除不需要的 item
    for date in toDelete:
        
        library.pop(date)
    
    # print(len(library))
    return library

def main(argv):
    
    query = []
    weather_query = []
    time_query = []
    """
    try:
        opts, args = getopt.getopt(argv,"hx:y:",["stringx=","stringy="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('compare_all_data.py -x <stringX> -y <stringY>')
            sys.exit()
        elif opt in ("-x", "--stringx"):
            stringX = arg
            query.append(stringX)
        elif opt in ("-y", "--stringy"):
            stringY = arg
            query.append(stringY)
    """
    # print('argv: ')
    # print(argv)
    # print('-----')
    for i in argv:
        query.append('#'+i)
    weather_query = argv[2].split('/')
    weather_query.pop()
    time_query = argv[3].split('/')
    time_query.pop()
    # print(query)
    # print ('2DStringX：', stringX)
    # print ('2DStringY：', stringY)
    #query = list(map(str,input("String to compare: ").split()))
    library = defaultdict(dict)
    with open('/home/s3014/Customize-2DString-/mysite/weather/codes/file_output(try2)_wind.csv', newline='') as csvfile:
        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)
        for row in rows:
            tmp = row
            # print('row')
            # print(tmp)
            #tmp = row.split('\t')
            #print(tmp)
            if tmp[1] == 'X':
                continue
            # 0 time , 1 string of x , 2 string of y
            library[tmp[0]]['X'] = tmp[1]
            library[tmp[0]]['Y'] = tmp[2]
            library[tmp[0]]['WD'] = tmp[3]
            library[tmp[0]]['WS'] = float(tmp[4])
            library[tmp[0]]['PS'] = float(tmp[5])
            library[tmp[0]]['TP'] = float(tmp[6])
            library[tmp[0]]['RH'] = int(tmp[7])
        csvfile.close()
        #print(library['2018/1/3 19:00']['X'])
    #print('Read End')
    # print(library)
    
    library = Filter(library, weather_query)
    # print(library)
    if (argv[3] != "////"):
        library = FilterTime(library, time_query)
    
    allScore = {}
    parameter_All = {}
    for i in library.keys():
        tmp = [library[i]['X'],library[i]['Y']]
        #if Score(tmp,query) < 1.03:
        #print(i)
        allScore[i], parameter_All[i] = Score(tmp,query)
        #print(tmp)
    #print('Score End')
    allScore_sorted = sorted(allScore.items(),key=lambda item:item[1],reverse=True)
    dictdata = {}
    topTen = allScore_sorted[:100]
    #print(topTen)
    tmpDate={}
    for date in topTen:
        if date[0].split()[0] not in tmpDate.keys():
            tmpDate[date[0].split()[0]] = date[0].split()[1]
    # for i in tmpDate.keys():
    #     print(i,end = ' ')
    #     print(tmpDate[i])
    for data in topTen:
        dictdata[data[0]] = data[1]
        # print(data[0])
        # print(library[data[0]]['X'], library[data[0]]['Y'])
    
    tmpStr = ''
    for i in dictdata.keys():
        print(i, end='\t')
        tmpStr += i.replace(' ','-') + ' ' 
        print(dictdata[i])
    # print(allScore['2018/1/1  04:00'])
    # print(list(sorted(allScore[i])[:10]))
    # print('query to select:')
    # print(tmpStr)
    # print(parameter_All)

    # print('==============================')
    # print('Input Example: 2018/8/22-23:00 2018/8/23-03:00')
    # print('==============================')
    # print('Enter the date that you want to check seperating with SPACE:')
    #date = list(map(str,input().split()))
    date = list(tmpStr.split())
    for i in range(len(date)):
        date[i] = date[i].replace('-',' ')
    selectData = defaultdict(dict)
    with open('/home/s3014/Customize-2DString-/mysite/weather/codes/2018micro高斯new.csv', newline='') as csvfile:
        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)
        for row in rows:
            if row[0] in date:
                tmp = []
                for i in row[1:]:
                    tmp.append(i)
                selectData[row[0]]['oringin'] = tmp 
        csvfile.close()
    #print(selectData)
    for i in selectData.keys():
        tmp_level = []
        for j in selectData[i]['oringin']:
            tmp_level.append(segment(j))
        selectData[i]['afterLevel'] = tmp_level
    #print(selectData)
    library = defaultdict(dict)
    with open('/home/s3014/Customize-2DString-/mysite/weather/codes/allData.csv', newline='') as csvfile:
        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)
        for row in rows:
            tmp = row
            #tmp = row.split('\t')
            if tmp[1] == 'X':
                continue
            # 0 time , 1 string of x , 2 string of y
            library[tmp[0]]['X'] = tmp[1]
            library[tmp[0]]['Y'] = tmp[2]
        csvfile.close()
    # for i in selectData.keys():
    #     # print(i)
    #     # print(parameter_All[i])
    #     for j in parameter_All[i].keys():
    #         print(j , end = ' : ')
    #         print(parameter_All[i][j])
    now = time.strftime("%m-%d-%Y_%H-%M-%S", time.localtime())
    with open('/home/s3014/Customize-2DString-/mysite/weather/codes/output_selectDate_'+now+'.csv', 'w', newline='') as csvfile:
        # 以空白分隔欄位，建立 CSV 檔寫入器
        writer = csv.writer(csvfile, delimiter=',')
        for i in selectData.keys():
            writer.writerow([i])
            if i in library.keys():
                writer.writerow([library[i]['X']])
                writer.writerow([library[i]['Y']])
                writer.writerow(parameter_All[i])
                writer.writerow([parameter_All[i]['Qx'],parameter_All[i]['Qy'],parameter_All[i]['Lx'],parameter_All[i]['Ly'],parameter_All[i]['Mx'],parameter_All[i]['My'],parameter_All[i]['Dx'],parameter_All[i]['Dy'],parameter_All[i]['Sx'],parameter_All[i]['Sy'],parameter_All[i]['Score']])
            for j in range(0,100,10):
                writer.writerow(selectData[i]['afterLevel'][j:j+10])

if __name__ == '__main__':
    main(sys.argv[1:])
