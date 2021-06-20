from django.shortcuts import render
import json
# Create your views here.
from django.http import HttpResponse
import os
from PIL import Image

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
        print(os.getcwd())
        os.chdir("/home/s3014/Customize-2DString-/mysite/weather/codes/")
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
        
        print('===========')
        print(jsonDate)
        print('===========')
        print(ctx['resultDate'])
        print(ctx['resultTime'])
        print(ctx['resultContent'])
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

def getQuery(request):
    ctx = {}
    if request.POST:
        data = request.POST['data']
        datalist = data.split(',')
        for i in range(len(datalist)):
            datalist[i] = segment(datalist[i])
        dataString = ' '.join(str(word) for word in datalist)
        print(dataString) 
        print('---java----')
        print(os.getcwd())
        os.chdir("/home/s3014/Customize-2DString-/mysite/weather/codes")
        os.system("javac ContourTracingViaWeb.java")
        command = "java ContourTracingViaWeb "+ dataString
        getString = os.popen(command).readlines()
        print(getString[1])

        stringX = getString[1].split()[0]
        stringY = getString[1].split()[1]
        
        ctx['stringX'] = stringX
        ctx['stringY'] = stringY
        # os.chdir("C:/sources/LCS")
        print('---LCS----')
        # input can't read when starting with '#'
        stringXwithoutSharp = stringX[1:]
        stringYwithoutSharp = stringY[1:]
        command = 'python3 compare_all_data.py ' + stringXwithoutSharp +' ' + stringYwithoutSharp
        print(command)
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
        
        print(jsonDate)
        
        print('---Pic----')
        print(os.getcwd())
        getPicCommand = 'python3 userDataPic.py ' + dataString
        print(getPicCommand)
        getPicName = os.popen(getPicCommand).readlines()[0].strip()
        ctx['PicName'] = getPicName
        print('---static----')
        print(os.getcwd())
        os.chdir("/home/s3014/Customize-2DString-/mysite/weather/static/sis")
        mixPic(getPicName)
    return render(request, "score.html", ctx)
