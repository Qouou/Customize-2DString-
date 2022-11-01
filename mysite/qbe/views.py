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
        dataset = request.POST['dataset']

        source = year + '/' + month + '/' + day + ' ' + hour.zfill(2) + ':00'
        
        # find the 100 greatest frames
        ctx = {}
        pwd=settings.BASE_DIR + "/qbe/codes/"
        os.chdir(pwd)
        command = "python3 HD_A_toWeb.py " + source
        print(command)

        tmp = os.popen(command).readlines()
        result = []
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
        imageData = []
        WDdata = []
        WSdata = []
        PSdata = []
        TPdata = []
        RHdata = []
        for i in range(len(ctx['result'])):
            time = ctx['result'][i]
            dateData.append(time.split(' ')[0])
            hourData.append(time.split(' ')[1])
            imageData.append(getImageSrc(time))
            WDdata.append(library[time]['WD'])
            WSdata.append(library[time]['WS'])
            PSdata.append(library[time]['PS'])
            TPdata.append(library[time]['TP'])
            RHdata.append(library[time]['RH'])

        ctx['resultDate'] = dateData
        ctx['resultHour'] = hourData
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

        print(ctx)

    return render(request, 'qbeResult.html', ctx)

# Create your views here.
def qbe(request):
    # return HttpResponse("Hello, world. You're at the query index.")
    # return 30 data (100) 
    return render(request, 'qbe.html')