from django.shortcuts import render
import json
# Create your views here.
from django.http import HttpResponse
import os
from PIL import Image
from django.conf import settings

def index(request):
    # return HttpResponse("Hello, world. You're at the query index.")
    # return 30 data (100) 
    return render(request, 'index.html')

def score(request):
    ctx = {}
    # 傳起始與終止的時間
    if request.POST:
        stringX = request.POST['StringX']
        stringY = request.POST['StringY']
        ctx['stringX'] = stringX
        ctx['stringY'] = stringY
        pwd=settings.BASE_DIR + "/weather/codes/"
        os.chdir(pwd)
        command = 'python3 compare_all_data.py ' + stringX +' ' + stringY
        ctx['allContainer'] = os.popen(command).readlines()
        date = []
        content = []
        score = []
        time = []
        for i in ctx['allContainer']:
            tmp = i.split()
            date.append(tmp[0].replace('/','-')+'-'+tmp[1].replace(':','-')+'.png')
            time.append(tmp[1].replace(':','-'))
            content.append(tmp[2])
            # score.append(tmp[3])
        ctx['resultDate'] = date
        ctx['resultTime'] = time
        ctx['resultContent'] = content
        # ctx['resultScore'] = score
        ctx['images'] = [i for i in range(30)]
        jsonDate = json.dumps(ctx['resultDate'])
        ctx['jsonDate'] = jsonDate
        
    return render(request, "score.html", ctx)

def segment(data):
    if data == 'A':
        return 0
    elif data == 'B':
        return 10
    elif data == 'C':
        return 20
    elif data == 'D':
        return 30
    elif data == 'E':
        return 40
    elif data == 'F':
        return 50
    elif data == 'G':
        return 80
    elif data == 'H':
        return 120
    elif data == 'I':
        return 200
    elif data == 'J':
        return 300
    else:
        return -1 

def mixPic(mask_path):
    #開啟照片
    imageA = Image.open(mask_path+'.png')
    imageA = imageA.convert('RGBA')
    x, y = imageA.size

    # Transparency
    for i in range(x):
        for k in range(y):
            color = imageA.getpixel((i, k))
            if color == (255, 255, 255, 255):
                color = (255, 255, 255, 0)
                imageA.putpixel((i, k), color)
                continue
            color = color[:-1] + (100, )
            imageA.putpixel((i, k), color)

    widthA , heightA = imageA.size

    #開啟簽名檔
    imageB = Image.open('../map_fix.png')
    imageB = imageB.convert('RGBA')
    widthB , heightB = imageB.size

    #重設簽名檔的寬為照片的1/2
    newWidthB = int(widthA)
    #重設簽名檔的高依據新的寬度等比例縮放
    newHeightB = int(heightB/widthB*newWidthB)
    #重設簽名檔圖片
    imageB_resize = imageB.resize((newWidthB, newHeightB))

    #新建一個透明的底圖
    resultPicture = Image.new('RGBA', imageA.size, (0, 0, 0, 0))

    #把照片貼到底圖
    resultPicture.paste(imageB_resize,(0,0))

    #設定簽名檔的位置參數
    right_bottom = ( newWidthB - widthA , 0)

    #為了背景保留透明度，將im參數與mask參數皆帶入重設過後的簽名檔圖片
    resultPicture.paste(imageA, right_bottom, imageA)

    #儲存新的照片
    os.chdir(os.getcwd())
    resultPicture.save(mask_path + "_mix.png")

def findRank(data):
    print(data)
    # print(data)
    ranking = [-1 for i in range(len(data))]
    no = 1
    ranking[0] = 1

    for i in range(len(data)):
        print(data[i])
        data[i] = float(data[i])
    for i in range(1, len(data)):
        if(data[i] < data[i-1]):
            no += 1
        ranking[i] = no
    return ranking


def getQuery(request):
    ctx = {}
    if request.POST:
        w_data =  request.POST.getlist('weather_query[]')    # 天氣因子的query
        # w_data =  request.POST['WD'] + "/" + request.POST['WS_l'] + "/" + request.POST['WS_u'] + "/" + request.POST['PS_l'] + "/" + request.POST['PS_u'] + "/" + request.POST['TP_l'] + "/" + request.POST['TP_u'] + "/" + request.POST['RH_l'] + "/" + request.POST['RH_u'] 
        weather_query =""

        for i in range(len(w_data)):
            if w_data[i] == "":
                w_data[i] = "X"
            weather_query += w_data[i] + "/"
        ctx['weather_query'] = weather_query
        print(ctx['weather_query'])
        
        time_query = ""
        t_data =  request.POST.getlist('time_query[]')    # 時間的query
        for i in range(len(t_data)):
            time_query += t_data[i] + "/"
        ctx['time_query'] = time_query

        data = request.POST['data']
        datalist = data.split(',')
        for i in range(len(datalist)):
            datalist[i] = segment(datalist[i])
        dataString = ' '.join(str(word) for word in datalist)
        print("dataString: ", dataString)
        pwd=settings.BASE_DIR + "/weather/codes/"
        os.chdir(pwd)
        os.system("javac ContourTracingViaWeb.java")
        command = "java ContourTracingViaWeb "+ dataString
        getString = os.popen(command).readlines()

        print("getString: ", getString)
        # print(getString)
        stringX = getString[1].split()[0]
        stringY = getString[1].split()[1]
        
        ctx['stringX'] = stringX
        ctx['stringY'] = stringY
        # os.chdir("C:/sources/LCS")
        # input can't read when starting with '#'
        stringXwithoutSharp = stringX[1:]
        stringYwithoutSharp = stringY[1:]
        command = 'python3 compare_all_data.py ' + stringXwithoutSharp +' ' + stringYwithoutSharp + ' ' + weather_query + ' ' + time_query
        print(command)

        ctx['allContainer'] = os.popen(command).readlines()
        # print("allContainer", ctx['allContainer'] )
        
        date = []
        content = []
        score = []
        time = []
        WDdata = []
        WSdata = []
        PSdata = []
        TPdata = []
        RHdata = []

        for i in ctx['allContainer']:
            tmp = i.split()
            date.append(tmp[0].replace('/','-')+'-'+tmp[1].replace(':','-')+'.png')
            time.append(tmp[1].replace(':','-'))
            content.append(tmp[2])
            # score.append(tmp[3])
            WDdata.append(tmp[3])
            WSdata.append(tmp[4])
            PSdata.append(tmp[5])
            TPdata.append(tmp[6])
            RHdata.append(tmp[7])
        ctx['resultDate'] = date
        ctx['resultTime'] = time
        ctx['resultContent'] = content
        ctx['resultWD'] = WDdata
        ctx['resultWS'] = WSdata
        ctx['resultPS'] = PSdata
        ctx['resultTP'] = TPdata
        ctx['resultRH'] = RHdata
        # ctx['resultScore'] = score
        ctx['images'] = [i for i in range(30)]
        jsonDate = json.dumps(ctx['resultDate'])
        ctx['jsonDate'] = jsonDate
        ctx['ranking'] = findRank(content)
        # print('--')
        # print(content)
        # print('--')
        

        
        pwd=settings.BASE_DIR + "/weather/codes/"
        os.chdir(pwd)

        getPicCommand = 'python3 userDataPic.py ' + dataString
        getPicName = os.popen(getPicCommand).readlines()[0].strip()
        ctx['PicName'] = getPicName
        pwd=settings.BASE_DIR + "/static/sis"
        os.chdir(pwd)
        mixPic(getPicName)
    return render(request, "score.html", ctx)
