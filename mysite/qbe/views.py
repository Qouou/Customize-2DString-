from collections import defaultdict
import csv
from email.mime import image
from django.shortcuts import render
from django.conf import settings
import os

# 2018/11/7 19:00 -> 2018-11-7-19-00.png
def getImageSrc(time):
    imageName = time.split(' ')[0].split('/')[0] + '-' + time.split(' ')[0].split('/')[1] + '-' + time.split(' ')[0].split('/')[2] + '-' + time.split(' ')[1].split(':')[0] + '-' + time.split(' ')[1].split(':')[1] + '.png'
    return imageName


def getQuery(request):
    if request.POST:
        # get formdata from frontend
        year = request.POST['year']
        month = request.POST['month']
        day = request.POST['day']
        hour = request.POST['hour']
        mode = request.POST['dataset']

        source = year + '/' + month + '/' + day + ' ' + hour.zfill(2) + ':00'
        
        # find the 100 greatest frames
        ctx = {}
        pwd=settings.BASE_DIR + "/qbe/codes/"
        os.chdir(pwd)
        print("mode:", mode)
        command = ""
        if mode == "level":    #level
            command = "python3 HD_A_toWeb.py " + source
        else:    #original
            command = "python3 rasterScan_D_toWeb.py " + source
        print(command)

        tmp = os.popen(command).readlines()
        # print("tmp:", tmp)
        result = []
        # print("result:", tmp)
        for i in range(len(tmp)):
            result.append(tmp[i].replace('\n', ''))
        ctx['result'] = result

        # read the weather data
        library = defaultdict(dict)
        with open('/home/tsai-jen/Customize-2DString-/mysite/weather/codes/file_output(try2)_wind.csv', newline='') as csvfile:
            rows = csv.reader(csvfile)
            next(rows)
            for row in rows:
                tmp = row
                library[tmp[0]]['WD'] = tmp[3]
                library[tmp[0]]['WS'] = float(tmp[4])
                library[tmp[0]]['PS'] = float(tmp[5])   #氣壓
                library[tmp[0]]['TP'] = float(tmp[6])   #溫度
                library[tmp[0]]['RH'] = int(tmp[7])
            csvfile.close()

        # match weather data with result
        dateData = []
        hourData = []
        scoreData = []
        rankData = []
        imageData = []
        WDdata = []
        WSdata = []
        PSdata = []
        TPdata = []
        RHdata = []
        for i in range(len(ctx['result'])):
            # print(ctx['result'][i])
            tmp =  ctx['result'][i]
            scoreData.append(tmp.split(' ')[0])
            dateData.append(tmp.split(' ')[1])
            hourData.append(tmp.split(' ')[2])
            rankData.append(tmp.split(' ')[3])
            time = tmp.split(' ')[1] + " " + tmp.split(' ')[2]
            # print("time:", time)
            imageData.append(getImageSrc(time))
            WDdata.append(library[time]['WD'])
            WSdata.append(library[time]['WS'])
            PSdata.append(library[time]['PS'])
            TPdata.append(library[time]['TP'])
            RHdata.append(library[time]['RH'])

        ctx['resultDate'] = dateData
        ctx['resultHour'] = hourData
        ctx['resultScore'] = scoreData
        ctx['resultRank'] = rankData
        ctx['resultImage'] = imageData
        ctx['resultWD'] = WDdata
        ctx['resultWS'] = WSdata
        ctx['resultPS'] = PSdata
        ctx['resultTP'] = TPdata
        ctx['resultRH'] = RHdata

        ctx['sourceDate'] = source
        ctx['sourceImage'] = getImageSrc(source)
        ctx['sourceWD'] = library[source]['WD']
        ctx['sourceWS'] = library[source]['WS']
        ctx['sourcePS'] = library[source]['PS']
        ctx['sourceTP'] = library[source]['TP']
        ctx['sourceRH'] = library[source]['RH']
        ctx['sourceDataset'] = mode

        # print(ctx)

    return render(request, 'qbeResult.html', ctx)

# Create your views here.
def qbe(request):
    # return HttpResponse("Hello, world. You're at the query index.")
    # return 30 data (100) 
    return render(request, 'qbe.html')